import os
from datetime import datetime
import cv2
import numpy as np
import torch
import time
from ultralytics import YOLO
from facenet_pytorch import InceptionResnetV1
import django
import os
from academics.utils.attendance_logic import mark_attendance

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # ✴️ استبدل your_project_name باسم مشروعك
django.setup()

class IPCameraAttndanceSystem:

    def __init__(self, model_path, dataset_path, ip_camera_url):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")

        self.model = YOLO(model_path)
        self.facenet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
        print("Models loaded successfully")

        data = np.load(dataset_path)
        trainX, trainy = data['arr_0'], data['arr_1']
        trainX_processed = self.preprocess_faces(trainX)

        if trainX_processed is None:
            raise ValueError("Failed to preprocess training faces")

        train_embeddings = self.get_embeddings(self.facenet, trainX_processed)
        if train_embeddings is None:
            raise ValueError("Failed to generate training embeddings")

        unique_labels = np.unique(trainy)
        self.student_embeddings = {
            label: np.mean(train_embeddings[np.where(trainy == label)[0]], axis=0)
            for label in unique_labels
        }
        self.expected_students = list(unique_labels)
        print(f"Loaded dataset with {len(unique_labels)} students")

        self.ip_camera_url = ip_camera_url

    def extract_faces(self, image, required_size=(160, 160)):
        results = self.model(image)
        faces = []
        face_images = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                face = image[y1:y2, x1:x2]
                if face.shape[0] > 0 and face.shape[1] > 0:
                    resized_face = cv2.resize(face, required_size)
                    faces.append(resized_face)
                    face_images.append(face)
        return faces, face_images

    def preprocess_faces(self, faces):
        try:
            processed_faces = []
            for face in faces:
                face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face_tensor = torch.tensor(face_rgb).permute(2, 0, 1).float() / 255.0
                face_tensor = face_tensor.unsqueeze(0)
                processed_faces.append(face_tensor)
            return torch.cat(processed_faces).to(self.device) if processed_faces else None
        except Exception as e:
            print(f"Face preprocessing error: {str(e)}")
            return None

    def get_embeddings(self, model, faces_tensor):
        try:
            with torch.no_grad():
                embeddings = model(faces_tensor)
            return embeddings.cpu().numpy()
        except Exception as e:
            print(f"Embedding generation error: {str(e)}")
            return None

    def recognize_faces(self, image, threshold=0.7):
        faces, _ = self.extract_faces(image)
        if not faces:
            return [], []

        faces_tensor = self.preprocess_faces(faces)
        if faces_tensor is None:
            return [], []

        embeddings = self.get_embeddings(self.facenet, faces_tensor)
        if embeddings is None:
            return [], []

        recognized_students = []
        for embedding in embeddings:
            min_dist = float('inf')
            recognized_student = "Unknown"
            for student, ref_embedding in self.student_embeddings.items():
                dist = np.linalg.norm(embedding - ref_embedding)
                if dist < min_dist:
                    min_dist = dist
                    recognized_student = student
            if min_dist < threshold:
                recognized_students.append(recognized_student)

        return recognized_students, faces

    def process_frame(self, frame, output_file, capture_number):
        # ✅ Save raw image before detection
        image_save_dir = 'attendance'
        os.makedirs(image_save_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_path = os.path.join(image_save_dir, f"capture_{capture_number}_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)

        recognized_students, _ = self.recognize_faces(frame)
        present_students = list(set([s for s in recognized_students if s != "Unknown"]))
        mark_attendance(present_students)
        with open(output_file, 'a') as f:
            for student in present_students:
                f.write(f"{student}\n")

        return {'present_students': present_students} if present_students else None

    def generate_final_report(self, attendance_data, output_file):
        present_students = set()
        for data in attendance_data:
            if data:
                present_students.update(data['present_students'])

        with open(output_file, 'w') as f:
            for student in sorted(present_students):
                f.write(f"{student}\n")

        print("Final report with only student IDs generated.")

    def run(self, output_dir='attendance_logs', capture_interval=15*60, session_duration=90*60):
        os.makedirs(output_dir, exist_ok=True)
        session_count = 1

        while True:
            output_file = os.path.join(output_dir, f"attendance_session_{session_count}.txt")
            open(output_file, 'w').close()

            cap = cv2.VideoCapture(self.ip_camera_url)
            if not cap.isOpened():
                print(f"❌ Failed to connect to camera: {self.ip_camera_url}")
                return

            attendance_data = []
            last_capture = time.time()
            session_start = time.time()
            capture_number = 0

            print(f"\n📹 Starting session {session_count}...")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("⚠ Camera read failed. Retrying...")
                    time.sleep(2)
                    continue

                cv2.imshow("Live Feed", frame)
                current_time = time.time()

                if current_time - last_capture > capture_interval:
                    last_capture = current_time
                    print(f"📸 Capturing frame {capture_number}")
                    data = self.process_frame(frame, output_file, capture_number)
                    if data:
                        attendance_data.append(data)
                    capture_number += 1

                if current_time - session_start > session_duration:
                    print(f"\n⏰ Session {session_count} finished. Generating report...")
                    break

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("🛑 Exiting manually.")
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            cap.release()
            cv2.destroyAllWindows()
            self.generate_final_report(attendance_data, output_file)

            print(f"✅ Attendance saved to: {output_file}")
            print("🔁 Restarting for next session in 10 seconds...\n")

            session_count += 1
            time.sleep(15 * 60)

# --- Main Config ---
MODEL_PATH = r"C:\Users\Mosal\Downloads\model.pt"
DATASET_PATH = r"C:\Graduation Project\dataset1.npz"
IP_CAMERA_URL = 0

if __name__ == "__main__":
    try:
        system = IPCameraAttendanceSystem(MODEL_PATH, DATASET_PATH, IP_CAMERA_URL)
        system.run(capture_interval=15*60)  # Adjust interval as needed
    except Exception as e:
        print(f"Startup error: {str(e)}")