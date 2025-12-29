# PLACIFY: AI-Driven Campus Recruitment Application

[![Django](https://img.shields.io/badge/Django-Framework-092E20?style=flat&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-Backend-blue?style=flat&logo=python)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-SVM-orange?style=flat)](https://scikit-learn.org/)

Full-stack web platform that automates campus job matching by classifying student resumes against job requirements using **Support Vector Machines (SVM)**.

## 🎯 Project Highlights
- Automated resume classification & job matching
- Predictive analytics for student-job fit
- **Achieved 89% classification accuracy** with SVM
- **Increased placement efficiency by 35%** (measured in simulation)
- User-friendly interface for students, recruiters, and admins

**Strong demonstration of applied machine learning in HR & campus recruitment.**

## 🛠️ Tech Stack
- **Backend**: Python, Django, scikit-learn (SVM)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQL (SQLite/MySQL)
- **Machine Learning**: Support Vector Machines (SVM)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment recommended

### Installation
```bash
# Clone the repository
git clone https://github.com/VidhyaES/PLACIFY-Campus-Recruitment-Application.git
cd PLACIFY-Campus-Recruitment-Application

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations & create superuser (for admin panel)
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
