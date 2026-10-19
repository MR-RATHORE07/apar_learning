# APAR Learning LMS

A comprehensive Learning Management System built with Django, MySQL, HTML, CSS, and JavaScript.

## Features

- **User Authentication & Role Management**: Login, registration, role-based access (Admin, Instructor, Student) with automatic profile creation
- **Admin Management**: Manage users, courses, and system settings via Django admin
- **Instructor Management**: Create and manage courses, assignments, quizzes, and content
- **Student Management**: Enroll in courses, submit assignments, take quizzes, track progress
- **Course Management**: Create, view, and manage courses with enrollment system
- **Assignment & Quiz Module**: Create assignments with file uploads, submit and grade assignments; create quizzes with multiple choice questions, take quizzes with scoring
- **Content Management**: Upload videos, documents, images, and links to courses
- **Progress Tracking**: Mark content as completed, track learning progress
- **Communication & Notification**: Send and receive messages between users
- **Feedback & Support**: Submit ratings and comments on courses
- **Database Management**: SQLite for development, MySQL for production

## Setup Instructions

1. **Prerequisites**:
   - Python 3.8 or higher
   - MySQL Server installed and running (for production)
   - Git (optional)

2. **Clone or Download the Project**:
   - Place the project in your desired directory.

3. **Create Virtual Environment**:
   ```
   python -m venv venv
   ```

4. **Activate Virtual Environment**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

5. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

6. **Configure the Django Secret Key**:
   - Local development uses a built-in development-only key.
   - For deployment, set `DJANGO_SECRET_KEY` to a unique, randomly generated value and keep it out of source control.
   - PowerShell: `$env:DJANGO_SECRET_KEY = "your-generated-secret-key"`
   - Linux/macOS: `export DJANGO_SECRET_KEY="your-generated-secret-key"`

7. **Database Setup**:
   - The project is currently configured to use SQLite for development.
   - For production with MySQL:
     - Download and install MySQL Server from https://dev.mysql.com/downloads/mysql/
     - During installation, set up a root password
     - Start MySQL service
     - Create database: `CREATE DATABASE apar_learning_db;`
     - Create user: `CREATE USER 'apar_user'@'localhost' IDENTIFIED BY 'your_password';`
     - Grant privileges: `GRANT ALL PRIVILEGES ON apar_learning_db.* TO 'apar_user'@'localhost';`
     - Update `apar_learning/settings.py` with your MySQL credentials:
       ```python
       DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.mysql',
               'NAME': 'apar_learning_db',
               'USER': 'apar_user',
               'PASSWORD': 'your_password',
               'HOST': 'localhost',
               'PORT': '3306',
           }
       }
       ```

8. **Run Migrations**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

9. **Create Superuser**:
   ```
   python manage.py createsuperuser
   ```
   Or use the provided script (already run for demo).

10. **Run the Development Server**:
   ```
   python manage.py runserver
   ```

11. **Access the Application**:
    - Open your browser and go to `http://127.0.0.1:8000/`
    - Admin panel: `http://127.0.0.1:8000/admin/` (username: admin, password: admin)
    - Register new users or login with existing accounts
    - Instructors can create courses, assignments, quizzes, and content
    - Students can enroll, submit work, take quizzes, and provide feedback

## Project Structure

- `apar_learning/`: Main project settings
- `authentication/`: User authentication and profiles
- `admin_management/`: Admin-specific functionality
- `instructor_management/`: Instructor tools
- `student_management/`: Student features
- `course_management/`: Course creation and management
- `assignment_quiz/`: Assignments and quizzes
- `content_management/`: Course content handling
- `communication/`: Messaging system
- `progress/`: Progress tracking
- `feedback/`: Feedback system
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, images
- `media/`: User-uploaded files

## Technologies Used

- **Backend**: Django 5.0
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS (can be extended with Bootstrap, etc.)

## Development

- To add new features, create views in the respective app's `views.py`
- Create templates in `templates/app_name/`
- Add URLs in `app_name/urls.py` and include in main `urls.py`
- Run migrations for model changes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open-source. Feel free to use and modify.

## Support

For issues or questions, please check the Django documentation or create an issue in the repository.