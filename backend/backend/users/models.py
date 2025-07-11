from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class AccountManager(BaseUserManager):
    def create_user(self, email, name, password=None, role='student', **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        if not name:
            raise ValueError("The Name field is required")
        if role not in ['admin', 'instructor', 'student']:
            raise ValueError("Role must be one of: admin, instructor, student")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.pop('role', None)
        return self.create_user(email=email, name=name, password=password, role='admin', **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    objects = AccountManager()

    def __str__(self):
        return f"{self.name} ({self.role})"

class GRADE_CHOICES(models.TextChoices):
    FIRST = '1', 'First'
    SECOND = '2', 'Second'
    THIRD = '3', 'Third'
    FOURTH = '4', 'Fourth'

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'M'),
        ('Female', 'F'),
    ]

    account = models.OneToOneField(
        Account,
        primary_key=True,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='student_profile'
    )
    student_code = models.CharField(unique=True, max_length=20)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_CHOICES)
    address = models.TextField(blank=True, null=True)
    enrollment_date = models.DateField()
    department = models.ForeignKey("academics.Department", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES.choices)

    def __str__(self):
        return f"{self.account.name} - {self.student_code}"


class Instructor(models.Model):
    account = models.OneToOneField(
        Account,
        primary_key=True,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'instructor'},
        related_name='instructor_profile'
    )
    department = models.ForeignKey("academics.Department", on_delete=models.SET_NULL, null=True)
    hire_date = models.DateField()

    def __str__(self):
        return self.account.name