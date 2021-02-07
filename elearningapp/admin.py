from django.contrib import admin
from .models import *
from users.models import *


class StaffActionAdmin(admin.ModelAdmin):
    list_display = ("course", "action", "user", "question")


class ProgramExerciseAdmin(admin.ModelAdmin):
    list_display = ("text", "course")


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("exercise", "input_case", "expected_output")


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "pk",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "pk")


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "course", "pk", "percentage_of_correct_answers")


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "answer_index", "pk")


class GlobalProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)


class CourseSpecificProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "course")


class ActiveTestAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "timestamp")


class TakenTestAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "timestamp", "score")


class AnswersInTakenTestAdmin(admin.ModelAdmin):
    list_display = ("answer_index", "question", "test")


class SeenQuestionAdmin(admin.ModelAdmin):
    list_display = ("pk", "question", "timestamp", "answer_index", "user")


class CoursePermissionAdmin(admin.ModelAdmin):
    list_display = ("pk", "user")


admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(GlobalProfile, GlobalProfileAdmin)
admin.site.register(CourseSpecificProfile, CourseSpecificProfileAdmin)
admin.site.register(ActiveTest, ActiveTestAdmin)
# admin.site.register(ActiveQuestion, ActiveQuestionAdmin)
admin.site.register(AnswersInTakenTest, AnswersInTakenTestAdmin)
admin.site.register(TakenTest, TakenTestAdmin)
admin.site.register(SeenQuestion, SeenQuestionAdmin)
admin.site.register(ProgramExercise, ProgramExerciseAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(StaffAction, StaffActionAdmin)
admin.site.register(CoursePermission, CoursePermissionAdmin)