# Smart Attendance System

![System Architecture](assets/system-architecture.png) <!-- Add architecture diagram -->

A full-stack attendance management solution featuring:
- **📱 Mobile App** (Flutter) for students/instructors
- **🖥️ Web Portal** (Django Admin + Custom UI) for administrators
- **🧠 AI Engine** for facial recognition attendance
- **📊 Real-time Analytics Dashboard**

## 🌟 Key Features

### Mobile Application
- 👥 Role-based access (Student/Instructor/Admin)
- 📅 Interactive class schedules
- 🤖 Face recognition attendance marking
- 📈 Personalized attendance reports
- 📝 Digital leave applications
- 🔔 Push notifications

### Web Portal
- 👨‍💼 Admin dashboard with system oversight
- 👥 User management interface
- 📚 Course/subject configuration
- 📊 Comprehensive analytics
- ⚙️ System configuration

### Backend Services
- 🔐 Secure JWT authentication
- 📱 Mobile API endpoints
- 🌐 Web admin interfaces
- 🤖 AI processing microservice
- 📦 PostgreSQL database

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
| AI Service | Python, OpenCV, FaceNet |
| Web Server | Nginx, Gunicorn |

### DevOps
| Area | Tools |
|------|-------|
| Containerization | Docker |
| CI/CD | GitHub Actions |

## 🖼️ System Screenshots

### Mobile App
<img width="202" height="433" alt="Screenshot 2024-12-07 115327" src="https://github.com/user-attachments/assets/8b9bc845-1317-4981-babc-fab5891ae8e6" />
<img width="247" height="538" alt="Screenshot 2024-12-07 184941" src="https://github.com/user-attachments/assets/174cfd7c-8a83-4645-bca0-dfd2758ce2bb" />
<img width="244" height="534" alt="Screenshot 2024-12-07 184934" src="https://github.com/user-attachments/assets/288f7fb0-ba36-431b-b818-7c671b8de10a" />
<img width="245" height="530" alt="Screenshot 2024-12-07 184924" src="https://github.com/user-attachments/assets/43933cfe-5590-49e9-a99d-9aca4c53ee8c" />
<img width="245" height="542" alt="Screenshot 2024-12-07 184917" src="https://github.com/user-attachments/assets/fcaadce1-8bd6-4233-898f-58f896d1ab36" />
<img width="245" height="538" alt="Screenshot 2024-12-07 184908" src="https://github.com/user-attachments/assets/cf8d91d8-cf26-4931-ae47-95ffceab42c8" />
<img width="209" height="438" alt="Screenshot 2024-12-07 115405" src="https://github.com/user-attachments/assets/885d2d23-130a-43be-b468-145c6f2bbebe" />
<img width="245" height="533" alt="Screenshot 2024-12-07 185004" src="https://github.com/user-attachments/assets/d9a16e28-dcdf-4e4e-bb40-0d63801db1c8" />


### Web Portal
![WhatsApp Image 2025-06-23 at 01 56 28_35214748](https://github.com/user-attachments/assets/78c11d6f-0e97-4bce-b70e-1638edcce6e4)
![WhatsApp Image 2025-06-23 at 01 41 57_4f9b3129](https://github.com/user-attachments/assets/22e43960-8979-43c6-b4cd-322d60933ff0)
![WhatsApp Image 2025-06-23 at 01 40 45_b7f26c2f](https://github.com/user-attachments/assets/c0502230-138c-456a-8ea7-f1e1219d37f8)
![WhatsApp Image 2025-06-23 at 01 39 51_2522a6ff](https://github.com/user-attachments/assets/b591f7ac-51fb-4bad-b466-689672218081)
![WhatsApp Image 2025-06-23 at 01 37 39_5a62ab60](https://github.com/user-attachments/assets/fc41d3c7-a9d1-4add-b57d-8c24676a2ac1)
![WhatsApp Image 2025-06-23 at 01 36 57_2f19f5a5](https://github.com/user-attachments/assets/2d667a80-a707-44fe-bb8b-9b726cb6eb81)
![WhatsApp Image 2025-06-23 at 01 32 41_3acbda3d](https://github.com/user-attachments/assets/607e3fa1-8678-4a36-a7cb-8beebefd2ebd)


## 🚀 Deployment Guide

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/Smart-Attendance-System/attendance-system.git
cd attendance-system

# Start services using Docker
docker-compose up -d

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

