import json

from django import forms
from django.forms import ModelForm

from .models import (
    Answer,
    Category,
    Course,
    CoursePermission,
    Question,
    Report,
    StaffAction,
)


class ProgramForm(forms.Form):
    program = forms.CharField(label="", widget=forms.Textarea())


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.question = kwargs.pop("question", None)
        self.resolved = kwargs.pop("resolved", False)
        super(ReportForm, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False):
        instance = super(ReportForm, self).save(self)
        if self.question is not None:
            instance.question = self.question
        if self.user is not None:
            instance.user = self.user

        instance.resolved = self.resolved
        return instance.save()


class PermissionForm(ModelForm):
    class Meta:
        model = CoursePermission
        fields = [
            "can_add_questions",
            "can_edit_questions",
            "can_manage_contributors",
        ]


class QuestionForm(ModelForm):
    answers = forms.CharField(max_length=10000)

    class Meta:
        model = Question
        fields = [
            "text",
            "course",
            "category",
            "correct_answer_index",
            "solution_text",
            "answers",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.action = kwargs.pop("action", None)
        super(QuestionForm, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False):
        # save Question and obtain instance
        instance = super(QuestionForm, self).save(self)

        # create log entry
        log = StaffAction(
            user=self.user,
            course=instance.course,
            question=instance,
            action=self.action,
        )
        log.save()

        if self["answers"].value():
            # update or create Answers for this question
            for (idx, text) in enumerate(self["answers"].value()):
                # we don't need the boolean returned by get_or_create, hence the _ wildcard
                ans, _ = Answer.objects.get_or_create(
                    question=self.instance, answer_index=(idx + 1)
                )
                ans.text = text
                ans.save()

            # delete Answer objects that were deleted in the form
            for answer in Answer.objects.filter(
                question=instance, answer_index__gt=len(self["answers"].value())
            ):
                answer.delete()
        return instance


class CourseForm(ModelForm):
    categories = forms.CharField(max_length=10000, required=False)
    category_distribution_values = forms.CharField(max_length=1000, required=False)

    class Meta:
        model = Course
        fields = [
            "name",
            "uses_category_distribution",
            "number_of_questions_per_test",
            "points_for_correct_answer",
            "points_for_wrong_answer",
            "points_for_unanswered",
            "minimum_passing_score",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(CourseForm, self).__init__(*args, **kwargs)

    def save(self, force_insert=False, force_update=False):
        instance = super(CourseForm, self).save(self)

        # create categories for this course
        for (idx, category) in enumerate(self["categories"].value()):
            cat = Category(name=category, course=instance)
            if self["category_distribution_values"].value():
                # if the course has a category distribution, add the number of questions for this category
                cat.quantity = self["category_distribution_values"].value()[idx]
            cat.save()

        # make user admin of the newly created course
        self.user.admin_of.add(instance)
        self.user.save()

        return instance
