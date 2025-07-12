# Smart Attendance System using Artificial Intelligence

The project is dedicated to managing attendance and absence records for students. It tracks student attendance rates in each subject and provides instructors with insights into both overall subject attendance and individual student attendance.

## 🖼️ System Screenshots

### Mobile App
<img width="202" height="433" alt="Screenshot 2024-12-07 115327" src="https://github.com/user-attachments/assets/23b9103b-5ae8-4d14-ae67-c00bb147c78e" />
<img width="209" height="438" alt="Screenshot 2024-12-07 115405" src="https://github.com/user-attachments/assets/0e4e7c32-6433-4706-8471-dce921ee1611" />
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

##ِAI Infrastructure
The project is to detect the attendance and absence rate and solve the problem for both the doctor and the students and save time and effort as a camera is installed in the room and all it does is take a picture and identify people's faces and know the students through yolov11 and then it performs the recognition process through FaceNet any person who is not recognized and is not a student, whether it is an instructor or someone outside the classroom who does not attend by comparing the faces with the database and after he attends, he interacts with the student's application and the instructor's web and shows the results of attendance and absence and solves the problem of crowding of students in front of a camera or fingerprint and solves the problem of the QR code system and the paper system


## 🚀 Deployment Guide

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/Smart-Attendance-System/attendance-system.git

#activation
cd backend
.\venv\Scripts\Activate   

#run
python manage.py runserver
 python manage.py mark_attendance_ai --model "F:\GP\backend\backend\academics\management\commands\model.pt" --dataset "F:\GP\backend\backend\academics\management\commands\dataset1.npz" --camera "http://192.168.1.25:8080/video"

#run application
flutter pub get                                                                                                                               

