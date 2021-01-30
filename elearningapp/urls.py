from django.urls import path, include, re_path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path("test", views.start_new_test, name="start_new_test"),
    # path('import', views.importQ),
    re_path(r"^test/(?P<course_id>\d+)/$", views.render_test, name="render_test"),
    re_path(r"^course/(?P<course_id>\d+)/$", views.view_course, name="view_course"),
    re_path(
        r"^eval_progsol/(?P<prog_id>\d+)/$", views.eval_progsol, name="eval_progsol"
    ),
    re_path(
        r"^progex/(?P<prog_id>\d+)/$", views.program_exercise, name="program_exercise"
    ),
    re_path(
        r"^question_history/(?P<user_id>\d+)/(?P<course_id>\d+)/$",
        views.question_history,
        name="question_history",
    ),
    re_path(
        r"^delete_question_history/(?P<user_id>\d+)/(?P<course_id>\d+)/$",
        views.delete_question_history,
        name="delete_question_history",
    ),
    re_path(
        r"^test_history/(?P<user_id>\d+)/(?P<course_id>\d+)/$",
        views.test_history,
        name="test_history",
    ),
    path("send_answers", views.check_answers, name="send_answers"),
    path("createcourse", views.create_course, name="create_course"),
    re_path(r"^course_cp/(?P<course_id>\d+)/$", views.course_cp, name="course_cp"),
    re_path(
        r"^add_question/(?P<course_id>\d+)/$", views.add_question, name="add_question"
    ),
    re_path(
        r"^edit_question/(?P<course_id>\d+)/$",
        views.edit_question,
        name="edit_question",
    ),
    re_path(
        r"^get_questions/(?P<course_id>\d+)/(?P<amount>\d+)/(?P<starting_from_pk>\d+)/$",
        views.get_questions,
        name="get_questions",
    ),
    re_path(
        r"^get_questions/(?P<course_id>\d+)/(?P<amount>\d+)/(?P<starting_from_pk>\d+)/(?P<category>\d+)/$",
        views.get_questions,
        name="get_questions",
    ),
]