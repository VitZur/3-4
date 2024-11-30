from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer

class CoursesViewSetTest(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Test Course")

    def test_get_courses(self):
        url = reverse('courses-list')
        response = self.client.get(url)
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_course(self):
        url = reverse('courses-list')
        data = {'name': 'New Course'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.get(id=2).name, 'New Course')
