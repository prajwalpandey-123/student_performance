# 🎓 Student Performance Analysis System

A **web-based application** built using **Flask (Python), MySQL, HTML, CSS, and Chart.js** to analyze and visualize student performance across academics, sports, and extracurricular activities.

---

## 🚀 Project Overview

The **Student Performance Analysis System** helps:

* 📊 Students track their academic and activity performance
* 🏅 Upload and manage certificates
* 📈 Visualize performance using charts
* 👨‍🏫 Teachers evaluate students and assign marks/ratings

This project is ideal for **college-level submissions (BCA / CS / IT)** and demonstrates full-stack development.

---

## 🛠️ Technologies Used

| Layer    | Technology                 |
| -------- | -------------------------- |
| Frontend | HTML, CSS, Chart.js        |
| Backend  | Python (Flask)             |
| Database | MySQL                      |
| Other    | Jinja2, File Upload System |

---

## 🔐 Features

### 🔑 Authentication System

* Student Login
* Teacher Login
* Session Management

---

## 🎓 Student Panel

### 📊 Performance Overview

* Academic performance
* Sports performance
* Extra-curricular activities
* Graphs (Bar chart using Chart.js)

### 📈 Marks Section

* Subject-wise marks
* Internal + external marks
* Performance visualization

### 🏅 Certificate Upload

* Upload certificates (PDF/Image)
* Categorization:

  * Games
  * Activities
* Points assigned automatically

### 📉 Graphical Analysis

* Academic graphs
* Activity-based performance tracking

---

## 👨‍🏫 Teacher Panel

### 📚 Student Management

* View all students
* Select students for evaluation

### 📝 Marks Entry

* Add subject marks
* Add internal marks

### 👁️ Performance View

* View student data and performance

---

## 🗄️ Database Structure

### Tables:

* `students`
* `teachers`
* `marks`
* `certificates`
* `performance`

---

## 📁 Project Structure

```
student-performance-system/
│
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── config.py
│   ├── models.py
│   ├── uploads/
│
├── frontend/
│   ├── templates/
│   ├── static/
│
├── database/
│   └── schema.sql
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/student-performance-system.git
cd student-performance-system
```

### 2️⃣ Install Dependencies

```bash
pip install flask mysql-connector-python
```

### 3️⃣ Setup Database

* Open MySQL
* Run:

```sql
SOURCE database/schema.sql;
```

---

### 4️⃣ Configure Database (if needed)

Update credentials in `app.py`:

```python
host="localhost"
user="root"
password=""
database="student_system"
```

---

### 5️⃣ Run the Application

```bash
cd backend
python app.py
```

---

### 6️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 📊 Sample Functional Flow

1. User logs in as **Student / Teacher**
2. Student:

   * Views performance dashboard
   * Uploads certificates
3. Teacher:

   * Adds marks
   * Evaluates students
4. Data is stored in MySQL
5. Graphs are generated dynamically

---

## 🎨 UI Features

* Responsive design
* Clean dashboard layout
* Graph-based visualization
* Simple and user-friendly interface

---

## 🔥 Future Enhancements

* 📱 Mobile-friendly UI (Bootstrap / Tailwind)
* 🤖 AI-based performance prediction
* 📄 Export report as PDF
* 🏆 Student ranking system
* 🔐 Password hashing & security improvements
* 📊 Advanced analytics dashboard

---

## ⚠️ Notes

* This is a **basic version** for learning purposes
* Passwords are stored in plain text (not recommended for production)
* Improve security before deploying

---

## 👨‍💻 Author

**Mayank Karki**
**Ayush Bisht**
**Karan Singh Bisht**
**Prajwal Pandey**
BCA Student | Aspiring Developer 🚀

---

## ⭐ Contribution

Feel free to fork, modify, and improve this project!

---

## 📜 License

This project is for educational purposes only.
