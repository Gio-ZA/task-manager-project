# 🗂️ Task Manager Project

A Python-based task management system that allows users to register, log in, assign tasks, view reports, and manage tasks. This program stores user and task information in text files and simulates a basic user management system with admin functionality.

---

## 🚀 Features

- ✅ Register new users (admin only)  
- ✅ Add new tasks with due dates, assigned users, and descriptions  
- ✅ View all tasks or only the tasks assigned to the logged-in user  
- ✅ Mark tasks as complete  
- ✅ Edit task details (e.g., due date, assigned user) if incomplete  
- ✅ Generate reports on overall task progress  
- ✅ Admin dashboard with statistics and user overview  

---

## 📁 Files Used

- `user.txt` — Stores registered users and passwords  
- `tasks.txt` — Stores task data (assigned user, title, description, dates, status)  
- `task_overview.txt` — Auto-generated report summarizing task data (created when "generate reports" is selected)  
- `user_overview.txt` — Auto-generated report summarizing user activity (created when "display statistics" is selected)  

---

## 🔧 How to Run

1. Make sure you have Python 3 installed  
2. Clone the repository or download the files  
3. Run the program:

   ```bash
   python task_manager.py

---

🔐 Default Admin Login

- Username: admin

- Password: adm1n

After logging in, follow the on-screen menu to use the system.

---

🛠️ Technologies Used

- Python 3

- File I/O

- Basic string and date handling

---

📌 Notes

Admin users have access to additional features like registering users and viewing statistics

Input is validated for errors like invalid usernames or negative dates

The program automatically creates task_overview.txt and user_overview.txt if they don't already exist when generating reports

---

📄 License

This project is open-source and available under the MIT License
