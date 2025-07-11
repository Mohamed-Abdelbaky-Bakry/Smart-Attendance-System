
from rest_framework import serializers
from .models import Department, ClassSession, AcademicYear, Subject, Enrollment, Teaches, SessionDate, AttendanceStatus, AttendanceRecord 
from users.serializers import InstructorSerializer, StudentRetriveSerializer, StudentSerializer,InstructorRetrieveSerializer 
from users.models import Instructor, Student
from .models import Subject, AcademicYear


# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at']


# Subject Serializer
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'description', 'credit_hours', 'department', 'created_at', 'grade']


class SubjectRetrieveSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = Subject
        fields = ['id', 'code', 'name', 'description', 'credit_hours', 'department', 'created_at', 'grade']


# Academic Year Serializer
class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['year_id', 'name', 'start_date', 'end_date']


class ClassSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSession
        fields = '__all__'


# Retrieve Session with full related fields
class ClassSessionRetrieveSerializer(serializers.ModelSerializer):
    subject = SubjectRetrieveSerializer(read_only=True)
    instructor = InstructorRetrieveSerializer(read_only=True)
    class Meta:
        model = ClassSession
        fields = [
            'id',
            'subject',
            'location',
            'instructor',
            'period_index'
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'subject', 'academic_year', 'enrollment_date']


class EnrollmentRetrieveSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    academic_year = AcademicYearSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'subject', 'academic_year', 'enrollment_date']

class TeachesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teaches
        fields = ['id', 'subject', 'instructor']


class TeachesRetrieveSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    instructor = InstructorSerializer(read_only=True)

    class Meta:
        model = Teaches
        fields = ['id', 'subject', 'instructor']


class SessionDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionDate
        fields = '__all__'

class SessionDateRetrieveSerializer(serializers.ModelSerializer):
    class_session = ClassSessionRetrieveSerializer(read_only=True)
    class Meta:
        model = SessionDate
        fields = '__all__'

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student = StudentRetriveSerializer(read_only=True)
    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'session_date', 'status', 'check_in_time', 'remarks']

class AttendanceRecordRetrieveSerializer(serializers.ModelSerializer):
    student = StudentRetriveSerializer(read_only=True)
    session_date = SessionDateRetrieveSerializer(read_only=True)
    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student', 'session_date', 'status', 'check_in_time', 'remarks']