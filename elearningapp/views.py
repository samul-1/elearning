from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import (
    Question,
    Course,
    Category,
    CourseSpecificProfile,
    GlobalProfile,
    ActiveTest,
    Answer,
    TakenTest,
    AnswersInTakenTest,
    SeenQuestion,
    ProgramExercise,
    TestCase,
)
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
def course_cp(request, course_id):
    course = get_object_or_404(Course, pk__exact=course_id)
    aggregated_info = course.get_aggregated_info()

    context = {
        "course": course,
        "number_of_subscribers": aggregated_info["number_of_subscribers"],
        "number_of_tests_taken": aggregated_info["number_of_tests_taken"],
        "average_score": aggregated_info["average_score"],
    }

    return render(
        request,
        "elearningapp/course_cp.html",
        context,
    )


# if accessed via GET, gets the first 5 questions for the course and renders template containing the EditQuestion component
# if accessed via PUT, updates the question
def edit_question(request, course_id):
    if request.method == "PUT":
        form_data = json.loads(request.body.decode("utf-8"))
        question = get_object_or_404(Question, pk=form_data["questionId"])
        form = QuestionForm(form_data, instance=question)

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

    return render(
        request,
        "elearningapp/edit_question.html",
        context,
    )


# accessed via GET by the client for infinite scrolling in the EditQuestion vue component
def get_questions(request, course_id, amount, starting_from_pk, category=None):
    course = get_object_or_404(Course, pk__exact=course_id)
    questions = course.get_complete_questions(
        int(amount), pk_greater_than=int(starting_from_pk), category=category
    )
    return JsonResponse(questions, safe=False)


# renders template containing CreateQuestion vue component when accessed via GET,
# handles question creation using Question ModelForm when accessed via POST
def add_question(request, course_id):
    course = get_object_or_404(Course, pk__exact=course_id)
    categories = Category.objects.filter(course=course)

    context = {
        "course_id": course_id,
        "categories": [{c.pk: c.name} for c in categories],
    }
    if request.method == "POST":
        form_data = json.loads(request.body.decode("utf-8"))
        form = QuestionForm(form_data)

        print(form_data)
        if form.is_valid():
            print("is valid")
            # add new question to db
            new_question = form.save()

            # ans_idx = 1
            # # create an Answer instance for each answer to this question
            # for answer in form_data["answers"]:
            #     ans = Answer(question=new_question, text=answer, answer_index=ans_idx)
            #     ans.save()
            #     ans_idx += 1

            return JsonResponse("ok", safe=False)
        else:
            print(form.errors)
        return

    return render(
        request,
        "elearningapp/add_question.html",
        context,
    )


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


# generates a new test according to the course rules and associates it with requesting user if
# such a test doesn't exist, and returns it; otherwise, returns the existing test
@login_required
def start_new_test(request, course_id):
    requesting_user = request.user  # User.objects.get(pk=user_id)
    course = Course.objects.get(pk=course_id)

    if ActiveTest.objects.filter(user=requesting_user, course=course).count() > 0:
        # user has already an active test associated to them; return that one
        # instead of creating a new one
        active_test = ActiveTest.objects.get(user=requesting_user, course=course)
        return active_test

    # create a new test associated to requesting user in selected course
    new_test = ActiveTest(user=requesting_user, course=course)
    new_test.save()
    try:
        new_test.init_test()
    except OutOfQuestionsException:  # delete the test that was attempted to be initialized and re-throw exception
        new_test.delete()
        raise OutOfQuestionsException

    return new_test


# renders a test for the user
def render_test(request, course_id):
    try:
        current_test = start_new_test(request, course_id)
    except OutOfQuestionsException:
        return HttpResponse("finito le domande!")

    # get user's global data
    global_profile = GlobalProfile.objects.get(user=request.user)
    global_user_data = {
        "name": global_profile.first_name
        if global_profile.first_name != ""
        else global_profile.user.username,
        "id": global_profile.user.pk,
    }

    context = {
        "questions": current_test.format_test_for_user,
        "global_user_data": global_user_data,
    }

    return render(request, "elearningapp/test.html", context)


# returns the list of questions that the user has seen in past tests
def question_history(request, user_id, course_id):
    user_profile = get_object_or_404(
        CourseSpecificProfile, user__pk__exact=user_id, course__pk__exact=course_id
    )

    seen_questions = map(
        lambda sq: sq.serialize(), list(user_profile.get_seen_questions())
    )
    return render(
        request,
        "elearningapp/question_history.html",
        {"questions": list(seen_questions), "user_id": user_id, "course_id": course_id},
    )


# empties the list of seen question for given user and course
def delete_question_history(request, user_id, course_id):
    user_profile = get_object_or_404(
        CourseSpecificProfile, user__pk__exact=user_id, course__pk__exact=course_id
    )

    for question in user_profile.get_seen_questions():
        question.delete()

    return JsonResponse("ok", safe=False)


# returns the list of tests that the user has taken in the past
def test_history(request, user_id, course_id):
    user_profile = get_object_or_404(
        CourseSpecificProfile, user__pk__exact=user_id, course__pk__exact=course_id
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
    # return HttpResponse(taken_tests)


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
    current_test.delete()

    return JsonResponse(outcome.serialize())


# retrieves context for rendering the course dashboard
@login_required
def view_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    try:
        course_profile = CourseSpecificProfile.objects.get(
            user=request.user, course__pk=course_id
        )
    except CourseSpecificProfile.DoesNotExist:
        # TODO handle signing up to new course
        return HttpResponse("not registered")

    # get user's global data
    global_profile = GlobalProfile.objects.get(user=request.user)
    global_user_data = {
        "name": global_profile.first_name
        if global_profile.first_name != ""
        else global_profile.user.username,
        "id": global_profile.user.pk,
    }

    # get user's course specific data
    course_specific_user_data = {
        "number_of_tests_taken": course_profile.number_of_tests_taken,
        "last_score": course_profile.last_score,
        "average_score": course_profile.average_score,
        "last_scores": course_profile.get_last_scores(5),
    }

    # get course's data
    course_data = {
        "name": course.name,
        "id": course.pk,
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