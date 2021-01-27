from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
import random


class Course(models.Model):
    class ExerciseModalities(models.TextChoices):
        SINGLE_QUESTIONS = "SQ", "Domande singole"
        MACRO_QUESTIONS = "MQ", "Domande raggruppate"
        JS = "JS", "Esercizi JavaScript"

    name = models.CharField(max_length=100)
    number_of_questions_per_test = models.IntegerField(default=10)
    category_distribution = models.JSONField(blank=True)
    points_for_correct_answer = models.FloatField(default=1)
    points_for_unanswered = models.FloatField(default=0)
    points_for_wrong_answer = models.FloatField(default=-0.5)
    minimum_passing_score = models.FloatField(default=5)
    answers_per_question = models.IntegerField(default=4)
    language = models.CharField(max_length=2, null=True, default="IT")
    exercise_modality = models.CharField(
        max_length=2,
        choices=ExerciseModalities.choices,
        default=ExerciseModalities.SINGLE_QUESTIONS,
    )
    setup_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # returns 'amount' random questions that user hasn't seen yet; if category is specified,
    # the questions will be from that category
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
            return None

        return random_questions

    def get_aggregated_info(self):
        subscribers = CourseSpecificProfile.objects.filter(course=self)
        taken_tests = TakenTest.objects.filter(course=self)

        avg_score = (
            sum([test.score for test in list(taken_tests)]) / taken_tests.count()
        )

        return {
            "number_of_subscribers": subscribers.count(),
            "number_of_tests_taken": taken_tests.count(),
            "average_score": avg_score,
        }

    def maximum_score(self):
        return self.points_for_correct_answer * self.number_of_questions_per_test


class ProgramExercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()
    is_visible = models.BooleanField(default=True)
    minimum_passing_testcase_perc = models.IntegerField(default=100)

    def __str__(self):
        return self.text

    def get_test_cases(self):
        return TestCase.objects.filter(exercise=self)

    def get_public_test_cases(self):
        return map(
            lambda t: t.serialize(),
            TestCase.objects.filter(exercise=self, is_public=True),
        )


class TestCase(models.Model):
    exercise = models.ForeignKey(ProgramExercise, on_delete=models.CASCADE)
    input_case = models.TextField()
    expected_output = models.TextField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.input_case

    def serialize(self):
        return {
            "input": self.input_case,
            "output": self.expected_output,
        }

    # TODO implement different types of program question (exact correspondence, function evaluation, ...)


class Category(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=500)
    correct_answer_index = models.IntegerField()
    solution_text = models.CharField(max_length=3000)
    hint_text = models.CharField(max_length=1000, null=True)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    edits_history = models.JSONField(null=True, blank=True)
    number_of_appearences = models.IntegerField(default=0)
    number_of_selections_per_answer = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.text

    # returns a dict containing the public information about the question;
    # i.e. its text and the text of its answers
    def format_question_for_user(self):
        output = {}
        output["text"] = self.text

        # get all answers to that self
        answers = Answer.objects.filter(question=self)
        i = 1
        output["answers"] = {}  # index:text dictionary containing self's answer
        for answer in answers:
            output["answers"][i] = answer.text
            # TODO REMOVE THIS AFTER DEBUG!!!
            if self.correct_answer_index == i:
                output["answers"][i] += " !"
            i += 1
        return output

    # returns a dict containing all the information about the question;
    # i.e. all its public information, the index of the correct answer, and the solution
    def format_complete_question(self):
        info = self.format_question_for_user()
        info["solution"] = self.solution_text
        info["correctAnswerIndex"] = self.correct_answer_index
        return info


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    answer_index = models.IntegerField()

    def __str__(self):
        return self.text


class GlobalProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email_address = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class CourseSpecificProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    last_score = models.IntegerField(default=0)
    number_of_tests_taken = models.IntegerField(default=0)
    highest_score = models.IntegerField(default=0)
    lowest_score = models.IntegerField(default=0)
    average_score = models.IntegerField(default=0)
    collaborator_of = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="collaborator_of",
    )
    admin_of = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="admin_of",
    )

    def __str__(self):
        return str(self.user) + " " + str(self.course)

    def get_seen_questions(self):
        return SeenQuestion.objects.filter(
            user=self.user, question__course__exact=self.course
        )

    def get_taken_tests(self):
        return TakenTest.objects.filter(
            user=self.user, course__exact=self.course
        ).order_by("-timestamp")

    def get_last_scores(self, n=10):
        return list(
            map(
                lambda t: t.score,
                TakenTest.objects.filter(
                    user=self.user, course__exact=self.course
                ).order_by("-timestamp")[0:n],
            )
        )[::-1]


class TakenTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    score = models.FloatField()
    passing = models.IntegerField(default=0)

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


class AnswersInTakenTest(models.Model):
    test = models.ForeignKey(TakenTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_index = models.IntegerField()


class SeenQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_index = models.IntegerField(default=-1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "question": self.question.format_complete_question(),
            "givenAnswer": self.answer_index,
        }


class ActiveTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    # returns a list containing all the questions of the test, formatted to display
    # their public information
    def format_test_for_user(self):
        output = []

        i = 1
        active_questions = ActiveQuestion.objects.filter(test=self)
        for question in active_questions:
            # add question index to dict for displaying to the user
            temp = question.question.format_question_for_user()
            temp["idx"] = i
            output.append(temp)
            i += 1

        return output

    # takes in a dict containing the answers to the test's questions;
    # computes the result, saves the test questions to the history of
    # seen questions, and returns a TakenTest object detailing the outcome of the test
    def evaluate_answers(self, answers):
        taken_test = TakenTest(user=self.user, course=self.course, score=0)
        taken_test.save()

        questions = map(lambda q: q.question, ActiveQuestion.objects.filter(test=self))
        score = 0

        for question, answer in zip(
            questions, map(lambda a: answers[a], answers)
        ):  # map {index:answer} to answer
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

        return taken_test


class ActiveQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test = models.ForeignKey(ActiveTest, on_delete=models.CASCADE)
