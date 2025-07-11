from datetime import datetime
from academics.models import SessionDate, AttendanceRecord, AttendanceStatus
from users.models import Student
from academics.utils.time_slots import PERIOD_TIME_RANGES


def get_current_period_index():
    now = datetime.now().time()
    for index, (start, end) in PERIOD_TIME_RANGES.items():
        if start <= now <= end:
            return index
    return None


def get_active_session_date():
    today = datetime.today().date()
    period_index = get_current_period_index()
    if not period_index:
        return None

    return SessionDate.objects.filter(
        session_date=today,
        class_session__period_index=period_index
    ).first()


def mark_attendance(student_codes):
    session_date = get_active_session_date()
    if not session_date:
        print("❌ No active session.")
        return

    for code in student_codes:
        try:
            student = Student.objects.get(student_code=code)
            record, created = AttendanceRecord.objects.get_or_create(
                student=student,
                session_date=session_date,
                defaults={'status': AttendanceStatus.PRESENT, 'check_in_time': datetime.now()}
            )
            if not created and record.status != AttendanceStatus.PRESENT:
                record.status = AttendanceStatus.PRESENT
                record.check_in_time = datetime.now()
                record.save()
            print(f"✅ Marked {student.account.name} as PRESENT")
        except Student.DoesNotExist:
            print(f"⚠ Unknown student code: {code}")
