
import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from model_bakery import baker

@pytest.fixture
def api_client():
    return  APIClient()

@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make('app_name.Course',**kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return  baker.make('app_name.Student',**kwargs)
    return factory



@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    baker.make('app_name.Course', _quantity=3)
    url = reverse('course-list')
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_filter_courses_by_id(api_client,course_factory):
    course_factory.create_batch(3)
    url = reverse('course-list')
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course = course_factory(name="Test Course")
    url = f"{reverse('course-list')}?name=Test Course"
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data[0]['name'] == "Test Course"

@pytest.mark.django_db
def test_create_course(api_client):
    data = {"name": "New Course","description": "Course description"}
    url = reverse('course-list')
    response = api_client.post(url, data)

    assert response.status_code == 201
    assert response.data['name'] == data['name']

@pytest.mark.django_db
def test_update_course(api_client,course_factory):
    course = course_factory()
    data = {"name": "Update Course","description": "Update description"}
    url = reverse ('course-detail', args=[course.id])
    response = api_client.put(url, data)

    assert response.status_code == 200
    assert response.data['name'] ==  data['name']


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    url = reverse('course-detail', args=[course.id])
    response = api_client.delete(url)

    assert response.status_code == 204


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory()
    url = reverse('course-detail', args=[course.id])
    response = api_client.get(url)

    # Проверяем код ответа и содержимое
    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name