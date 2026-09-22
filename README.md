# 🎓 Course Selling Platform

A **Django-based online learning platform** where people can create, sell, and purchase courses.

The idea is simple: if you have knowledge about something — **AI, web development, LinkedIn customization, web design, programming, career development, or any other skill** — you can share that knowledge with others by creating courses and getting paid for your work.

At the same time, learners can discover courses, purchase them, save them to their wishlist, and learn from structured course content.

---

## 🚀 Project Overview

This project is built with:

* **Backend:** Django / Python
* **Frontend:** HTML / CSS
* **Database:** SQLite
* **Authentication:** Django Authentication
* **Course Management:** Django Models & ORM
* **Package Manager:** uv

My main focus in this project was building a **strong backend architecture** and implementing realistic relationships between users, courses, sections, lectures, purchases, feedback, ratings, and wishlists.

---

## 🎯 Main Features

### 👤 User Management

Users can:

* Create an account
* Log in and log out
* Manage their profile
* Create their own courses
* Update their courses
* Delete their courses
* Purchase courses
* Save courses to their wishlist
* Access purchased courses
* Leave feedback on purchased courses
* Rate purchased courses

---

### 📚 Course Management

Course creators can build complete courses.

A course can contain multiple sections:

```text
Course
│
├── Section 1
│   ├── Lecture 1
│   ├── Lecture 2
│   └── Lecture 3
│
├── Section 2
│   ├── Lecture 1
│   ├── Lecture 2
│   └── Lecture 3
│
└── Section 3
    └── Lecture 1
```

This structure allows instructors to organize their knowledge into a clear learning path.

---

## 🎥 Lecture System

Each section can contain multiple lectures.

A lecture can contain different types of learning material, such as:

* 🎥 Video
* 📄 PDF
* 🖼️ Image
* 📝 Other learning resources

The instructor can upload the required material and use the lecture to teach students.

Example:

```text
Python Course
│
├── Introduction
│   ├── What is Python? → Video
│   ├── Python Installation → PDF
│   └── First Python Program → Video
│
├── Python Basics
│   ├── Variables → Video
│   ├── Data Types → PDF
│   └── Exercises → PDF
│
└── Advanced Python
    ├── OOP → Video
    └── Advanced Exercises → PDF
```

---

## 🛒 Course Purchasing

Students can purchase courses from instructors.

After purchasing a course, the student can access its learning content and provide feedback or a rating.

The general workflow is:

```text
Instructor
    ↓
Creates Course
    ↓
Course
    ↓
Sections
    ↓
Lectures
    ↓
Student purchases Course
    ↓
Student learns
    ↓
Student gives Feedback / Rating
```

---

## ❤️ Wishlist

Users can save courses they are interested in to their wishlist.

This allows them to come back later and decide whether they want to purchase the course.

```text
Browse Courses
      ↓
Interesting Course
      ↓
Add to Wishlist
      ↓
Come Back Later
      ↓
Purchase Course
```

---

## 🧠 Recommendation System

The platform also contains a **course recommendation system**.

The recommendation system analyzes information about the user and courses and uses information-retrieval techniques to find relevant courses.

One of the algorithms used in the project is **BM25**.

The general process is:

```text
User Information
      ↓
Extract User Interests
      ↓
Build Course Documents
      ↓
BM25 Retrieval
      ↓
Calculate Relevance Scores
      ↓
Recommend Courses
```

This was an important part of the project because it allowed me to apply algorithms I learned in a real Django application rather than implementing them only as standalone Python programs.

---

## 🏗️ Backend Architecture

The backend is designed around Django's models and relationships.

The main relationships are approximately:

```text
User
 │
 ├───────────────┐
 │               │
 ▼               ▼
Courses        Wishlist
 │
 ├── Section
 │     │
 │     └── Lecture
 │
 └── ...

User
 │
 └── Purchases
       │
       └── Course
```

A course can have many sections, and each section can contain many lectures.

This gives the application a hierarchical structure:

```text
Course
   ↓
Section
   ↓
Lecture
   ↓
Learning Material
```

---

## 🛠️ Technologies

| Technology | Purpose                                       |
| ---------- | --------------------------------------------- |
| Python     | Backend programming                           |
| Django     | Web framework                                 |
| Django ORM | Database operations                           |
| HTML       | Frontend structure                            |
| CSS        | Frontend styling                              |
| SQLite     | Development database                          |
| Pillow     | Image processing                              |
| uv         | Python package and environment management     |
| BM25       | Course recommendation / information retrieval |

---

# ⚙️ Installation & Setup

## 📋 Requirements

Before running the project, make sure you have:

* **Python 3.14+**
* **uv**
* **Git**

The project uses `uv` to manage the Python environment and dependencies.

---

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

Replace `<YOUR_REPOSITORY_URL>` with the URL of this GitHub repository.

---

## 2. Install Dependencies

The project uses `uv` to create/manage the environment and install the dependencies.

You can run:

```bash
make install
```

This executes:

```bash
pip install uv
uv sync
```

Or manually:

```bash
pip install uv
uv sync
```

The dependencies are defined in `pyproject.toml`:

```toml
[project]
name = "udemy"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "django>=6.1.1",
    "pillow>=12.3.0"
]
```

---

## 3. Apply Database Migrations

Run:

```bash
make migrate
```

Or:

```bash
uv run python3 manage.py migrate
```

This creates the required database tables.

---

## 4. Create a Superuser

To access the Django administration panel:

```bash
make superuser
```

Or:

```bash
uv run python3 manage.py createsuperuser
```

Django will ask you for:

```text
Username:
Email address:
Password:
Password (again):
```

---

## 5. Run the Development Server

Start the Django development server:

```bash
make run
```

Or:

```bash
uv run python3 manage.py runserver
```

The website will normally be available at:

```text
http://127.0.0.1:8000/
```

The Django administration panel is available at:

```text
http://127.0.0.1:8000/admin/
```

---

# 🧰 Makefile Commands

The project includes a `Makefile` to simplify common Django commands.

| Command                     | Description                                       |
| --------------------------- | ------------------------------------------------- |
| `make install`              | Install `uv` and synchronize project dependencies |
| `make run`                  | Run the Django development server                 |
| `make add_app APP=app_name` | Create a new Django application                   |
| `make makemigrations`       | Create new database migrations                    |
| `make migrate`              | Apply database migrations                         |
| `make superuser`            | Create a Django administrator                     |
| `make clean`                | Remove `__pycache__` directories                  |
| `make help`                 | Display available commands                        |

### Run the server

```bash
make run
```

### Create a new Django app

```bash
make add_app APP=users
```

### Create migrations

```bash
make makemigrations
```

### Apply migrations

```bash
make migrate
```

### Create an admin user

```bash
make superuser
```

### Clean Python cache files

```bash
make clean
```

### Show available commands

```bash
make help
```

---

## 📌 What I Focused On

Instead of focusing only on the visual side of the website, I focused heavily on building a **functional backend**.

The project allowed me to practice:

* Django models
* Model relationships
* Foreign Keys
* Many-to-Many relationships
* Django ORM
* CRUD operations
* Authentication
* Authorization
* File uploads
* Course management
* Wishlist systems
* Purchase systems
* Feedback systems
* Course ratings
* Recommendation systems
* Information retrieval
* BM25
* Backend architecture

---

## 🔮 Future Improvements

Some features that could be added in the future:

* 💳 Real payment integration
* 💬 Course discussions
* 🔍 Advanced course search
* 📊 Instructor analytics
* 📈 Student progress tracking
* 🎓 Course completion certificates
* 🔔 Notifications
* 🤖 AI-powered course recommendations
* 🔎 Hybrid search using **BM25 + embeddings**
* 📱 Responsive/mobile-friendly interface
* ☁️ Cloud storage for videos and PDFs
* 🔐 More advanced authorization and permissions

---

## 🎯 Purpose of the Project

This project is more than just a course-selling website.

I built it to practice how to take **backend concepts, algorithms, and data structures** and integrate them into a real-world web application.

For example:

```text
Django
  +
Database Design
  +
Authentication
  +
CRUD
  +
Information Retrieval
  +
BM25
  ↓
Real-world Application
```

The goal is to continue improving the platform and gradually introduce more advanced technologies such as **semantic search, embeddings, recommendation systems, and AI-powered features**.

---

## 👨‍💻 Author

**Mohamed Kirate**

Machine Learning Engineer & Data Scientist

Interested in:

* Machine Learning
* Data Science
* Backend Development
* Django
* Information Retrieval
* RAG
* LLMs
* AI Applications

---

## ⭐ If You Like the Project

If you find this project interesting, feel free to **star the repository** and explore the code.
