import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient
from django_testing.students.models import Course

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make('students.Course', **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make('students.Student', **kwargs)
    return factory

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    course_factory(_quantity=3)
    url = reverse('courses')
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    courses = course_factory(_quantity=3)
    url = f"{reverse('courses')}?id={courses[0].id}"
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1  # Убедитесь, что возвращается только один курс
    assert response.data[0]['id'] == courses[0].id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course = course_factory(name="Test Course")
    url = f"{reverse('courses')}?name=Test Course"
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1  # Убедитесь, что возвращается только один курс
    assert response.data[0]['name'] == "Test Course"

@pytest.mark.django_db
def test_create_course(api_client):
    data = {"name": "New Course", "description": "Course description"}
    url = reverse('courses')
    response = api_client.post(url, data)

    assert response.status_code == 201
    assert response.data['name'] == data['name']
    assert 'id' in response.data  # Проверяем, что возвращается ID нового курса

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory()
    data = {"name": "Updated Course", "description": "Updated description"}
    url = reverse('courses', args=[course.id])
    response = api_client.put(url, data)

    assert response.status_code == 200
    assert response.data['name'] == data['name']
    assert response.data['description'] == data['description']  # Проверяем обновленное описание
