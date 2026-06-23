# 🚌 Cloud-Based Bus Pass System
### CodeAlpha Internship Project — Task 3

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?logo=sqlite)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![Railway](https://img.shields.io/badge/Deployed-Railway-blueviolet?logo=railway)

> A modern, cloud-hosted bus pass management system built with Python Flask.  
> Students can register, apply for bus passes, and receive QR-coded passes —  
> all managed by an admin dashboard.

🌐 **Live Demo:** [https://web-production-27923.up.railway.app/](https://web-production-27923.up.railway.app/)

---

## ✨ Features

- 🔐 **User Authentication** — Secure register & login with encrypted passwords (Bcrypt)
- 🎫 **Bus Pass Application** — Students apply for monthly, quarterly, or yearly passes
- 📊 **Student Dashboard** — View pass status, QR code, and booking history
- 🛡️ **Admin Dashboard** — Approve or reject pass requests, manage all users
- 📱 **QR Code Generation** — Each approved pass gets a unique scannable QR code
- ☁️ **Cloud Deployed** — Hosted on Railway, accessible from anywhere
- 📱 **Responsive Design** — Works on mobile, tablet, and desktop
- 🔍 **Search & Filter** — Admin can search users and filter passes by status

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Flask 3.0 |
| Database | SQLite + Flask-SQLAlchemy |
| Authentication | Flask-Login, Flask-Bcrypt |
| Frontend | HTML5, CSS3, Bootstrap 5.3 |
| QR Code | qrcode + Pillow |
| Deployment | Railway (Cloud) |

---

## 📁 Project Structure

```
CodeAlpha_CloudBasedBusPassSystem/
│
├── app.py                  # Main application entry point
├── create_admin.py         # Script to create admin account
├── requirements.txt        # Python dependencies
├── Procfile                # Railway deployment config
│
├── models/
│   ├── user.py             # User database model
│   └── bus_pass.py         # BusPass database model
│
├── routes/
│   ├── auth.py             # Login, Register, Logout
│   ├── main.py             # Home, Dashboard
│   ├── passes.py           # Apply, View bus passes
│   └── admin.py            # Admin dashboard, Approve/Reject
│
├── templates/
│   ├── base.html           # Base template (navbar, footer)
│   ├── index.html          # Landing page
│   ├── login.html          # Login page
│   ├── register.html       # Register page
│   ├── dashboard.html      # Student dashboard
│   ├── new_pass.html       # Apply for a pass
│   └── admin_dashboard.html# Admin panel
│
├── static/
│   ├── css/style.css       # Custom styles
│   └── qrcodes/            # Generated QR code images
│
├── forms/                  # WTForms (form validation)
└── utils/                  # Helper utilities
```

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/mabdesamad-gif/CodeAlpha_CloudBasedBusPassSystem.git
cd CodeAlpha_CloudBasedBusPassSystem
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

### 6. Create admin account
```bash
python create_admin.py
```

---

## 📸 Screenshots

### 🏠 Landing Page
> Modern hero section with features and how-it-works steps

### 👤 Student Dashboard
> View active passes, stats, and apply for new passes

### 🛡️ Admin Dashboard
> Approve/reject passes, view all users and statistics

---

## 🔄 How It Works

```
1. Student registers an account
        ↓
2. Student applies for a bus pass (route + duration)
        ↓
3. Admin reviews and approves the request
        ↓
4. System generates a unique QR Code for the pass
        ↓
5. Student shows QR Code when boarding the bus ✅
```

---

## ☁️ Cloud Deployment

This project is deployed on **Railway** — a cloud platform that provides:
- ✅ Automatic deployments from GitHub
- ✅ Always-on server (no sleep like Render free tier)
- ✅ Environment variable management
- ✅ Custom domain support

---

## 🔒 Security Features

- Passwords hashed with **Bcrypt** (never stored as plain text)
- Session management with **Flask-Login**
- Admin-only routes protected with custom decorators
- SQL Injection prevention via **SQLAlchemy ORM**

---

## 📦 Dependencies

```
flask
flask-sqlalchemy
flask-login
flask-bcrypt
flask-wtf
qrcode[pil]
pillow
email-validator
gunicorn
```

---

## 👨‍💻 Developer

**Abdesmad** — CodeAlpha Cloud Computing Intern

- 🌐 Live App: [https://web-production-27923.up.railway.app/](https://web-production-27923.up.railway.app/)
- 💻 GitHub: [github.com/mabdesamad-gif](https://github.com/mabdesamad-gif)

---

## 📄 License

This project was built as part of the **CodeAlpha Internship Program**.  
© 2024 CodeAlpha — All rights reserved.

---

<div align="center">
  <strong>Built with ❤️ using Python Flask & Bootstrap 5</strong><br>
  <em>CodeAlpha Cloud Computing Internship — Task 3</em>
</div>
