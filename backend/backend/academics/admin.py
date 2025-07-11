from django.contrib import admin

from django.contrib import admin
from .models import (
    Department,
    Subject,
    AcademicYear,
    Enrollment,
    Teaches,
    ClassSession,
    SessionDate,
    AttendanceRecord
)

# Register your models here.
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(AcademicYear)
admin.site.register(Enrollment)
admin.site.register(Teaches)
admin.site.register(ClassSession)
admin.site.register(SessionDate)
admin.site.register(AttendanceRecord)
