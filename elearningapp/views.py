from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import (
    Question,
    Course,
    Category,
    ActiveTest,
    Answer,
    TakenTest,
    AnswersInTakenTest,
    SeenQuestion,
    ProgramExercise,
    TestCase,
)
from users.models import CourseSpecificProfile, GlobalProfile
from .forms import QuestionForm, CourseForm
from django.contrib.auth.models import User
import random
from django.db.models import Q
from django.template import loader
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import subprocess
from .exceptions import OutOfQuestionsException


@login_required
def create_course(request):
    if request.method == "POST":
        form_data = json.loads(request.body.decode("utf-8"))
        form = CourseForm(form_data)
        print(form_data)
        if form.is_valid():
            new_course = form.save()
        else:
            print(form.errors)

        return JsonResponse({"courseId": new_course.pk}, safe=False)

    return render(
        request,
        "elearningapp/createcourse.html",
    )


# course control panel
@login_required
def course_cp(request, course_id):
    course = get_object_or_404(Course, pk__exact=course_id)
    aggregated_info = course.get_aggregated_info()

    context = {
        "course": course,
        "last_actions": course.get_last_actions(5),
        "number_of_subscribers": aggregated_info["number_of_subscribers"],
        "number_of_tests_taken": aggregated_info["number_of_tests_taken"],
        "average_score": aggregated_info["average_score"],
        "hardest_questions": course.get_hardest_questions(3),
    }

    return render(
        request,
        "elearningapp/course_cp.html",
        context,
    )


# if accessed via GET, gets the first 5 questions for the course and renders template containing the EditQuestion component
# if accessed via PUT, updates the question
# if question_id is specified, the id is passed via the context object to EditQuestion vue component
@login_required
def edit_question(request, course_id, question_id=None):
    if request.method == "PUT":
        form_data = json.loads(request.body.decode("utf-8"))
        question = get_object_or_404(Question, pk=form_data["questionId"])
        form = QuestionForm(form_data, user=request.user, action="E", instance=question)

        print(form_data)
        if form.is_valid():
            print("is valid")
            updated_question = form.save()
            print(updated_question)
            return JsonResponse(updated_question.format_complete_question(), safe=False)
        else:
            print(form.errors)

    course = get_object_or_404(Course, pk__exact=course_id)
    categories = Category.objects.filter(course=course)
    questions = course.get_complete_questions(5)

    context = {
        "course_id": course_id,
        "categories": [{c.pk: c.name} for c in categories],
        "questions": questions,
    }

    if question_id is not None:
        context["editing_id"] = question_id

    return render(
        request,
        "elearningapp/edit_question.html",
        context,
    )


# accessed via GET by the client for infinite scrolling in the EditQuestion vue component
@login_required
def get_questions(request, course_id, amount, starting_from_pk, category=None):
    course = get_object_or_404(Course, pk__exact=course_id)
    questions = course.get_complete_questions(
        int(amount), pk_greater_than=int(starting_from_pk), category=category
    )
    return JsonResponse(questions, safe=False)


# accessed via GET by the client for infinite scrolling in the QuestionHistory vue component
@login_required
def get_seen_questions(request, course_id, amount, starting_from_pk, category=None):
    course = get_object_or_404(Course, pk__exact=course_id)
    questions = course.get_seen_questions(
        request.user,
        int(amount),
        pk_greater_than=int(starting_from_pk),
        category=category,
    )
    print(questions)
    return JsonResponse(questions, safe=False)


# renders template containing CreateQuestion vue component when accessed via GET,
# handles question creation using Question ModelForm when accessed via POST
@login_required
def add_question(request, course_id):
    course = get_object_or_404(Course, pk__exact=course_id)
    categories = Category.objects.filter(course=course)

    context = {
        "course_id": course_id,
        "categories": [{c.pk: c.name} for c in categories],
    }
    if request.method == "POST":
        form_data = json.loads(request.body.decode("utf-8"))
        form = QuestionForm(form_data, user=request.user, action="C")

        if form.is_valid():
            # add new question to db
            new_question = form.save()

            return JsonResponse("ok", safe=False)
        else:
            print(form.errors)
        return

    return render(
        request,
        "elearningapp/add_question.html",
        context,
    )


@login_required
def program_exercise(request, prog_id):
    exercise = get_object_or_404(ProgramExercise, pk__exact=prog_id)

    return render(
        request,
        "elearningapp/program.html",
        {
            "exercise": exercise,
            "public_test_cases": list(exercise.get_public_test_cases()),
        },
    )


# def test_tex(request):
#     questions = Question.objects.filter(pk__gt=53)
#     for q in questions:
#         q.save()
#         for answer in Answer.objects.filter(question=q):
#             answer.save()
#     return HttpResponse(":)")


@login_required
def eval_progsol(request, prog_id):
    exercise = get_object_or_404(ProgramExercise, pk__exact=prog_id)
    count = 0  # number of passed test cases

    program = json.loads(
        request.body.decode("utf-8")
    )  # user's submission is in request body

    for testcase in exercise.get_test_cases():
        inputcase = testcase.input_case

        # call node to evaluate user's submission passing the test case input parameters
        res = subprocess.check_output(
            [
                "node",
                "elearningapp/node_scripts/evalUserFunction.js",
                program,
                inputcase,
            ]
        )
        res = str(res)[2:-3]  # trim b' and \n' from the string converted from byte type

        # successful test case
        if res == testcase.expected_output:
            count += 1
    if (
        count / TestCase.objects.filter(exercise=exercise).count()
    ) * 100 >= exercise.minimum_passing_testcase_perc:
        passing = 1
    else:
        passing = 0

    outcome = {
        "passing": passing,
        "positiveCases": count,
        "totalCases": exercise.get_test_cases().count(),
    }

    return JsonResponse(outcome)


# renders a test for the user
@login_required
def render_test(request, course_id):
    requesting_user = request.user  # User.objects.get(pk=user_id)
    course = Course.objects.get(pk=course_id)

    if ActiveTest.objects.filter(user=requesting_user, course=course).count() > 0:
        # user already has an active test associated to them; use that one
        # instead of creating a new one
        current_test = ActiveTest.objects.get(user=requesting_user, course=course)
    else:
        # no active tests found for this user;
        # create a new test associated to requesting user in selected course
        try:
            current_test = ActiveTest(user=requesting_user, course=course)
            current_test.save()
            current_test.init_test()
        except OutOfQuestionsException:
            # delete the test that was attempted to be initialized if exception occurs
            current_test.delete()
            # TODO show an actual page
            return HttpResponse("finito le domande!")

    # get user's global data
    global_profile = GlobalProfile.objects.get(user=request.user)
    global_user_data = {
        "name": global_profile.first_name
        if global_profile.user.first_name != ""
        else global_profile.user.username,
        "id": global_profile.user.pk,
    }

    context = {
        "questions": current_test.format_test_for_user(),
        "global_user_data": global_user_data,
    }

    return render(request, "elearningapp/test.html", context)


# returns the list of questions that the user has seen in past tests
@login_required
def question_history(request, course_id):
    user_profile = get_object_or_404(
        CourseSpecificProfile, user__exact=request.user, course__pk__exact=course_id
    )

    course = Course.objects.get(pk=course_id)
    seen_questions = course.get_seen_questions(user=request.user, amount=5)

    # seen_questions = map(
    #     lambda sq: sq.serialize(), list(user_profile.get_seen_questions())
    # )
    return render(
        request,
        "elearningapp/question_history.html",
        {
            "questions": list(seen_questions),
            "user_id": request.user.pk,
            "course_id": course_id,
        },
    )


# empties the list of seen question for given user and course
@login_required
def delete_question_history(request, course_id):
    user_profile = get_object_or_404(
        CourseSpecificProfile, user__exact=request.user, course__pk__exact=course_id
    )

    for question in user_profile.get_seen_questions():
        question.delete()

    return JsonResponse("ok", safe=False)


# returns the list of tests that the user has taken in the past
@login_required
def test_history(request, course_id):
    user_profile = get_object_or_404(
        CourseSpecificProfile, user__exact=request.user, course__pk__exact=course_id
    )

    taken_tests = map(lambda t: t.serialize(), list(user_profile.get_taken_tests()))
    return render(
        request,
        "elearningapp/test_history.html",
        {
            "tests": list(taken_tests),
            "maxScore": Course.objects.get(pk=course_id).maximum_score(),
        },
    )


# calls a method to evaluate the answers given, save the question and test outcome to user's history;
# returns details about the outcome of the test
@login_required
def check_answers(request):
    if request.method != "POST":
        return

    answers = json.loads(request.body.decode("utf-8"))
    print(answers)
    # TODO check validity of sent json object
    requesting_user = request.user

    # ! TODO check course in addition to requesting user
    current_test = ActiveTest.objects.get(user=requesting_user)

    outcome = current_test.evaluate_answers(answers)
    # current_test.delete()

    return JsonResponse(outcome.serialize())


# retrieves context for rendering the course dashboard
@login_required
def view_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # get course's data
    course_data = {
        "name": course.name,
        "id": course.pk,
    }

    # get user's global data
    global_profile = GlobalProfile.objects.get(
        user=request.user
    )  # we can assume this exists because it's created at signup time and the view has @login_required
    global_user_data = {
        "name": global_profile.user.first_name
        if global_profile.user.first_name != ""
        else global_profile.user.username,
        "id": global_profile.user.pk,
    }

    try:
        course_profile = CourseSpecificProfile.objects.get(
            user=request.user, course__pk=course_id
        )
    except CourseSpecificProfile.DoesNotExist:
        # user isn't signed up to this course, give them a chance to
        return render(
            request,
            "course_register.html",
            {
                "global_user_data": global_user_data,
                "course_data": course_data,
            },
        )

    # get user's course specific data
    course_specific_user_data = {
        "number_of_tests_taken": course_profile.number_of_tests_taken,
        "last_score": course_profile.last_score,
        "average_score": round(course_profile.get_average_score(), 1),
        "last_scores": course_profile.get_last_scores(5),
    }

    return render(
        request,
        "elearningapp/course_dashboard.html",
        {
            "global_user_data": global_user_data,
            "course_specific_user_data": course_specific_user_data,
            "course_data": course_data,
        },
    )
