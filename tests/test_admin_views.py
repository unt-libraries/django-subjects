from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from tests import factories
import pytest
from unittest import mock


@pytest.mark.django_db
class TestAdminViews(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
                          'test_user', 'test_user@test.com', 'password')
        self.admin_user.save()
        self.c = Client()
        self.c.force_login(self.admin_user)

    def test_subject_add(self):
        response = self.c.get(reverse('admin_main_add'))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/add_subject.html'

    def test_subject_add_with_sub_id(self):
        subject = factories.SubjectFactory.create()
        response = self.c.get(reverse('admin_add', kwargs={'sub_id': subject.id}))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/add_subject.html'

    def test_subject_add_post_with_sub_id(self):
        subject = factories.SubjectFactory.create()
        subject_2 = factories.SubjectFactory.create()
        with mock.patch('subjects.admin_views.AddSubject') as mock_form:
            mock_form.return_value.is_valid.return_value = True
            mock_form.return_value.cleaned_data = {'name': subject_2.name, 'keywords': 'keyword',
                                                   'notes': 'notes'}
            response = self.c.post(reverse('admin_add', kwargs={'sub_id': subject.id}))

        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/add_subject.html'
        assert '<span class="browse"><a href="/subjects/admin/add/{id}/">{name}</a> ></span>'\
            .format(id=subject_2.id, name=subject_2.name).encode() in response.content

    def test_subject_modify(self):
        response = self.c.get(reverse('admin_main_modify'))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/modify_subject.html'

    def test_subject_modify_post_with_sub_id(self):
        subject = factories.SubjectFactory.create()
        subject_2 = factories.SubjectFactory.create()
        with mock.patch('subjects.admin_views.ModifySubject') as mock_form:
            mock_form.return_value.is_valid.return_value = True
            mock_form.return_value.cleaned_data = {'name': subject_2.name, 'keywords': 'keyword',
                                                   'notes': 'notes'}
            response = self.c.post(reverse('admin_modify', kwargs={'sub_id': subject.id}))

        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/modify_subject.html'
        print('\n response content: ', response.content)
        assert '<span class="browse"><a href=\'/subjects/admin/modify/{id}/\'>{name}</a> ></span>'\
            .format(id=subject_2.id, name=subject_2.name).encode() in response.content

    def test_subject_delete(self):
        response = self.c.get(reverse('admin_main_delete'))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/delete_subject.html'

    def test_subject_delete_with_sub_id(self):
        subject = factories.SubjectFactory.create()
        response = self.c.get(reverse('admin_delete', kwargs={'sub_id': subject.id}))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/delete_subject.html'

    def test_subject_delete_with_sub_delete(self):
        subject = factories.SubjectFactory.create()
        response = self.c.get(reverse('admin_delete_subject', kwargs={'sub_id': subject.id,
                                      'sub_delete': True}))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/delete_subject.html'
