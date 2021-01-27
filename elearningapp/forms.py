from django import forms
from django.forms import ModelForm
from .models import Course, Question, Category


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
    class Meta:
        model = Question
        fields = ["text", "course", "category", "correct_answer_index", "solution_text"]
