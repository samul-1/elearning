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