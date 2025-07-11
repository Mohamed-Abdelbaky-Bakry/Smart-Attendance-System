from django.db import models
from users.models import GRADE_CHOICES, Instructor
from django.utils import timezone
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    credit_hours = models.PositiveIntegerField()
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES.choices)

    def __str__(self):
        return f"{self.name} - ({self.code})"

class AcademicYear(models.Model):
    year_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'academic_year')
    

class Teaches(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('instructor', 'subject')

    def __str__(self):
        return f"{self.instructor.account.name} teaches {self.subject.name}"


class PeriodIndex(models.TextChoices):
    FIRST = '1', 'First Period'
    SECOND = '2', 'Second Period'
    THIRD = '3', 'Third Period'
    FOURTH = '4', 'Fourth Period'

class ClassSession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    instructor = models.ForeignKey('users.Instructor', on_delete=models.SET_NULL, null=True)
    period_index = models.CharField(max_length=1, choices=PeriodIndex.choices)
    weekday = models.IntegerField()
    start_date = models.DateField()
    weeks_count = models.IntegerField(default=12)

    def __str__(self):
        return f"{self.subject.name} @ {self.start_date} (Weekday {self.weekday}) till {self.weeks_count} weeks"


class SessionDate(models.Model):
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    session_date = models.DateField()

    def __str__(self):
        return f"{self.class_session.subject.name} on {self.session_date}"


class AttendanceStatus(models.TextChoices):
    PRESENT = 'present', 'Present'
    LATE = 'late', 'Late'
    ABSENT = 'absent', 'Absent'
    PENDING = 'pending', 'Pending'

class AttendanceRecord(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    session_date = models.ForeignKey(SessionDate, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=AttendanceStatus.choices, default=AttendanceStatus.PENDING)
    check_in_time = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'session_date')
