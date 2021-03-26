import json
import random
import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from users.models import CourseSpecificProfile, GlobalProfile

from .exceptions import OutOfQuestionsException
from .forms import CourseForm, PermissionForm, QuestionForm, ReportForm
from .models import (
    ActiveTest,
    Answer,
    AnswersInTakenTest,
    Category,
    Course,
    CoursePermission,
    Question,
    Report,
    SeenQuestion,
    TakenTest,
)


@login_required
def redirect_to_login_or_profile(request):
    return redirect("profile")


@login_required
def create_course(request):
    if not request.user.globalprofile.is_teacher:
        return HttpResponseForbidden()

    if request.method == "POST":
        form_data = json.loads(request.body.decode("utf-8"))
        form = CourseForm(form_data, user=request.user.globalprofile)
        print(form_data)
        if form.is_valid():
            new_course = form.save()
            CourseSpecificProfile.objects.create(user=request.user, course=new_course)
        else:
            print(form.errors)
            return HttpResponseBadRequest()

        return JsonResponse({"courseId": new_course.pk}, safe=False)

    # GET
    return render(
        request,
        "elearningapp/createcourse.html",
    )


# course control panel
@login_required
def course_cp(request, course_id):
    course = get_object_or_404(Course, pk__exact=course_id)

    # reject with 403 if user isn't authorized to view the control panel for this course
    if course not in request.user.globalprofile.admin_of.all() and (
        request.user.coursespecificprofile_set.filter(course=course).count() == 0
        or not hasattr(
            request.user.coursespecificprofile_set.get(course=course),
            "coursepermission",
        )
    ):
        return HttpResponseForbidden()

    aggregated_info = course.get_aggregated_info()

    context = {
        "course": course,
        "reports": course.get_reports(resolved=False),
        "last_actions": course.get_last_actions(5),
        "number_of_subscribers": aggregated_info["number_of_subscribers"],
        "number_of_tests_taken": aggregated_info["number_of_tests_taken"],
        "average_score": aggregated_info["average_score"],
        "hardest_questions": course.get_hardest_questions(3),
        "admin": "true"
        if course in request.user.globalprofile.admin_of.all()
        else "false",  # using 'true' and 'false' to prevent issues with js frontend consuming the value
    }

    # get user's permissions, if they have a permission object associated to them (admins don't)
    if len(
        course_profile := request.user.coursespecificprofile_set.filter(course=course)
    ) != 0 and hasattr(course_profile[0], "coursepermission"):
        context["my_permissions"] = json.dumps(
            course_profile[0].coursepermission.serialize()
        )
        context["user_id"] = course_profile[0].pk
    else:
        context["my_permissions"] = {}
        context[
            "user_id"
        ] = "null"  # once again using 'null' as a string for easier passing of the value as a prop

    return render(
        request,
        "elearningapp/course_cp.html",
        context,
    )


# accessed via GET, returns a list of users subscribed to the course
@login_required
def get_course_users(request, course_id):
    course = get_object_or_404(Course, pk__exact=course_id)
    return JsonResponse(course.get_subscribed_users(), safe=False)


# accessed via GET, returns a lit of reports that have been made to questions from the course
@login_required
def get_course_reports(request, course_id):
    course = get_object_or_404(Course, pk__exact=course_id)
    return JsonResponse(course.get_reports(), safe=False)


# if accessed via GET, gets the first 5 questions for the course and renders template containing the EditQuestion component
# if accessed via PUT, updates the question
# if question_id is specified, the id is passed via the context object to EditQuestion vue component
@login_required
def edit_question(request, course_id, question_id=None):
    course = get_object_or_404(Course, pk__exact=course_id)

    # reject with 403 if user isn't authorized to edit questions for this course
    if course not in request.user.globalprofile.admin_of.all() and (
        request.user.coursespecificprofile_set.filter(course=course).count() == 0
        or not hasattr(
            request.user.coursespecificprofile_set.get(course=course),
            "coursepermission",
        )
        or not request.user.coursespecificprofile_set.get(
            course=course
        ).coursepermission.can_edit_questions
    ):
        return HttpResponseForbidden()

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
            return HttpResponseBadRequest()

    # GET
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


# if accessed via POST, creates a new report for the specified question
# if accessed via PUT, updates the status of the specified report
@login_required
def report_question(request):
    if request.method not in ["POST", "PUT"]:
        return HttpResponseNotAllowed()

    form_data = json.loads(request.body.decode("utf-8"))

    if request.method == "POST":
        question = get_object_or_404(Question, pk__exact=form_data["questionId"])
        form = ReportForm(form_data, user=request.user, question=question)

        if form.is_valid():
            # add new report to db
            form.save()

            return JsonResponse({"success": True})
        else:
            print(form.errors)
            return HttpResponseBadRequest()

    if request.method == "PUT":
        report = get_object_or_404(Report, pk__exact=form_data["reportId"])
        # add report text to form data as it is a mandatory field that isn't supplied when the view is accessed via PUT
        # ? maybe there's a better way to do this
        form_data["text"] = report.text

        form = ReportForm(form_data, instance=report, resolved=form_data["resolved"])
        print(form_data)
        if form.is_valid():
            print("is valid")
            form.save()
            return JsonResponse({"success": True})
        else:
            print(form.errors)
            return HttpResponseBadRequest()


# if accessed via PUT, updates or creates the permissions of a user for a course,
# if accessed via DELETE, deletes the permission object for the specified user and course
def update_course_permissions(request, course_id):
    if request.method == "GET":
        return HttpResponseNotAllowed()
    course = get_object_or_404(Course, pk__exact=course_id)

    # reject with 403 if user isn't authorized to add assistants for this course
    if course not in request.user.globalprofile.admin_of.all() and (
        request.user.coursespecificprofile_set.filter(course=course).count() == 0
        or not hasattr(
            request.user.coursespecificprofile_set.get(course=course),
            "coursepermission",
        )
        or not request.user.coursespecificprofile_set.get(
            course=course
        ).coursepermission.can_manage_contributors
    ):
        return HttpResponseForbidden()

    form_data = json.loads(request.body.decode("utf-8"))
    print(form_data)
    editing_profile = get_object_or_404(
        CourseSpecificProfile, pk=form_data["profile_id"]
    )
    if request.method == "PUT":
        # cannot edit permissions of a course admin
        if course in editing_profile.user.globalprofile.admin_of.all():
            return HttpResponseForbidden()
        # retrieve or create permissions for this user
        # we don't need the boolean returned by get_or_create, hence the _ wildcard
        permissions, _ = CoursePermission.objects.get_or_create(user=editing_profile)
        form = PermissionForm(form_data["permissions"], instance=permissions)

        print(form_data)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            print(form.errors)
            return HttpResponseBadRequest()

    if request.method == "DELETE":
        try:
            permissions = CoursePermission.objects.get(user=editing_profile)
        except CoursePermission.DoesNotExist:
            return HttpResponseNotFound()
        permissions.delete()
        return JsonResponse({"success": True})


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


# accessed via GET by the client for infinite scrolling in the TestHistory vue component
@login_required
def get_taken_tests(request, course_id, amount, until_pk, category=None):
    course = get_object_or_404(Course, pk__exact=course_id)
    user_profile = get_object_or_404(
        CourseSpecificProfile, user__exact=request.user, course__pk__exact=course_id
    )
    # questions = course.get_seen_questions(
    #     request.user,
    #     int(amount),
    #     pk_greater_than=int(starting_from_pk),
    #     category=category,
    # )
    taken_tests = map(
        lambda t: t.serialize(),
        list(user_profile.get_taken_tests(int(amount), pk_less_than=int(until_pk))),
    )
    return JsonResponse(list(taken_tests), safe=False)


# renders template containing CreateQuestion vue component when accessed via GET,
# handles question creation using Question ModelForm when accessed via POST
@login_required
def add_question(request, course_id):
    course = get_object_or_404(Course, pk__exact=course_id)
    # reject with 403 if user isn't authorized to add questions to this course
    if course not in request.user.globalprofile.admin_of.all() and (
        request.user.coursespecificprofile_set.filter(course=course).count() == 0
        or not hasattr(
            request.user.coursespecificprofile_set.get(course=course),
            "coursepermission",
        )
        or not request.user.coursespecificprofile_set.get(
            course=course
        ).coursepermission.can_add_questions
    ):
        return HttpResponseForbidden()

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
            return HttpResponseBadRequest()

        return JsonResponse({"success": True})

    # GET
    return render(
        request,
        "elearningapp/add_question.html",
        context,
    )


# @login_required
# def program_exercise(request, prog_id):
#     exercise = get_object_or_404(ProgramExercise, pk__exact=prog_id)

#     return render(
#         request,
#         "elearningapp/program.html",
#         {
#             "exercise": exercise,
#             "public_test_cases": list(exercise.get_public_test_cases()),
#         },
#     )


# def test_tex(request):
#     questions = Question.objects.filter(pk__gt=53)
#     for q in questions:
#         q.save()
#         for answer in Answer.objects.filter(question=q):
#             answer.save()
#     return HttpResponse(":)")


# @login_required
# def eval_progsol(request, prog_id):
#     exercise = get_object_or_404(ProgramExercise, pk__exact=prog_id)
#     count = 0  # number of passed test cases

#     program = json.loads(
#         request.body.decode("utf-8")
#     )  # user's submission is in request body

#     for testcase in exercise.get_test_cases():
#         inputcase = testcase.input_case

#         # call node to evaluate user's submission passing the test case input parameters
#         res = subprocess.check_output(
#             [
#                 "node",
#                 "elearningapp/node_scripts/evalUserFunction.js",
#                 program,
#                 inputcase,
#             ]
#         )
#         res = str(res)[2:-3]  # trim b' and \n' from the string converted from byte type

#         # successful test case
#         if res == testcase.expected_output:
#             count += 1
#     if (
#         count / TestCase.objects.filter(exercise=exercise).count()
#     ) * 100 >= exercise.minimum_passing_testcase_perc:
#         passing = 1
#     else:
#         passing = 0

#     outcome = {
#         "passing": passing,
#         "positiveCases": count,
#         "totalCases": exercise.get_test_cases().count(),
#     }

#     return JsonResponse(outcome)


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
            return render(
                request,
                "elearningapp/generic_error.html",
                {
                    "course_id": course.pk,
                    "err_title": "Hai già visto tutte le domande disponibili",
                    "err_description": "Puoi cancellare la cronologia delle domande già viste dalla home del corso.",
                },
            )

    # get user's global data
    global_profile = GlobalProfile.objects.get(user=request.user)
    global_user_data = {
        "name": global_profile.user.username,
        "id": global_profile.user.pk,
    }

    """
    global_profile.first_name
        if global_profile.user.first_name != ""
        else """

    context = {
        "course_id": course.pk,
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

    taken_tests = map(
        lambda t: t.serialize(), list(user_profile.get_taken_tests(amount=3))
    )
    return render(
        request,
        "elearningapp/test_history.html",
        {
            "course_id": course_id,
            "tests": list(taken_tests),
            "maxScore": Course.objects.get(pk=course_id).maximum_score(),
        },
    )


# calls a method to evaluate the answers given, save the question and test outcome to user's history;
# returns details about the outcome of the test
@login_required
def check_answers(request, course_id):
    if request.method != "POST":
        return HttpResponseNotAllowed()

    course = get_object_or_404(Course, pk=course_id)

    answers = json.loads(request.body.decode("utf-8"))
    print(answers)
    # TODO check validity of sent json object
    requesting_user = request.user

    current_test = ActiveTest.objects.get(user=requesting_user, course=course)

    outcome = current_test.evaluate_answers(answers)
    current_test.delete()

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
        "access_to_cp": (
            course in request.user.globalprofile.admin_of.all()
            or (
                request.user.coursespecificprofile_set.filter(course=course).count() > 0
                and hasattr(
                    request.user.coursespecificprofile_set.get(course=course),
                    "coursepermission",
                )
            )
        ),
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
