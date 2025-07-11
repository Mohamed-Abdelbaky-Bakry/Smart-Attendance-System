from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AttendanceStatus, ClassSession, SessionDate, AttendanceRecord
from academics.models import Enrollment
import datetime

@receiver(post_save, sender=ClassSession)
def generate_session_dates_and_attendance(sender, instance, created, **kwargs):
    if created:
        session = instance
        start_date = session.start_date
        weekday = session.weekday
        count = session.weeks_count

        for week in range(count):
            session_day = start_date + datetime.timedelta(weeks=week)
            sd = SessionDate.objects.create(class_session=session, session_date=session_day)

            enrolled_students = Enrollment.objects.filter(subject=session.subject)
            for enrollment in enrolled_students:
                AttendanceRecord.objects.create(
                    student=enrollment.student,
                    session_date=sd,
                    status=AttendanceStatus.PENDING
                )