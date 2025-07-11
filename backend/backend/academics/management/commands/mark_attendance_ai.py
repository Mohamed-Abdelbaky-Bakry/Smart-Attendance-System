import os
import time
import cv2
import torch
import datetime
import numpy as np
import pytz  # ← ✅ لإدارة الـ time zone
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware, is_naive
from ultralytics import YOLO
from facenet_pytorch import InceptionResnetV1
from users.models import Student
from academics.models import (
    AttendanceRecord, AttendanceStatus, SessionDate, PeriodIndex, Enrollment
)

class Command(BaseCommand):
    help = 'Run AI attendance and mark students present'

    def add_arguments(self, parser):
        parser.add_argument('--model', type=str, required=True, help='Path to YOLO model')
        parser.add_argument('--dataset', type=str, required=True, help='Path to dataset .npz file')
        parser.add_argument('--camera', type=str, required=True, help='IP camera stream URL')

    def handle(self, *args, **kwargs):
        model_path = kwargs['model']
        dataset_path = kwargs['dataset']
        ip_camera_url = kwargs['camera']

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(model_path)
        self.facenet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

        data = np.load(dataset_path)
        trainX, trainy = data['arr_0'], data['arr_1']
        self.student_map = {}
        trainX_processed = self.preprocess_faces(trainX)
        train_embeddings = self.get_embeddings(trainX_processed)

        for label, embedding in zip(trainy, train_embeddings):
            self.student_map[label] = embedding

        # ✅ عرض الطلاب المحملين
        print("\n📋 Loaded Student Codes:")
        for label in self.student_map:
            try:
                student = Student.objects.get(student_code=label)
                print(f"🔹 {label} → {student.account.name}")
            except Student.DoesNotExist:
                print(f"⚠️ {label} → Unknown student (not in DB)")

        cap = cv2.VideoCapture(ip_camera_url)
        if not cap.isOpened():
            self.stdout.write(self.style.ERROR("Can't connect to camera"))
            return

        last_saved = time.time()

        # ✅ تحديد توقيت القاهرة
        egypt_tz = pytz.timezone('Africa/Cairo')
        now = datetime.datetime.now(egypt_tz)
        today = now.date()
        period_index = self.detect_current_period(now.time())

        print(f"🕓 Current time: {now.time()}")
        print(f"🕓 Detected period: {period_index}")

        while True:
            ret, frame = cap.read()
            if not ret:
                self.stdout.write("❗️ Failed to read from camera")
                time.sleep(2)
                continue

            if time.time() - last_saved >= 10:
                timestamp = datetime.datetime.now(egypt_tz).strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join("captured_frames", f"frame_{timestamp}.jpg")
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                cv2.imwrite(save_path, frame)
                self.stdout.write(f"💾 Saved frame at {save_path}")
                last_saved = time.time()

                recognized_students = self.recognize_faces(frame)
                print(f"⚠️ {recognized_students} is recognized.")

                for student_code in recognized_students:
                    try:
                        student = Student.objects.get(student_code=student_code)
                    except Student.DoesNotExist:
                        self.stdout.write(f"⚠ Unknown student code: {student_code}")
                        continue

                    now = datetime.datetime.now(egypt_tz)
                    today = now.date()
                    period_index = self.detect_current_period(now.time())
                    if not period_index:
                        continue

                    subject_ids = Enrollment.objects.filter(student=student).values_list("subject", flat=True)

                    try:
                        session_date = SessionDate.objects.get(
                            session_date=today,
                            class_session__period_index=period_index,
                            class_session__subject__in=subject_ids
                        )
                    except SessionDate.DoesNotExist:
                        self.stdout.write(f"🟡 No session for {student_code} today {today} at period {period_index}")
                        continue

                    check_in_time = now if not is_naive(now) else make_aware(now)

                    record, created = AttendanceRecord.objects.get_or_create(
                        student=student,
                        session_date=session_date,
                        defaults={
                            'status': AttendanceStatus.PRESENT,
                            'check_in_time': check_in_time
                        }
                    )
                    if not created and record.status != AttendanceStatus.PRESENT:
                        record.status = AttendanceStatus.PRESENT
                        record.check_in_time = check_in_time
                        record.save()

                    self.stdout.write(self.style.SUCCESS(f"✅ Marked {student_code} as present"))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def extract_faces(self, image, required_size=(160, 160)):
        results = self.model(image)
        faces = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                face = image[int(y1):int(y2), int(x1):int(x2)]
                if face.shape[0] > 0 and face.shape[1] > 0:
                    resized = cv2.resize(face, required_size)
                    faces.append(resized)
        return faces

    def preprocess_faces(self, faces):
        tensors = []
        for face in faces:
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            tensor = torch.tensor(face_rgb).permute(2, 0, 1).float() / 255.0
            tensors.append(tensor.unsqueeze(0))
        return torch.cat(tensors).to(self.device)

    def get_embeddings(self, face_tensor):
        with torch.no_grad():
            return self.facenet(face_tensor).cpu().numpy()

    def recognize_faces(self, frame):
        faces = self.extract_faces(frame)
        if not faces:
            return []

        tensor = self.preprocess_faces(faces)
        embeddings = self.get_embeddings(tensor)
        recognized = []

        for emb in embeddings:
            best_match = None
            best_dist = float('inf')
            for student_code, ref_emb in self.student_map.items():
                dist = np.linalg.norm(emb - ref_emb)
                if dist < 0.9 and dist < best_dist:
                    best_dist = dist
                    best_match = student_code
            if best_match:
                recognized.append(best_match)

        return recognized

    def detect_current_period(self, current_time):
        periods = {
            PeriodIndex.FIRST: (datetime.time(0, 15), datetime.time(10, 45)),
            PeriodIndex.SECOND: (datetime.time(11, 0), datetime.time(12, 30)),
            PeriodIndex.THIRD: (datetime.time(13, 0), datetime.time(14, 30)),
            PeriodIndex.FOURTH: (datetime.time(15, 0), datetime.time(16, 30)),
        }

        for period, (start, end) in periods.items():
            if start <= current_time <= end:
                return period
        return None

    # For testing
    def detect_current_period_test(self, current_time):
        from datetime import time
        periods = {
            PeriodIndex.FIRST: (time(19, 0), time(19, 20)),  # تجريبي
            PeriodIndex.SECOND: (time(0, 0), time(1, 0)),
            PeriodIndex.THIRD: (time(23, 0), time(23, 59)),
            PeriodIndex.FOURTH: (time(0, 0), time(1, 0)),
        }

        for period, (start, end) in periods.items():
            if start <= current_time <= end:
                return period
        return None
