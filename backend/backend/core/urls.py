"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import AccountViewSet,StudentViewSet,InstructorViewSet, LoginView, LogoutView
from academics.views import TeachesViewSet, DepartmentViewSet, SubjectViewSet, AcademicYearViewSet, EnrollmentViewSet, ClassSessionViewSet, SessionDateViewSet, AttendanceRecordViewSet
from s_requests.views import RequestViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'students', StudentViewSet)
router.register(r'instructors', InstructorViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'teaches', TeachesViewSet)
router.register(r'class-sessions', ClassSessionViewSet)
router.register(r'session-dates', SessionDateViewSet)
router.register(r'attendance', AttendanceRecordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', TokenObtainPairView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
