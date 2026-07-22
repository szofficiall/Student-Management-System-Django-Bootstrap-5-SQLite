from django.contrib import admin
from django.urls import path
from student.views import *

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", home_page, name="home_page"),
    path("about_page/", about_page, name="about_page"),
    path("contact_page/", contact_page, name="contact_page"),
    path("login_page/", login_page, name="login_page"),
    path("signup_page/", signup_page, name="signup_page"),
    path("student_view/", student_view, name="student_view"),
    path("student_result/<str:student_id>/", student_result, name="student_result"),
    path(
        "student_result/<str:student_id>/pdf/",
        download_result_pdf,
        name="download_result_pdf",
    ),
    path("logout/", logout_page, name="logout_page"),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
