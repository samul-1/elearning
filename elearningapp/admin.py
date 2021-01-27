from django.contrib import admin
from .models import *

class ProgramExerciseAdmin(admin.ModelAdmin):
    list_display = ('text', 'course')

class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'input_case', 'expected_output')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_questions_per_test', 'setup_completed', 'exercise_modality', 'pk')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'pk')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'course', 'pk')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'answer_index', 'pk')

class GlobalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name')

class CourseSpecificProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'admin_of', 'collaborator_of')

class ActiveTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'timestamp')

class ActiveQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'test')

class TakenTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'timestamp', 'score')

class SeenQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'timestamp', 'answer_index', 'user')

admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(GlobalProfile, GlobalProfileAdmin)
admin.site.register(CourseSpecificProfile, CourseSpecificProfileAdmin)
admin.site.register(ActiveTest, ActiveTestAdmin)
admin.site.register(ActiveQuestion, ActiveQuestionAdmin)
admin.site.register(TakenTest, TakenTestAdmin)
admin.site.register(SeenQuestion, SeenQuestionAdmin)
admin.site.register(ProgramExercise, ProgramExerciseAdmin)
admin.site.register(TestCase, TestCaseAdmin)
