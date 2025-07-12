# Smart Attendance System using Artificial Intelligence

The project is dedicated to managing student attendance and absence records.
It tracks each student’s attendance rate per subject and provides instructors with detailed insights into both overall subject attendance and individual student participation.

A camera is installed in the classroom to automate the attendance process. It captures an image, detects faces using YOLOv11, and then uses FaceNet for face recognition. The system distinguishes between recognized students and other individuals (such as instructors or unauthorized persons) by comparing captured faces with the database.

Once attendance is confirmed, the system synchronizes with both the student mobile application and the instructor's web dashboard, displaying real-time attendance data. This approach eliminates the need for QR codes, fingerprint scanners, or paper-based systems, and helps avoid crowding and delays at classroom entrances.

## 🖼️ System Screenshots

### Mobile App
<img width="202" height="433" alt="Screenshot 2024-12-07 115327" src="https://github.com/user-attachments/assets/23b9103b-5ae8-4d14-ae67-c00bb147c78e" />
<img width="245" height="538" alt="Screenshot 2024-12-07 184908" src="https://github.com/user-attachments/assets/a07bdcc2-16fd-409a-a0c7-0454bb2883aa" />
<img width="245" height="542" alt="Screenshot 2024-12-07 184917" src="https://github.com/user-attachments/assets/cb742984-9a7e-4433-9018-13390b97326c" />
<img width="245" height="530" alt="Screenshot 2024-12-07 184924" src="https://github.com/user-attachments/assets/b517d719-0a12-40f4-bfa9-44d41834566c" />
<img width="244" height="534" alt="Screenshot 2024-12-07 184934" src="https://github.com/user-attachments/assets/d0660e2e-c7c4-4110-b330-f222c87cecf8" />
<img width="247" height="538" alt="Screenshot 2024-12-07 184941" src="https://github.com/user-attachments/assets/a0c3cc02-ba7c-4e70-8484-2b8c467f78b1" />
<img width="245" height="533" alt="Screenshot 2024-12-07 185004" src="https://github.com/user-attachments/assets/4f83afbb-0278-4171-a35e-672a3ac1eb6b" />


### Web Portal
![WhatsApp Image 2025-06-23 at 01 36 57_2f19f5a5](https://github.com/user-attachments/assets/7e71451d-86cc-49c4-8ebf-82d7104ef938)
![WhatsApp Image 2025-06-23 at 01 39 51_2522a6ff](https://github.com/user-attachments/assets/efb85b53-9c7a-4d32-92fe-1a8dd4df4d3a)
![WhatsApp Image 2025-06-23 at 01 32 41_3acbda3d](https://github.com/user-attachments/assets/cb95cff9-1b25-4502-a501-7cfdf4e1977d)
![WhatsApp Image 2025-06-23 at 01 37 39_5a62ab60](https://github.com/user-attachments/assets/3254aea5-ff85-47a6-a30c-989c3b7fbcd0)
![WhatsApp Image 2025-06-23 at 01 40 45_b7f26c2f](https://github.com/user-attachments/assets/82872935-2045-4b21-971a-2f360e9b954f)
![WhatsApp Image 2025-06-23 at 01 41 57_4f9b3129](https://github.com/user-attachments/assets/1a2c9f46-9254-42ac-ad5c-2072028b2016)


## 🛠 Technology Stack

### Frontend
| Platform | Technologies |
|----------|--------------|
| Mobile | Flutter, Dart, Provider, HTTP |
| Web | Django Templates, HTML5, CSS3, JavaScript, Chart.js |

### Backend
| Component | Technologies |
|-----------|--------------|
| Core API | Django REST Framework |
| Database | PostgreSQL |
| AI Service | Python, OpenCV,YoloV11, FaceNet |

## 🚀 Installation Guide

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/Smart-Attendance-System/attendance-system.git

#activation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#migration
cd backend
python manage.py makemigrations 
python manage.py migrate
python manage.py runserver

#run 
python manage.py mark_attendance_ai --model "F:\GP\backend\backend\academics\management\commands\model.pt" --dataset "F:\GP\backend\backend\academics\management\commands\dataset1.npz" --camera "http://192.168.1.25:8080/video"
```
### Application Setup
```bash
flutter pub get
```
                                                                                                                            

