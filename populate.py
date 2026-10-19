import os
import django
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apar_learning.settings')
django.setup()

from django.contrib.auth.models import User
from authentication.models import Profile
from course_management.models import Course, Enrollment
from assignment_quiz.models import Assignment, Quiz, Question
from content_management.models import Content
from communication.models import Message
from progress.models import Progress
from feedback.models import Feedback

def create_sample_data():
    # Create users
    # Admin
    admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
    if created:
        admin_user.set_password('admin123')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
    admin_profile, _ = Profile.objects.get_or_create(user=admin_user, defaults={'role': 'admin'})

    # Instructors
    instructor1, _ = User.objects.get_or_create(username='instructor1', defaults={'email': 'instructor1@example.com'})
    if not instructor1.password:
        instructor1.set_password('pass123')
        instructor1.save()
    Profile.objects.get_or_create(user=instructor1, defaults={'role': 'instructor'})

    instructor2, _ = User.objects.get_or_create(username='instructor2', defaults={'email': 'instructor2@example.com'})
    if not instructor2.password:
        instructor2.set_password('pass123')
        instructor2.save()
    Profile.objects.get_or_create(user=instructor2, defaults={'role': 'instructor'})

    # Students
    student1, _ = User.objects.get_or_create(username='student1', defaults={'email': 'student1@example.com'})
    if not student1.password:
        student1.set_password('pass123')
        student1.save()
    Profile.objects.get_or_create(user=student1, defaults={'role': 'student'})

    student2, _ = User.objects.get_or_create(username='student2', defaults={'email': 'student2@example.com'})
    if not student2.password:
        student2.set_password('pass123')
        student2.save()
    Profile.objects.get_or_create(user=student2, defaults={'role': 'student'})

    student3, _ = User.objects.get_or_create(username='student3', defaults={'email': 'student3@example.com'})
    if not student3.password:
        student3.set_password('pass123')
        student3.save()
    Profile.objects.get_or_create(user=student3, defaults={'role': 'student'})

    student4, _ = User.objects.get_or_create(username='student4', defaults={'email': 'student4@example.com'})
    if not student4.password:
        student4.set_password('pass123')
        student4.save()
    Profile.objects.get_or_create(user=student4, defaults={'role': 'student'})

    student5, _ = User.objects.get_or_create(username='student5', defaults={'email': 'student5@example.com'})
    if not student5.password:
        student5.set_password('pass123')
        student5.save()
    Profile.objects.get_or_create(user=student5, defaults={'role': 'student'})

    # Courses
    course1, _ = Course.objects.get_or_create(
        title='Introduction to Python',
        defaults={
            'description': 'Learn the basics of Python programming.',
            'instructor': instructor1
        }
    )

    course2, _ = Course.objects.get_or_create(
        title='Web Development with Django',
        defaults={
            'description': 'Build web applications using Django framework.',
            'instructor': instructor2
        }
    )

    course3, _ = Course.objects.get_or_create(
        title='Data Science Fundamentals',
        defaults={
            'description': 'Introduction to data analysis and machine learning.',
            'instructor': instructor1
        }
    )

    course4, _ = Course.objects.get_or_create(
        title='JavaScript for Beginners',
        defaults={
            'description': 'Master JavaScript programming from scratch with hands-on projects and real-world applications.',
            'instructor': instructor2
        }
    )

    course5, _ = Course.objects.get_or_create(
        title='Machine Learning with Python',
        defaults={
            'description': 'Dive deep into machine learning algorithms, neural networks, and AI applications using Python and scikit-learn.',
            'instructor': instructor1
        }
    )

    course6, _ = Course.objects.get_or_create(
        title='React.js Development',
        defaults={
            'description': 'Build modern, interactive user interfaces with React.js, hooks, and state management.',
            'instructor': instructor2
        }
    )

    course7, _ = Course.objects.get_or_create(
        title='Cybersecurity Fundamentals',
        defaults={
            'description': 'Learn essential cybersecurity concepts, ethical hacking, and network security principles.',
            'instructor': instructor1
        }
    )

    course8, _ = Course.objects.get_or_create(
        title='Cloud Computing with AWS',
        defaults={
            'description': 'Master Amazon Web Services, cloud architecture, and scalable application deployment.',
            'instructor': instructor2
        }
    )

    course9, _ = Course.objects.get_or_create(
        title='DevOps Engineering',
        defaults={
            'description': 'Learn CI/CD pipelines, containerization with Docker, and infrastructure automation.',
            'instructor': instructor1
        }
    )

    # Enrollments
    Enrollment.objects.get_or_create(student=student1, course=course1)
    Enrollment.objects.get_or_create(student=student1, course=course2)
    Enrollment.objects.get_or_create(student=student2, course=course1)
    Enrollment.objects.get_or_create(student=student2, course=course3)
    Enrollment.objects.get_or_create(student=student3, course=course2)
    Enrollment.objects.get_or_create(student=student3, course=course4)
    Enrollment.objects.get_or_create(student=student4, course=course3)
    Enrollment.objects.get_or_create(student=student4, course=course4)
    Enrollment.objects.get_or_create(student=student5, course=course1)
    Enrollment.objects.get_or_create(student=student5, course=course2)
    Enrollment.objects.get_or_create(student=student5, course=course3)

    # Sample Assignment
    assignment1, _ = Assignment.objects.get_or_create(
        course=course1,
        title='Python Basics Assignment',
        defaults={
            'description': 'Complete the basic Python exercises.',
            'due_date': timezone.now() + timedelta(days=30)
        }
    )

    # Sample Quiz
    quiz1, _ = Quiz.objects.get_or_create(
        course=course1,
        title='Python Fundamentals Quiz',
        defaults={
            'description': 'Test your knowledge of Python basics.',
            'time_limit': timedelta(minutes=30)
        }
    )

    question1, _ = Question.objects.get_or_create(
        quiz=quiz1,
        question_text='What is the output of print(2 + 3)?',
        defaults={
            'options': ['5', '23', '2+3', 'Error'],
            'correct_answer': '5'
        }
    )

    # Sample Content - Enhanced for all courses
    # Python Course Content
    content1, _ = Content.objects.get_or_create(
        course=course1,
        title='Python Installation and Setup',
        defaults={
            'content_type': 'video',
            'description': 'Complete guide to installing Python and setting up your development environment. Learn about different Python versions, IDEs, and best practices for beginners.',
            'video_url': 'https://www.youtube.com/watch?v=example1',
            'order': 1
        }
    )

    content2, _ = Content.objects.get_or_create(
        course=course1,
        title='Python Basics: Variables and Data Types',
        defaults={
            'content_type': 'video',
            'description': 'Understanding variables, strings, numbers, booleans, and type conversion in Python. Interactive examples and exercises included.',
            'video_url': 'https://www.youtube.com/watch?v=example2',
            'order': 2
        }
    )

    content3, _ = Content.objects.get_or_create(
        course=course1,
        title='Control Structures: Loops and Conditionals',
        defaults={
            'content_type': 'video',
            'description': 'Master if-else statements, for loops, while loops, and nested control structures. Real-world examples and debugging tips.',
            'video_url': 'https://www.youtube.com/watch?v=example3',
            'order': 3
        }
    )

    content4, _ = Content.objects.get_or_create(
        course=course1,
        title='Functions and Modules',
        defaults={
            'content_type': 'video',
            'description': 'Learn to write reusable functions, work with modules, and understand scope. Includes lambda functions and built-in modules.',
            'video_url': 'https://www.youtube.com/watch?v=example4',
            'order': 4
        }
    )

    content5, _ = Content.objects.get_or_create(
        course=course1,
        title='File Handling in Python',
        defaults={
            'content_type': 'video',
            'description': 'Reading and writing files, working with different file formats (text, CSV, JSON), and error handling for file operations.',
            'video_url': 'https://www.youtube.com/watch?v=example5',
            'order': 5
        }
    )

    content6, _ = Content.objects.get_or_create(
        course=course1,
        title='Python Project: Build a Calculator',
        defaults={
            'content_type': 'interactive',
            'description': 'Apply your Python knowledge to build a fully functional calculator application. Step-by-step project walkthrough.',
            'video_url': 'https://www.youtube.com/watch?v=example6',
            'order': 6
        }
    )

    # Django Course Content
    django_content1, _ = Content.objects.get_or_create(
        course=course2,
        title='Django Fundamentals: MVC Architecture',
        defaults={
            'content_type': 'video',
            'description': 'Understanding Django\'s Model-View-Template architecture, project structure, and core concepts. Setting up your first Django project.',
            'video_url': 'https://www.youtube.com/watch?v=django1',
            'order': 1
        }
    )

    django_content2, _ = Content.objects.get_or_create(
        course=course2,
        title='Models and Database Design',
        defaults={
            'content_type': 'video',
            'description': 'Creating Django models, understanding relationships (OneToOne, ForeignKey, ManyToMany), and database migrations.',
            'video_url': 'https://www.youtube.com/watch?v=django2',
            'order': 2
        }
    )

    django_content3, _ = Content.objects.get_or_create(
        course=course2,
        title='Views and URL Routing',
        defaults={
            'content_type': 'video',
            'description': 'Function-based and class-based views, URL patterns, and routing. Learn to handle HTTP requests and responses.',
            'video_url': 'https://www.youtube.com/watch?v=django3',
            'order': 3
        }
    )

    django_content4, _ = Content.objects.get_or_create(
        course=course2,
        title='Templates and Static Files',
        defaults={
            'content_type': 'video',
            'description': 'Django template language, template inheritance, static file handling, and creating responsive user interfaces.',
            'video_url': 'https://www.youtube.com/watch?v=django4',
            'order': 4
        }
    )

    django_content5, _ = Content.objects.get_or_create(
        course=course2,
        title='Forms and User Authentication',
        defaults={
            'content_type': 'video',
            'description': 'Django forms, model forms, user registration, login/logout, and securing your web application.',
            'video_url': 'https://www.youtube.com/watch?v=django5',
            'order': 5
        }
    )

    django_content6, _ = Content.objects.get_or_create(
        course=course2,
        title='Django Project: Blog Application',
        defaults={
            'content_type': 'interactive',
            'description': 'Build a complete blog application with user authentication, CRUD operations, and responsive design.',
            'video_url': 'https://www.youtube.com/watch?v=django6',
            'order': 6
        }
    )

    # Data Science Course Content
    ds_content1, _ = Content.objects.get_or_create(
        course=course3,
        title='Introduction to Data Science',
        defaults={
            'content_type': 'video',
            'description': 'Overview of data science field, career paths, tools, and methodologies. Understanding the data science workflow.',
            'video_url': 'https://www.youtube.com/watch?v=ds1',
            'order': 1
        }
    )

    ds_content2, _ = Content.objects.get_or_create(
        course=course3,
        title='Python for Data Analysis: NumPy',
        defaults={
            'content_type': 'video',
            'description': 'NumPy arrays, mathematical operations, indexing, and data manipulation techniques for efficient numerical computing.',
            'video_url': 'https://www.youtube.com/watch?v=ds2',
            'order': 2
        }
    )

    ds_content3, _ = Content.objects.get_or_create(
        course=course3,
        title='Data Manipulation with Pandas',
        defaults={
            'content_type': 'video',
            'description': 'Pandas DataFrames and Series, data cleaning, filtering, grouping, and merging datasets for analysis.',
            'video_url': 'https://www.youtube.com/watch?v=ds3',
            'order': 3
        }
    )

    ds_content4, _ = Content.objects.get_or_create(
        course=course3,
        title='Data Visualization with Matplotlib',
        defaults={
            'content_type': 'video',
            'description': 'Creating charts, graphs, and visualizations. Understanding different plot types and customization options.',
            'video_url': 'https://www.youtube.com/watch?v=ds4',
            'order': 4
        }
    )

    ds_content5, _ = Content.objects.get_or_create(
        course=course3,
        title='Introduction to Machine Learning',
        defaults={
            'content_type': 'video',
            'description': 'Machine learning concepts, supervised vs unsupervised learning, and building your first ML models.',
            'video_url': 'https://www.youtube.com/watch?v=ds5',
            'order': 5
        }
    )

    ds_content6, _ = Content.objects.get_or_create(
        course=course3,
        title='Data Science Project: Predictive Analytics',
        defaults={
            'content_type': 'interactive',
            'description': 'End-to-end data science project: data collection, cleaning, analysis, visualization, and predictive modeling.',
            'video_url': 'https://www.youtube.com/watch?v=ds6',
            'order': 6
        }
    )

    # JavaScript Course Content
    js_content1, _ = Content.objects.get_or_create(
        course=course4,
        title='JavaScript Fundamentals',
        defaults={
            'content_type': 'video',
            'description': 'Variables, data types, operators, and basic syntax. Understanding JavaScript as a programming language.',
            'video_url': 'https://www.youtube.com/watch?v=js1',
            'order': 1
        }
    )

    js_content2, _ = Content.objects.get_or_create(
        course=course4,
        title='DOM Manipulation',
        defaults={
            'content_type': 'video',
            'description': 'Understanding the Document Object Model, selecting elements, and dynamically modifying web pages.',
            'video_url': 'https://www.youtube.com/watch?v=js2',
            'order': 2
        }
    )

    js_content3, _ = Content.objects.get_or_create(
        course=course4,
        title='Events and Event Handling',
        defaults={
            'content_type': 'video',
            'description': 'Event listeners, event objects, and creating interactive web applications with JavaScript events.',
            'video_url': 'https://www.youtube.com/watch?v=js3',
            'order': 3
        }
    )

    js_content4, _ = Content.objects.get_or_create(
        course=course4,
        title='Asynchronous JavaScript',
        defaults={
            'content_type': 'video',
            'description': 'Promises, async/await, AJAX, and API integration. Understanding asynchronous programming concepts.',
            'video_url': 'https://www.youtube.com/watch?v=js4',
            'order': 4
        }
    )

    js_content5, _ = Content.objects.get_or_create(
        course=course4,
        title='Modern JavaScript: ES6+ Features',
        defaults={
            'content_type': 'video',
            'description': 'Arrow functions, destructuring, modules, classes, and other modern JavaScript features.',
            'video_url': 'https://www.youtube.com/watch?v=js5',
            'order': 5
        }
    )

    js_content6, _ = Content.objects.get_or_create(
        course=course4,
        title='JavaScript Project: Interactive Web App',
        defaults={
            'content_type': 'interactive',
            'description': 'Build a complete interactive web application using HTML, CSS, and JavaScript. Includes API integration and modern UI.',
            'video_url': 'https://www.youtube.com/watch?v=js6',
            'order': 6
        }
    )

    # Machine Learning Course Content
    ml_content1, _ = Content.objects.get_or_create(
        course=course5,
        title='Introduction to Machine Learning',
        defaults={
            'content_type': 'video',
            'description': 'Understanding ML concepts, types of learning, and real-world applications. Setting up your ML environment.',
            'video_url': 'https://www.youtube.com/watch?v=ml1',
            'order': 1
        }
    )

    ml_content2, _ = Content.objects.get_or_create(
        course=course5,
        title='Linear Regression and Gradient Descent',
        defaults={
            'content_type': 'video',
            'description': 'Simple and multiple linear regression, cost functions, and optimization with gradient descent.',
            'video_url': 'https://www.youtube.com/watch?v=ml2',
            'order': 2
        }
    )

    ml_content3, _ = Content.objects.get_or_create(
        course=course5,
        title='Logistic Regression and Classification',
        defaults={
            'content_type': 'video',
            'description': 'Binary and multiclass classification, sigmoid function, and evaluation metrics.',
            'video_url': 'https://www.youtube.com/watch?v=ml3',
            'order': 3
        }
    )

    ml_content4, _ = Content.objects.get_or_create(
        course=course5,
        title='Decision Trees and Random Forests',
        defaults={
            'content_type': 'video',
            'description': 'Tree-based algorithms, ensemble methods, and feature importance analysis.',
            'video_url': 'https://www.youtube.com/watch?v=ml4',
            'order': 4
        }
    )

    ml_content5, _ = Content.objects.get_or_create(
        course=course5,
        title='Neural Networks and Deep Learning',
        defaults={
            'content_type': 'video',
            'description': 'Artificial neural networks, backpropagation, and introduction to deep learning frameworks.',
            'video_url': 'https://www.youtube.com/watch?v=ml5',
            'order': 5
        }
    )

    ml_content6, _ = Content.objects.get_or_create(
        course=course5,
        title='ML Project: Image Classification',
        defaults={
            'content_type': 'interactive',
            'description': 'Build and deploy an image classification model using convolutional neural networks.',
            'video_url': 'https://www.youtube.com/watch?v=ml6',
            'order': 6
        }
    )
    # React Course Content
    react_content1, _ = Content.objects.get_or_create(
        course=course6,
        title='React Fundamentals and JSX',
        defaults={
            'content_type': 'video',
            'description': 'Understanding React components, JSX syntax, and creating your first React application.',
            'video_url': 'https://www.youtube.com/watch?v=react1',
            'order': 1
        }
    )

    react_content2, _ = Content.objects.get_or_create(
        course=course6,
        title='Components and Props',
        defaults={
            'content_type': 'video',
            'description': 'Functional and class components, props passing, and component composition patterns.',
            'video_url': 'https://www.youtube.com/watch?v=react2',
            'order': 2
        }
    )

    react_content3, _ = Content.objects.get_or_create(
        course=course6,
        title='State Management with Hooks',
        defaults={
            'content_type': 'video',
            'description': 'useState, useEffect, and custom hooks for managing component state and side effects.',
            'video_url': 'https://www.youtube.com/watch?v=react3',
            'order': 3
        }
    )

    react_content4, _ = Content.objects.get_or_create(
        course=course6,
        title='React Router and Navigation',
        defaults={
            'content_type': 'video',
            'description': 'Client-side routing, navigation guards, and building multi-page React applications.',
            'video_url': 'https://www.youtube.com/watch?v=react4',
            'order': 4
        }
    )

    react_content5, _ = Content.objects.get_or_create(
        course=course6,
        title='Context API and Redux',
        defaults={
            'content_type': 'video',
            'description': 'Global state management with Context API and Redux for complex applications.',
            'video_url': 'https://www.youtube.com/watch?v=react5',
            'order': 5
        }
    )

    react_content6, _ = Content.objects.get_or_create(
        course=course6,
        title='React Project: E-commerce App',
        defaults={
            'content_type': 'interactive',
            'description': 'Build a full-featured e-commerce application with shopping cart, user authentication, and payment integration.',
            'video_url': 'https://www.youtube.com/watch?v=react6',
            'order': 6
        }
    )

    # Cybersecurity Course Content
    cyber_content1, _ = Content.objects.get_or_create(
        course=course7,
        title='Cybersecurity Fundamentals',
        defaults={
            'content_type': 'video',
            'description': 'Understanding cybersecurity threats, attack vectors, and defense strategies.',
            'video_url': 'https://www.youtube.com/watch?v=cyber1',
            'order': 1
        }
    )

    cyber_content2, _ = Content.objects.get_or_create(
        course=course7,
        title='Network Security',
        defaults={
            'content_type': 'video',
            'description': 'Firewalls, VPNs, intrusion detection systems, and secure network architecture.',
            'video_url': 'https://www.youtube.com/watch?v=cyber2',
            'order': 2
        }
    )

    cyber_content3, _ = Content.objects.get_or_create(
        course=course7,
        title='Ethical Hacking Techniques',
        defaults={
            'content_type': 'video',
            'description': 'Penetration testing, vulnerability assessment, and ethical hacking methodologies.',
            'video_url': 'https://www.youtube.com/watch?v=cyber3',
            'order': 3
        }
    )

    cyber_content4, _ = Content.objects.get_or_create(
        course=course7,
        title='Cryptography and Encryption',
        defaults={
            'content_type': 'video',
            'description': 'Symmetric and asymmetric encryption, digital signatures, and cryptographic protocols.',
            'video_url': 'https://www.youtube.com/watch?v=cyber4',
            'order': 4
        }
    )

    cyber_content5, _ = Content.objects.get_or_create(
        course=course7,
        title='Incident Response and Forensics',
        defaults={
            'content_type': 'video',
            'description': 'Security incident handling, digital forensics, and evidence collection techniques.',
            'video_url': 'https://www.youtube.com/watch?v=cyber5',
            'order': 5
        }
    )

    cyber_content6, _ = Content.objects.get_or_create(
        course=course7,
        title='Cybersecurity Project: Security Audit',
        defaults={
            'content_type': 'interactive',
            'description': 'Conduct a comprehensive security audit of a web application and implement security measures.',
            'video_url': 'https://www.youtube.com/watch?v=cyber6',
            'order': 6
        }
    )

    # Cloud Computing Course Content
    cloud_content1, _ = Content.objects.get_or_create(
        course=course8,
        title='Cloud Computing Fundamentals',
        defaults={
            'content_type': 'video',
            'description': 'Understanding cloud service models (IaaS, PaaS, SaaS) and deployment models.',
            'video_url': 'https://www.youtube.com/watch?v=cloud1',
            'order': 1
        }
    )

    cloud_content2, _ = Content.objects.get_or_create(
        course=course8,
        title='AWS Core Services',
        defaults={
            'content_type': 'video',
            'description': 'EC2, S3, RDS, Lambda, and other essential AWS services for application deployment.',
            'video_url': 'https://www.youtube.com/watch?v=cloud2',
            'order': 2
        }
    )

    cloud_content3, _ = Content.objects.get_or_create(
        course=course8,
        title='Serverless Architecture',
        defaults={
            'content_type': 'video',
            'description': 'Building serverless applications with AWS Lambda, API Gateway, and DynamoDB.',
            'video_url': 'https://www.youtube.com/watch?v=cloud3',
            'order': 3
        }
    )

    cloud_content4, _ = Content.objects.get_or_create(
        course=course8,
        title='Cloud Security and Compliance',
        defaults={
            'content_type': 'video',
            'description': 'IAM, security groups, encryption, and compliance frameworks in the cloud.',
            'video_url': 'https://www.youtube.com/watch?v=cloud4',
            'order': 4
        }
    )

    cloud_content5, _ = Content.objects.get_or_create(
        course=course8,
        title='Monitoring and Scaling',
        defaults={
            'content_type': 'video',
            'description': 'CloudWatch, auto-scaling, load balancing, and performance optimization.',
            'video_url': 'https://www.youtube.com/watch?v=cloud5',
            'order': 5
        }
    )

    cloud_content6, _ = Content.objects.get_or_create(
        course=course8,
        title='Cloud Project: Scalable Web App',
        defaults={
            'content_type': 'interactive',
            'description': 'Deploy a highly available, scalable web application on AWS with CI/CD pipeline.',
            'video_url': 'https://www.youtube.com/watch?v=cloud6',
            'order': 6
        }
    )

    # DevOps Course Content
    devops_content1, _ = Content.objects.get_or_create(
        course=course9,
        title='DevOps Culture and Principles',
        defaults={
            'content_type': 'video',
            'description': 'Understanding DevOps culture, agile methodologies, and continuous improvement practices.',
            'video_url': 'https://www.youtube.com/watch?v=devops1',
            'order': 1
        }
    )

    devops_content2, _ = Content.objects.get_or_create(
        course=course9,
        title='Version Control with Git',
        defaults={
            'content_type': 'video',
            'description': 'Advanced Git workflows, branching strategies, and collaboration techniques.',
            'video_url': 'https://www.youtube.com/watch?v=devops2',
            'order': 2
        }
    )

    devops_content3, _ = Content.objects.get_or_create(
        course=course9,
        title='Containerization with Docker',
        defaults={
            'content_type': 'video',
            'description': 'Docker fundamentals, container orchestration, and building microservices architecture.',
            'video_url': 'https://www.youtube.com/watch?v=devops3',
            'order': 3
        }
    )

    devops_content4, _ = Content.objects.get_or_create(
        course=course9,
        title='CI/CD Pipelines',
        defaults={
            'content_type': 'video',
            'description': 'Jenkins, GitHub Actions, automated testing, and deployment pipelines.',
            'video_url': 'https://www.youtube.com/watch?v=devops4',
            'order': 4
        }
    )

    devops_content5, _ = Content.objects.get_or_create(
        course=course9,
        title='Infrastructure as Code',
        defaults={
            'content_type': 'video',
            'description': 'Terraform, Ansible, and automated infrastructure provisioning and configuration.',
            'video_url': 'https://www.youtube.com/watch?v=devops5',
            'order': 5
        }
    )

    devops_content6, _ = Content.objects.get_or_create(
        course=course9,
        title='DevOps Project: Full CI/CD Pipeline',
        defaults={
            'content_type': 'interactive',
            'description': 'Build a complete CI/CD pipeline for a microservices application with monitoring and logging.',
            'video_url': 'https://www.youtube.com/watch?v=devops6',
            'order': 6
        }
    )
    # Sample Message
    message1, _ = Message.objects.get_or_create(
        sender=student1,
        receiver=instructor1,
        defaults={
            'course': course1,
            'message': 'Question about assignment: I have a question about the Python assignment.',
            'is_read': False
        }
    )

    # Sample Feedback
    feedback1, _ = Feedback.objects.get_or_create(
        student=student1,
        course=course1,
        defaults={
            'rating': 5,
            'comment': 'Excellent course! Learned a lot.'
        }
    )

    print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()