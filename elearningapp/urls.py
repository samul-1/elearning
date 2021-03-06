from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path("", views.redirect_to_login_or_profile),
    re_path(r"^test/(?P<course_id>\d+)/$", views.render_test, name="render_test"),
    re_path(r"^course/(?P<course_id>\d+)/$", views.view_course, name="view_course"),
    re_path(
        r"^update_permissions/(?P<course_id>\d+)/$",
        views.update_course_permissions,
        name="update_course_permissions",
    ),
    re_path(
        r"^get_reports/(?P<course_id>\d+)/$",
        views.get_course_reports,
        name="get_course_reports",
    ),
    path(
        "report",
        views.report_question,
        name="report_question",
    ),
    re_path(
        r"^users/(?P<course_id>\d+)/$", views.get_course_users, name="get_course_users"
    ),
    re_path(
        r"^question_history/(?P<course_id>\d+)/$",
        views.question_history,
        name="question_history",
    ),
    re_path(
        r"^delete_question_history/(?P<course_id>\d+)/$",
        views.delete_question_history,
        name="delete_question_history",
    ),
    re_path(
        r"^test_history/(?P<course_id>\d+)/$",
        views.test_history,
        name="test_history",
    ),
    re_path(
        r"send_answers/(?P<course_id>\d+)/$", views.check_answers, name="send_answers"
    ),
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
        r"^edit_question/(?P<course_id>\d+)/(?P<question_id>\d+)/$",
        views.edit_question,
        name="edit_question",
    ),
    re_path(
        r"^get_questions/(?P<course_id>\d+)/$",
        views.get_questions,
        name="get_questions",
    ),
    re_path(
        r"^get_questions/(?P<course_id>\d+)/(?P<amount>\d+)/(?P<starting_from_pk>\d+)/$",
        views.get_questions,
        name="get_questions",
    ),
    re_path(
        r"^get_seen_questions/(?P<course_id>\d+)/(?P<amount>\d+)/$",
        views.get_seen_questions,
        name="get_seen_questions",
    ),
    re_path(
        r"^get_seen_questions/(?P<course_id>\d+)/(?P<amount>\d+)/(?P<starting_from_pk>\d+)/$",
        views.get_seen_questions,
        name="get_seen_questions",
    ),
    re_path(
        r"^get_questions/(?P<course_id>\d+)/(?P<amount>\d+)/(?P<starting_from_pk>\d+)/(?P<category>\d+)/$",
        views.get_questions,
        name="get_questions",
    ),
    re_path(
        r"^get_taken_test/(?P<course_id>\d+)/(?P<amount>\d+)/(?P<until_pk>\d+)/$",
        views.get_taken_tests,
        name="get_taken_tests",
    ),
    re_path(
        r"^get_taken_test/(?P<course_id>\d+)/(?P<amount>\d+)/$",
        views.get_taken_tests,
        name="get_taken_tests",
    ),
    # re_path(
    #     r"^eval_progsol/(?P<prog_id>\d+)/$", views.eval_progsol, name="eval_progsol"
    # ),
    # re_path(
    #     r"^progex/(?P<prog_id>\d+)/$", views.program_exercise, name="program_exercise"
    # ),
]
