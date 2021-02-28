import random

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .exceptions import OutOfQuestionsException
from .utils import tex_to_svg


class Course(models.Model):
    name = models.CharField(max_length=100)
    number_of_questions_per_test = models.IntegerField(default=10)
    # True if the course has a category distribution, i.e. tests choose a fixed amount of questions from each category
    uses_category_distribution = models.BooleanField(default=False)
    points_for_correct_answer = models.FloatField(default=1)
    points_for_unanswered = models.FloatField(default=0)
    points_for_wrong_answer = models.FloatField(default=-0.5)
    minimum_passing_score = models.FloatField(default=5)

    def __str__(self):
        return self.name

    # returns 'amount' random questions that user hasn't seen yet; if category is specified,
    # the questions will be from that category
    # raises OutOfQuestionsException if there aren't enough questions that satisfy requirements
    def get_questions_for(self, user, amount, category=None):
        # get list of questions already seen by user
        seen_questions = SeenQuestion.objects.filter(user=user)
        seen_question_ids = map(lambda q: q.question.pk, seen_questions)

        questions = Question.objects.filter(course=self).exclude(
            id__in=seen_question_ids
        )
        if category:
            questions = questions.filter(category=category)

        # pick random questions
        try:
            random_questions = random.sample(list(questions), amount)
        except ValueError as err:  # if there aren't enough questions left, return None
            raise OutOfQuestionsException

        return random_questions

    # returns an object containing info about the course
    def get_aggregated_info(self):
        subscribers = apps.get_model(
            "users", model_name="CourseSpecificProfile"
        ).objects.filter(course=self)
        taken_tests = TakenTest.objects.filter(course=self)

        avg_score = (
            (sum([test.score for test in list(taken_tests)]) / taken_tests.count())
            if taken_tests.count() > 0
            else 0
        )

        return {
            "number_of_subscribers": subscribers.count(),
            "number_of_tests_taken": taken_tests.count(),
            "average_score": round(avg_score, 1),
        }

    # returns 'amount' questions, showing correct answer and solution too
    # (meant for use inside of course control panel)
    def get_complete_questions(self, amount, pk_greater_than=0, category=None):
        questions = self.question_set.filter(pk__gt=pk_greater_than)
        if category is not None:
            cat = Category.objects.get(pk=category)
            questions = questions.filter(category=cat)

        questions = questions.order_by("pk")[:amount]
        # TODO add sorting
        return list(
            map(
                lambda q: q.format_complete_question(),
                questions,
            )
        )

    # ? move this to CourseSpecificProfile
    def get_seen_questions(self, user, amount, pk_greater_than=0, category=None):
        questions = user.seenquestion_set.filter(pk__gt=pk_greater_than)
        if category is not None:
            cat = Category.objects.get(pk=category)
            questions = questions.filter(category=cat)

        questions = questions.order_by("pk")[:amount]
        # TODO add sorting
        return list(
            map(
                lambda q: q.serialize(),
                questions,
            )
        )

    # returns the 'quantity' hardest questions from this course,
    # i.e. those with the lowest percentage of times they were answered correctly
    def get_hardest_questions(self, quantity):
        return list(
            map(
                lambda q: q.format_complete_question(),
                self.question_set.all().order_by("percentage_of_correct_answers")[
                    :quantity
                ],
            )
        )

    # returns the last 'quantity' actions taken by course admins or collaborators
    def get_last_actions(self, quantity):
        return list(
            map(
                lambda a: a.serialize(),
                self.staffaction_set.all().order_by("-timestamp")[:quantity],
            )
        )

    # returns the profiles of users who are subscribed to this course
    def get_subscribed_users(self):
        return list(map(lambda u: u.serialize(), self.coursespecificprofile_set.all()))

    # returns all the reports that have been made to questions from this course
    # if resolved is specified, only reports with that status are returned
    def get_reports(self, resolved=None):
        reports = Report.objects.filter(question__course=self)

        if resolved is not None:
            reports = reports.filter(resolved=resolved)
        return list(map(lambda r: r.serialize(), reports))

    def maximum_score(self):
        return self.points_for_correct_answer * self.number_of_questions_per_test


# used to keep track of courses assistants' permissions
# (it's meant to work kinda like Django built-in permission system, but on a per-instance basis rather than per-model)
class CoursePermission(models.Model):
    user = models.OneToOneField(
        "users.CourseSpecificProfile", on_delete=models.CASCADE, null=True
    )
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    can_add_questions = models.BooleanField(default=True)
    can_edit_questions = models.BooleanField(default=True)
    can_manage_contributors = models.BooleanField(default=False)
    # can_edit_contributors = models.BooleanField(default=False)

    def serialize(self):
        return {
            "can_add_questions": self.can_add_questions,
            "can_edit_questions": self.can_edit_questions,
            "can_manage_contributors": self.can_manage_contributors,
        }


class Category(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="categories"
    )  # many to one
    name = models.CharField(max_length=100)
    # how many questions from this category need to appear in each test of this course
    # (used only if the course has 'category distribution' enabled)
    quantity = models.PositiveIntegerField(default=None, null=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # many to one
    category = models.ForeignKey(
        Category, null=True, blank=True, default=None, on_delete=models.SET_NULL
    )  # many to one
    rendered_text = (
        models.TextField()
    )  # contains public text including html generated by mathjax
    text = models.TextField(
        default=""
    )  # contains the actual test that was input upon creating the question
    correct_answer_index = models.PositiveIntegerField()
    solution_text_rendered = models.TextField()
    solution_text = models.TextField(default="")
    # TODO add logic to track who added a question
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    number_of_appearances = models.PositiveIntegerField(default=0)
    percentage_of_correct_answers = models.FloatField(default=100.0)

    def __str__(self):
        return self.text

    # when model is saved, process the question text to render TeX as svg
    def save(self, re_render_text=True, *args, **kwargs):
        # TODO raise exception if question is saved to a category for a course different than that specified in fk Course

        if re_render_text:
            self.rendered_text = tex_to_svg(self.text)
            self.solution_text_rendered = tex_to_svg(self.solution_text)

        return super(Question, self).save(*args, **kwargs)

    # returns a dict containing the public information about the question;
    # i.e. its text and the text of its answers
    def format_question_for_user(self):
        output = {}
        output["text"] = self.rendered_text

        # get all answers to the question
        answers = self.answer_set.all().order_by(
            "answer_index"
        )  # Answer.objects.filter(question=self)
        output["answers"] = [a.rendered_text for a in list(answers)]

        # output["answers"] = {}  # index:text dictionary containing self's answer
        i = 0
        for answer in output["answers"]:
            # output["answers"][i] = answer.text
            # ! REMOVE THIS AFTER DEBUG!!!
            if self.correct_answer_index == i + 1:
                output["answers"][i] += " !"
            i += 1
        return output

    # returns a dict containing all the information about the question;
    # i.e. all its public information, the index of the correct answer, and the solution,
    # as well as the source code for all the texts (question, solution, answers), used for editing a question
    def format_complete_question(self):
        info = self.format_question_for_user()
        info["textSource"] = self.text
        info["solution"] = self.solution_text_rendered
        info["solutionSource"] = self.solution_text
        info["correctAnswerIndex"] = self.correct_answer_index
        info["questionId"] = self.pk
        info["category"] = self.category.pk
        info["wrongAnswersPercentage"] = 100 - self.percentage_of_correct_answers

        # get the source text for all the answers
        answers_sources = Answer.objects.filter(question=self).order_by("answer_index")
        info["answersSources"] = [a.text for a in list(answers_sources)]
        return info

    # returns the PERCENTAGE of times this question was answered correctly relative to
    # how many times it appeared in tests
    # this is intended to be called ONLY by Answer.save() each time this question is answered
    # to access this property from somewhere else, use the field percentage_of_correct_answers
    def get_percentage_right_answers(self):
        right_answer = self.answer_set.get(answer_index=self.correct_answer_index)
        if self.number_of_appearances == 0:
            return 100
        return right_answer.selections / self.number_of_appearances * 100


# a report made by a user about a question containing a mistake
class Report(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    text = models.TextField(default="")
    resolved = models.BooleanField(default=False)

    def serialize(self):
        return {
            "reportId": self.pk,
            "timestamp": str(self.timestamp),
            "userId": self.user.pk,
            "username": self.user.username,
            "firstName": self.user.first_name,
            "lastName": self.user.last_name,
            "question": self.question.format_complete_question(),
            "text": self.text,
            "resolved": 1 if self.resolved else 0,
        }


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # many to one
    rendered_text = models.TextField()
    text = models.TextField(default="")
    answer_index = models.PositiveIntegerField()
    selections = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text

    # when model is saved, process the question text to render TeX as svg
    # and update the percentage of times the corresponding question was answered correctly
    def save(self, re_render_text=True, *args, **kwargs):
        if re_render_text:
            self.rendered_text = tex_to_svg(self.text)

        instance = super(Answer, self).save(*args, **kwargs)

        # re-compute the percentage of correct answers to the question
        self.question.percentage_of_correct_answers = (
            self.question.get_percentage_right_answers()
        )
        self.question.save(re_render_text=False)

        return instance


"""
Models to manage history, active tests, and course cp logs
"""


class StaffAction(models.Model):
    ACTIONS = [
        ("C", "Create"),
        ("E", "Edit"),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # many to one
    action = models.CharField(max_length=1, choices=ACTIONS)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # many to one
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            str(self.course)
            + ": "
            + str(self.user)
            + " "
            + str(self.action)
            + " "
            + str(self.question)
        )

    def serialize(self):
        return {
            "action": self.action,
            "user": self.user.username,
            "question": self.question.text,
            "questionId": self.question.pk,
            "timestamp": str(self.timestamp),
        }


# a test that was taken by a user, detailed with its outcome
class TakenTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # many to one
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True
    )  # many to one
    timestamp = models.DateTimeField(auto_now=True)
    score = models.FloatField()
    passing = models.IntegerField(default=0)  # boolean?

    # returns a json representation of self that the client can consume
    def serialize(self):
        json_self = {
            "score": self.score,
            "timestamp": str(self.timestamp),
            "correctlyAnsweredQuestions": [],
            "unansweredQuestions": [],
            "incorrectlyAnsweredQuestions": [],
            "passing": self.passing,
        }

        for answer in AnswersInTakenTest.objects.filter(test=self):
            # get question info and add the answer that was given to this question in the test
            question_with_your_answer = answer.question.format_complete_question()
            question_with_your_answer["yourAnswer"] = answer.answer_index

            # append question to corresponding list based on whether it was answered correctly,
            # incorrectly, or left unanswered
            if answer.answer_index == -1:
                json_self["unansweredQuestions"].append(question_with_your_answer)
            elif answer.answer_index == answer.question.correct_answer_index:
                json_self["correctlyAnsweredQuestions"].append(
                    question_with_your_answer
                )
            else:
                json_self["incorrectlyAnsweredQuestions"].append(
                    question_with_your_answer
                )

        return json_self


# a question that appeared on a TakenTest, and its answer
class AnswersInTakenTest(models.Model):
    test = models.ForeignKey(TakenTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ? should probably use null instead of -1 for unanswered
    answer_index = models.IntegerField()  # -1 if unanswered


# a question that was seen by the user, together with its answer
# needs a separate model from TakenTest because the history of seen questions
# is erasable, whereas that of taken tests isn't
class SeenQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    # ? should probably use null instead of -1 for unanswered
    answer_index = models.IntegerField(default=-1)  # -1 if unanswered
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "questionId": self.pk,
            "question": self.question.format_complete_question(),
            "givenAnswer": self.answer_index,
        }


# a test currently, associated to a user: used in case they leave and come back to the test
# to retrieve the data without generating a new one, as well as to keep track of what questions
# the answers given by the user need to be checked against
class ActiveTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    # chooses random questions that the requesting user hasn't seen yet according to the course distribution (if any)
    # and adds them to the ManyToMany relationship with Question
    def init_test(self):
        if not self.course.uses_category_distribution:
            # course doesn't have a category distribution (or questions for this course aren't grouped in categories)
            for question in self.course.get_questions_for(
                self.user, self.course.number_of_questions_per_test
            ):
                self.questions.add(question)
        else:
            chosen_questions = []
            # get the right number of questions for each category
            for category in self.course.categories.all():
                chosen_questions.extend(
                    list(
                        self.course.get_questions_for(
                            self.user, category.quantity, category
                        )
                    )
                )

            random.shuffle(chosen_questions)
            for question in chosen_questions:
                self.questions.add(question)
        self.save()

    # returns a list containing all questions of the test,
    # formatted to display their public information
    def format_test_for_user(self):
        output = []

        i = 1

        for question in self.questions.all():
            # add question index to dict for displaying to the user
            temp = question.format_question_for_user()
            temp["idx"] = i
            output.append(temp)
            i += 1

        return output

    # takes in a dict containing the answers to the test's questions; computes the result,
    # updates data about questions and answers, saves the test questions to the history of
    # seen questions, and returns a TakenTest object detailing the outcome of the test
    def evaluate_answers(self, answers):
        taken_test = TakenTest(user=self.user, course=self.course, score=0)
        taken_test.save()

        # update the number of tests taken by the user
        user_profile = self.user.coursespecificprofile_set.get(course=self.course)
        user_profile.number_of_tests_taken += 1
        user_profile.save()

        questions = self.questions.all()  # ? could use select_related('answer_set')
        score = 0

        for question, answer in zip(
            questions, map(lambda a: answers[a], answers)
        ):  # map {index:answer} to answer

            # increment number of appearances of this question
            question.number_of_appearances += 1
            question.save(re_render_text=False)
            # increment number of selections for this answer
            if answer != -1:
                given_answer = question.answer_set.get(answer_index=answer)
                print(given_answer)
                given_answer.selections += 1
                given_answer.save(re_render_text=False)

            # record given answer for history
            ans = AnswersInTakenTest(
                answer_index=answer, question=question, test=taken_test
            )
            ans.save()

            # record question for (deletable) history
            seen_question = SeenQuestion(
                user=self.user, question=question, answer_index=answer
            )
            seen_question.save()

            if int(answer) == question.correct_answer_index:
                score += self.course.points_for_correct_answer
            elif int(answer) == -1:
                score += self.course.points_for_unanswered
            else:
                score += self.course.points_for_wrong_answer

        if score > self.course.minimum_passing_score:
            taken_test.passing = 1  # using 1, 0 instead of True, False to make it easier to convert to JSON
        else:
            taken_test.passing = 0

        taken_test.score = score
        taken_test.save()
        user_profile.last_score = score
        user_profile.save()

        return taken_test


"""
 JavaScript platform models
"""


# class ProgramExercise(models.Model):
#     # TODO implement different types of program question (exact correspondence, function evaluation, ...)

#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     text = models.TextField()
#     is_visible = models.BooleanField(default=True)
#     minimum_passing_testcase_perc = models.PositiveIntegerField(default=100)

#     def __str__(self):
#         return self.text

#     def get_test_cases(self):
#         return TestCase.objects.filter(exercise=self)

#     def get_public_test_cases(self):
#         return map(
#             lambda t: t.serialize(),
#             TestCase.objects.filter(exercise=self, is_public=True),
#         )


# class TestCase(models.Model):
#     exercise = models.ForeignKey(
#         ProgramExercise, on_delete=models.CASCADE
#     )  # many to one
#     input_case = models.TextField()
#     expected_output = models.TextField()
#     is_public = models.BooleanField(default=True)

#     def __str__(self):
#         return self.input_case

#     def serialize(self):
#         return {
#             "input": self.input_case,
#             "output": self.expected_output,
#         }
