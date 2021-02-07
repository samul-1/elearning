from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import GlobalProfile, CourseSpecificProfile
from elearningapp.models import Course
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
import json

# user registration
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            return redirect(reverse("profile"))
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


# user profile page
def profile(request):
    global_profile = request.user.globalprofile
    password_change_form = PasswordChangeForm(user=request.user)
    # get all course profiles
    course_profiles = request.user.coursespecificprofile_set.all()

    courses = [
        {
            "course_name": p.course.name,
            "course_max_score": p.course.maximum_score(),
            "course_id": p.course.pk,
            "average_score": round(p.get_average_score(), 1),
            "average_score_perc": int(
                p.get_average_score() / p.course.maximum_score() * 100
                if p.get_average_score() > 0
                else 0
            ),
            "access_to_cp": p.course in global_profile.admin_of.all()
            or hasattr(p, "coursepermission"),
        }
        for p in course_profiles
    ]

    print(courses)
    context = {
        "global_profile": global_profile,
        "courses": courses,
        "password_change_form": password_change_form,
    }
    return render(request, "profile.html", context)


# creates a new CourseSpecificProfile for the user when signing up to a new course
def course_signup(request, course_id):
    course = Course.objects.get(pk=course_id)
    try:
        CourseSpecificProfile.objects.get(user=request.user, course=course)
        return HttpResponse("already signed up")
    except CourseSpecificProfile.DoesNotExist:
        profile = CourseSpecificProfile(user=request.user, course=course)
        profile.save()
        return redirect("view_course", course_id=course_id)


def change_password(request):
    if request.method == "POST":
        print(request.body)
        form = PasswordChangeForm(
            request.user, json.loads(request.body.decode("utf-8"))
        )
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, "Your password was successfully updated!")
            # return redirect("change_password")
            return JsonResponse({"success": True})
        else:
            # messages.error(request, "Please correct the error below.")
            return JsonResponse({"success": False, "errors": form.errors})
    # else:
    #     form = PasswordChangeForm(request.user)
    # return render(request, "accounts/change_password.html", {"form": form})
