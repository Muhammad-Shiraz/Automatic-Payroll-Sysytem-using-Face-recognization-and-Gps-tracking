# 🧠 AI-Powered Human Resource Information System (HRIS)

An intelligent, end-to-end **HR Management System** powered by **Face Recognition** and **GPS Tracking** to automate employee attendance, payroll processing, and leave management.  
This system replaces manual attendance processes with real-time, ML-driven validation and integrates geofencing and dashboards for complete HR automation.

---

## 🛠️ Tech Stack

- **Backend:** Python, Django  
- **AI/ML:** OpenCV, face_recognition, Scikit-learn  
- **Frontend:** HTML, CSS, Bootstrap, JavaScript (basic)  
- **Database:** MySQL  
- **Tools:** Jupyter Notebook, Git, VS Code  

---

## 📦 Features

- ✅ Face Recognition-Based Attendance  
- ✅ GPS Tracking & Geofencing Validation  
- ✅ Manual Attendance with Image Verification  
- ✅ Automated Payroll System (daily/monthly)  
- ✅ Live Dashboards for KPIs  
- ✅ Leave Management with Approvals & Notifications  
- ✅ Shift Assignment & Overtime Tracking  
- ✅ Email Notifications Integration  

---

## 📸 Face Recognition & GPS Flow

1. Employee faces are encoded and stored securely.  
2. Real-time face recognition marks attendance via webcam or uploaded image.  
3. GPS coordinates are checked for geofencing.  
4. Manual attendance outside zone is flagged for HR approval.

---

## 🧮 Payroll Automation

- Calculates salary based on working hours, overtime, and leaves.  
- Generates daily/monthly payroll records with PDF slip generation.  
- Integrated with dashboards for HR overview.

---

## 📊 Dashboards

- Employee Attendance History  
- Monthly Payroll Summary  
- Leave & Overtime Trends  
- Real-Time Insights via ECharts

---

## 📁 Project Structure (Simplified)

├── DjangoWeb/ # HR dashboard (admin logic)
├── employee_dashboard/ # Employee-facing panel
├── flask_camera_service/ # Flask face recognition API
├── attendance/ # Attendance logic
├── payroll/ # Payroll calculations
├── leave/ # Leave management
├── static/ # CSS, JS, images
├── templates/ # HTML templates
└── manage.py


---

## 🔧 How to Run

1. **Clone the repository**
```bash
git clone https://github.com/Muhammad-Shiraz/Automatic-Payroll-Sysytem-using-Face-recognization-and-Gps-tracking
cd HRIS-FaceRecognition
```
Create a virtual environment

```bash
python -m venv env
source env/bin/activate     # On Windows: env\Scripts\activate
```
Install requirements
```bash
pip install -r requirements.txt
```
Run Django server
```bash
python manage.py runserver
```
Run Flask camera service

```bash
cd flask_camera_service
python app.py
```
📚 Future Improvements
Mobile app (React Native)

Performance prediction using ML

QR code check-ins for female employees

WiFi router log integration for indoor tracking

Admin panel with audit logs

🙋‍♂️ Author
Muhammad Shiraz
📧 shirazshahzad876@gmail.com
🔗 LinkedIn
💻 GitHub
🌐 Portfolio

