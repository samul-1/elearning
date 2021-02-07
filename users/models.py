from django.db import models
from elearningapp.models import TakenTest, SeenQuestion, CoursePermission
from django.contrib.auth.models import User
from django.conf import settings

"""
Profiles
"""


class GlobalProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    # contributes_to = models.ManyToManyField("elearningapp.Course", blank=True)
    admin_of = models.OneToOneField(
        "elearningapp.Course",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="admin_of_course",
    )

    def __str__(self):
        return self.user.username


class CourseSpecificProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey("elearningapp.Course", on_delete=models.CASCADE)
    last_score = models.IntegerField(default=0)
    number_of_tests_taken = models.PositiveIntegerField(default=0)
    highest_score = models.IntegerField(default=0)
    lowest_score = models.IntegerField(default=0)
    # average_score = models.IntegerField(default=0)

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

    def get_average_score(self):
        if self.number_of_tests_taken == 0:
            return 0
        sum = 0
        for taken_test in self.user.takentest_set.all():
            sum += taken_test.score
        return sum / self.number_of_tests_taken

    def serialize(self):
        return {
            "id": self.pk,
            "username": self.user.username,
            "firstName": self.user.first_name,
            "lastName": self.user.last_name,
            "email": self.user.email,
            "permissions": self.coursepermission.serialize()
            if hasattr(self, "coursepermission")
            else {},
            "isContributor": hasattr(self, "coursepermission"),
        }