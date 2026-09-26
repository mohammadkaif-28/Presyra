# Presyra 🎓

### AI-Powered Multimodal Student Attendance System

Presyra is an AI-powered student attendance management system that
combines **face recognition** and **voice recognition** to automate and
simplify attendance management in educational environments.

The system provides separate experiences for **teachers and students**,
allowing teachers to manage subjects and attendance while students can
register their profiles, enroll in subjects, and view their attendance
statistics.

------------------------------------------------------------------------

## ✨ Features

### 👨‍🏫 Teacher Features

-   Teacher registration
-   Secure password hashing using bcrypt
-   Teacher login
-   Create and manage subjects
-   Generate/share subject codes
-   View enrolled students
-   Take attendance
-   View attendance records
-   View attendance statistics

### 👨‍🎓 Student Features

-   Student registration
-   Face-based student registration
-   Optional voice enrollment
-   Face recognition
-   Voice recognition
-   Student login
-   Enroll in subjects
-   Unenroll from subjects
-   View enrolled subjects
-   View attendance statistics

### 🤖 AI Features

-   Face embedding generation
-   Face recognition
-   Voice embedding generation
-   Voice-based recognition
-   Multimodal attendance system
-   Machine-learning based face classification

### ☁️ Backend & Database

-   Supabase integration
-   PostgreSQL database
-   Student face embeddings stored as JSONB
-   Student voice embeddings stored as JSONB
-   Teacher-subject relationships
-   Student-subject many-to-many relationships
-   Attendance logging

### 🐳 Deployment

-   Docker support
-   Python 3.12 environment
-   CPU-based PyTorch
-   Containerized application environment

------------------------------------------------------------------------

# 🧠 How Presyra Works

``` text
                 ┌─────────────────────┐
                 │       Presyra       │
                 │   Streamlit App     │
                 └──────────┬──────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
      ┌──────────────┐             ┌──────────────┐
      │ Face Pipeline│             │ Voice Pipeline│
      └──────┬───────┘             └──────┬───────┘
             │                             │
             ▼                             ▼
      Face Embeddings              Voice Embeddings
             │                             │
             └──────────────┬──────────────┘
                            │
                            ▼
                    Student Recognition
                            │
                            ▼
                    Attendance System
                            │
                            ▼
                     Supabase Database
```

------------------------------------------------------------------------

# 🛠️ Technology Stack

  Technology                Purpose
  ------------------------- ------------------------------------
  Python                    Core programming language
  Streamlit                 Web application framework
  NumPy                     Numerical processing
  Pandas                    Data processing
  Scikit-learn              Machine learning
  dlib                      Face detection and face processing
  face_recognition_models   Face recognition model
  PyTorch                   Deep learning / voice processing
  Resemblyzer               Voice embeddings
  Librosa                   Audio processing
  Pillow                    Image processing
  Supabase                  Backend database
  PostgreSQL                Database engine
  bcrypt                    Password hashing
  Segno                     QR code generation
  Docker                    Containerization

------------------------------------------------------------------------

# 📁 Project Structure

``` text
Presyra/
│
├── app.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── README.md
│
├── docker_packages/
│   └── face_recognition_models-0.3.0.tar.gz
│
├── .streamlit/
│   └── config.toml
│
└── src/
    ├── components/
    ├── database/
    │   ├── config.py
    │   ├── db.py
    │   └── schema.sql
    ├── pipelines/
    │   ├── face_pipeline.py
    │   └── voice_pipeline.py
    ├── screens/
    │   ├── home_screen.py
    │   ├── teacher_screen.py
    │   └── student_screen.py
    └── ui/
```

> The exact contents of individual folders may change as the project
> evolves.

------------------------------------------------------------------------

# 🚀 Getting Started

There are two ways to run Presyra:

1.  🐳 Docker --- Recommended
2.  🐍 Local Python environment

------------------------------------------------------------------------

# ☁️ 1. Supabase Database Setup

Presyra uses **Supabase** as its backend database.

Before running the application, create your own Supabase project.

## Step 1 --- Create a Supabase Project

Create a new project in Supabase.

## Step 2 --- Open SQL Editor

``` text
Supabase Dashboard
        ↓
SQL Editor
        ↓
New Query
```

## Step 3 --- Create Database Tables

Open `src/database/schema.sql`, copy the SQL code, and run it in the
Supabase SQL Editor.

The schema creates:

``` text
teachers
students
subjects
subject_students
attendance_logs
```

------------------------------------------------------------------------

# 🗄️ Database Structure

``` text
                    teachers
                       │
                       ▼
                    subjects
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
      subject_students     attendance_logs
              │                 │
              ▼                 ▼
           students          students
```

### Teachers

Stores `teacher_id`, `username`, `password`, and `name`. Passwords are
hashed using bcrypt before being stored.

### Students

Stores `student_id`, `name`, `face_embedding`, and `voice_embedding`.
Face and voice embeddings are stored as JSONB values.

### Subjects

Stores `subject_id`, `subject_code`, `name`, `section`, and
`teacher_id`.

### Subject Students

Manages the many-to-many relationship between students and subjects
using `subject_id` and `student_id`.

### Attendance Logs

Stores `id`, `timestamp`, `subject_id`, `student_id`, and `is_present`.
The timestamp is stored as PostgreSQL `TIMESTAMPTZ`.

------------------------------------------------------------------------

# 🔐 2. Configure Supabase Credentials

Create the following file locally:

``` text
.streamlit/secrets.toml
```

Add:

``` toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-key"
```

Never upload `.streamlit/secrets.toml` to GitHub. Never commit `.env`,
`.env.*`, private API keys, passwords, tokens, or credentials.

------------------------------------------------------------------------

# 🐳 3. Run with Docker --- Recommended

## Step 1 --- Clone the Repository

``` bash
git clone https://github.com/YOUR_USERNAME/Presyra.git
cd Presyra
```

## Step 2 --- Create Supabase Secrets

Create `.streamlit/secrets.toml` with your own credentials.

## Step 3 --- Build Docker Image

``` bash
docker build -t presyra .
```

The first build may take some time because Presyra uses machine-learning
and computer-vision dependencies.

## Step 4 --- Run the Container

### Windows PowerShell

``` powershell
docker run --rm -p 8501:8501 `
  -v "${PWD}\.streamlit\secrets.toml:/app/.streamlit/secrets.toml:ro" `
  presyra
```

## Step 5 --- Open Presyra

Open `http://localhost:8501`.

------------------------------------------------------------------------

# 🐍 4. Run Without Docker

Presyra is configured for **Python 3.12**.

``` powershell
python --version
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml` before starting the app.

------------------------------------------------------------------------

# 📱 Mobile Testing

Run:

``` powershell
streamlit run app.py
```

Streamlit will display a Network URL similar to
`http://192.168.x.x:8501`. Open that URL from another device on the same
network.

## 📷 Camera Access

Make sure camera permission is allowed, the browser supports camera
access, the device can reach the application, and the deployment
environment provides the required secure connection. Some browsers
require HTTPS for camera access in non-localhost environments.

------------------------------------------------------------------------

# 👨‍🏫 Teacher Workflow

``` text
Teacher Registration
        ↓
Teacher Login
        ↓
Create Subject
        ↓
Share Subject Code
        ↓
Students Enroll
        ↓
Take Attendance
        ↓
View Attendance Records
```

# 👨‍🎓 Student Workflow

``` text
Student Registration
        ↓
Capture Face
        ↓
Optional Voice Enrollment
        ↓
Student Profile Created
        ↓
Face Recognition Login
        ↓
Enroll in Subject
        ↓
Attendance
        ↓
View Attendance Statistics
```

------------------------------------------------------------------------

# 🤖 Face Recognition Pipeline

``` text
Camera Image
      ↓
Face Detection
      ↓
Face Feature Extraction
      ↓
Face Embedding
      ↓
Student Matching
      ↓
Recognition Result
```

During student registration, the face embedding is stored in the
database.

# 🎙️ Voice Recognition Pipeline

``` text
Audio Input
     ↓
Audio Processing
     ↓
Voice Embedding
     ↓
Student Matching
     ↓
Recognition Result
```

Voice enrollment is optional during student registration.

------------------------------------------------------------------------

# 🔑 Authentication

Teacher passwords are not stored as plain text. Presyra uses bcrypt
password hashing.

``` text
Password → bcrypt hashing → Hashed Password → Supabase
```

------------------------------------------------------------------------

# 🕒 Attendance Timestamp

Attendance records use database timestamps. The database stores
timestamps using PostgreSQL `TIMESTAMPTZ`, and the application converts
timestamps for display where required.

------------------------------------------------------------------------

# 🧪 Testing Checklist

## Teacher

-   [ ] Teacher registration works
-   [ ] Teacher login works
-   [ ] Password validation works
-   [ ] Subject creation works
-   [ ] Subject code sharing works
-   [ ] Attendance can be taken
-   [ ] Attendance records are displayed

## Student

-   [ ] Student registration works
-   [ ] Camera access works
-   [ ] Face embedding is generated
-   [ ] Student profile is created
-   [ ] Optional voice enrollment works
-   [ ] Student login works
-   [ ] Subject enrollment works
-   [ ] Student attendance is displayed
-   [ ] Attendance statistics are displayed

## Database

-   [ ] Supabase project is connected
-   [ ] All required tables exist
-   [ ] Teacher records are created
-   [ ] Student records are created
-   [ ] Subjects are created
-   [ ] Student-subject enrollment works
-   [ ] Attendance records are inserted

------------------------------------------------------------------------

# 🛠️ Troubleshooting

## `StreamlitSecretNotFoundError`

Make sure `.streamlit/secrets.toml` exists and contains valid Supabase
credentials.

## Docker Container Starts but Supabase Does Not Work

Check the Supabase URL, API key, `secrets.toml` location, database
tables, and database permissions.

## Camera Is Not Working

Check browser camera permission, operating-system camera permission, the
URL, network connectivity, and HTTPS requirements for remote camera
access.

## Docker Build Takes a Long Time

Presyra contains machine-learning and computer-vision dependencies such
as PyTorch, dlib, SciPy, NumPy, Librosa, and Resemblyzer. Therefore, the
first Docker build can take several minutes.

------------------------------------------------------------------------

# 🔒 Security Recommendations

For production deployments:

-   Never expose Supabase service-role keys in the frontend.
-   Never commit secrets to GitHub.
-   Use environment variables or secret managers.
-   Use strong teacher passwords.
-   Enable appropriate Supabase Row Level Security policies.
-   Review database permissions before public deployment.
-   Avoid storing unnecessary sensitive biometric information.
-   Protect database backups and exported embeddings.

------------------------------------------------------------------------

# 📌 Important Notes

Presyra is an AI/ML-based attendance project intended for educational,
research and development purposes.

The system processes biometric-related information such as face and
voice embeddings. Deployers should ensure that their use of such
information follows applicable privacy, security, consent, and
data-protection requirements.

------------------------------------------------------------------------

# 🚧 Future Improvements

-   Improved face recognition accuracy
-   Advanced voice verification
-   Better anti-spoofing mechanisms
-   Liveness detection
-   Role-based database access
-   Advanced attendance analytics
-   Attendance reports and exports
-   Email notifications
-   Cloud deployment
-   Production-grade authentication
-   Improved mobile experience
-   Automated testing
-   CI/CD pipeline

------------------------------------------------------------------------

# 🤝 Contributing

Contributions are welcome.

``` bash
git clone https://github.com/mohammadkaif-28/Presyra.git
cd Presyra
git checkout -b feature/your-feature

# Make your changes
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a Pull Request on GitHub.

------------------------------------------------------------------------

# 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

------------------------------------------------------------------------

# 👨‍💻 Author

## MD Kaif

MCA --- Generative AI

Interested in: - Artificial Intelligence - Machine Learning - Deep
Learning - Generative AI - Computer Vision - AI Engineering

------------------------------------------------------------------------

# ⭐ Support

If you find Presyra useful, consider giving the repository a ⭐ on
GitHub.

------------------------------------------------------------------------

## Presyra

**AI-powered attendance for modern classrooms.**

Built with ❤️ using Python, Streamlit, AI/ML and Supabase.
