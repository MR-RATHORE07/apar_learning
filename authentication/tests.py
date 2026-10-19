from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from course_management.models import Course, Enrollment


class RegistrationViewTests(TestCase):
    def test_registration_creates_student_profile_and_opens_dashboard(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newstudent',
                'password1': 'SafePassword!2468',
                'password2': 'SafePassword!2468',
            },
        )

        self.assertRedirects(response, reverse('dashboard'))
        user = User.objects.get(username='newstudent')
        self.assertEqual(user.profile.role, 'student')
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)

    def test_registration_renders_password_validation_errors(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newstudent',
                'password1': 'short',
                'password2': 'short',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(User.objects.filter(username='newstudent').exists())


class MyCoursesViewTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student',
            password='SafePassword!2468',
        )
        self.instructor = User.objects.create_user(
            username='instructor',
            password='SafePassword!2468',
        )
        self.instructor.profile.role = 'instructor'
        self.instructor.profile.save()
        self.other_instructor = User.objects.create_user(
            username='otherinstructor',
            password='SafePassword!2468',
        )
        self.enrolled_course = Course.objects.create(
            title='Enrolled course',
            description='A course the student enrolled in.',
            instructor=self.instructor,
        )
        self.other_course = Course.objects.create(
            title='Other course',
            description='A course the student did not enroll in.',
            instructor=self.instructor,
        )
        Course.objects.create(
            title='Another instructor course',
            description='A course owned by a different instructor.',
            instructor=self.other_instructor,
        )
        Enrollment.objects.create(student=self.student, course=self.enrolled_course)

    def test_student_sees_only_enrolled_courses(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse('my_courses'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enrolled course')
        self.assertNotContains(response, 'Other course')

    def test_instructor_sees_only_courses_they_teach(self):
        self.client.force_login(self.instructor)

        response = self.client.get(reverse('my_courses'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enrolled course')
        self.assertContains(response, 'Other course')
        self.assertNotContains(response, 'Another instructor course')

    def test_my_courses_requires_login(self):
        response = self.client.get(reverse('my_courses'))

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("my_courses")}',
        )
