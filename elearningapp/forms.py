from django import forms
from django.forms import ModelForm
from .models import Course, Question, Category, Answer
import json


class ProgramForm(forms.Form):
    program = forms.CharField(label="", widget=forms.Textarea())


# class QuestionForm(forms.Form):
#     text = forms.CharField(max_length=500)
#     course = forms.ModelMultipleChoiceField(queryset=Course.objects.all())
#     category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
#     correct_answer_index = forms.IntegerField()
#     solution_text = forms.CharField(max_length=3000)
#     answers = forms.JSONField()


class QuestionForm(ModelForm):
    answers = forms.CharField(max_length=3000)

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

    def save(self, force_insert=False, force_update=False):
        # save Question and obtain instance
        instance = super(QuestionForm, self).save(self)

        if self["answers"].value():
            # update or create Answers for this question
            for (idx, text) in enumerate(self["answers"].value()):
                # we don't need the boolean returned by get_or_create, hence the wildcard _
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
