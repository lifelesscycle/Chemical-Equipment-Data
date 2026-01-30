# ChemData - Chemical Equipment Monitoring System

ChemData is a comprehensive monitoring system designed for chemical equipment data management. It features a robust Django backend with a REST API, a React-based web dashboard, and a PyQt6 desktop application for cross-platform data visualization and equipment tracking.

## Project Structure

* **`Backend/`**: Django REST Framework project handling data processing, authentication (JWT), and equipment management.
* **`Frontend (App)/`**: Desktop application built with PyQt6 for real-time monitoring and data management.
* **`Frontend (Web)/`**: Modern web dashboard built with React and Vite for accessible data visualization.

## Prerequisites

* Python 3.10+
* Node.js (for Web Frontend)
* PostgreSQL or MySQL (Optional, defaults to SQLite)

---

## Setup Instructions

### 1. Backend Setup (Django)

Navigate to the `Backend` directory and set up a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd "Backend"

```

**Database Initialization:**

```bash
python manage.py migrate
python manage.py createsuperuser  # Create an admin account
python manage.py runserver

```

### 2. Web Frontend Setup (React)

In another command prompt window navigate to the `Frontend (Web)` directory.

```bash
cd "Frontend (Web)"
npm install
npm run dev

```

The application will be available at `http://localhost:5173`.

### 3. Desktop App Setup (PyQt6)

In another command prompt window navigate to the `Frontend (App)` directory.

```bash
venv\Scripts\activate
cd "Frontend (App)"
python main.py

```

---

## Key Features

* **Authentication**: Secure login using JWT (SimpleJWT) and session-based authentication.
* **Dashboard**: Interactive data visualization using `recharts` (Web) and `matplotlib/seaborn` (Backend/Desktop).
* **Equipment Management**: Detailed tracking of chemical equipment through dedicated equipment modules.
* **Data Upload**: Support for CSV file uploads to process equipment data (supports files up to 50MB).
* **Theme Support**: Both Web and Desktop applications support Light and Dark modes.

## Tech Stack

* **Backend**: Django, Django REST Framework, Pandas, WhiteNoise (static file serving).
* **Web Frontend**: React 19, Vite, Lucide React, Recharts.
* **Desktop Frontend**: PyQt6.
* **Database**: Support for SQLite (default), PostgreSQL, and MySQL.

## License

This project is licensed under the terms of the LICENSE.txt file included in the repository.