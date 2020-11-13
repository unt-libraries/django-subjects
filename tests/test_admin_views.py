from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from tests import factories
import pytest
from unittest import mock


@pytest.mark.django_db
class TestSubjectAdd(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
                          'test_user', 'test_user@test.com', 'password')
        self.admin_user.save()
        self.c = Client()
        self.c.force_login(self.admin_user)

    def test_subject_add(self):
        """Test main add menu is displayed."""
        response = self.c.get(reverse('admin_main_add'))
        assert response.status_code == 200
        # Assert the subject will be added to the top level
        assert response.context['browse_len'] == 0
        assert response.context['saved'] is None
        assert response.templates[0].name == 'subjects/add_subject.html'

    def test_subject_add_to_sub_id(self):
        """Test the AddSubject form for new subject will add it as a sub-category
         to the current subject."""
        subject = factories.SubjectFactory.create()
        response = self.c.get(reverse('admin_add', kwargs={'sub_id': subject.id}))
        # Assert the new subject will be added as a sub category of 'subject'.
        assert response.context['browse_len'] == 1
        assert response.context['browse_string'] == subject.name
        assert response.context['saved'] is None
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/add_subject.html'

    def test_subject_add_post_with_sub_id(self):
        """Test the new subject is added."""
        subject = factories.SubjectFactory.create()
        name = 'foo'
        with mock.patch('subjects.admin_views.AddSubject') as mock_form:
            mock_form.return_value.is_valid.return_value = True
            mock_form.return_value.cleaned_data = {'name': name,
                                                   'keywords': 'test keywords',
                                                   'notes': 'test notes'}
            response = self.c.post(reverse('admin_add', kwargs={'sub_id': subject.id}))

        assert response.context['saved'].name == name
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/add_subject.html'


@pytest.mark.django_db
class TestSubjectModify(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            'test_user', 'test_user@test.com', 'password')
        self.admin_user.save()
        self.c = Client()
        self.c.force_login(self.admin_user)

    def test_subject_modify(self):
        """Test main modify menu is displayed."""
        response = self.c.get(reverse('admin_main_modify'))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/modify_subject.html'
        assert response.context['modified'] is None

    def test_subject_modify_post_with_sub_id(self):
        """Test the subject is modified."""
        subject = factories.SubjectFactory.create()
        with mock.patch('subjects.admin_views.ModifySubject') as mock_form:
            mock_form.return_value.is_valid.return_value = True
            mock_form.return_value.cleaned_data = {'keywords': 'modified_keyword',
                                                   'notes': 'modified_notes'}
            response = self.c.post(reverse('admin_modify', kwargs={'sub_id': subject.id}))
        subject.refresh_from_db()

        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/modify_subject.html'
        assert response.context['selected_subject'].name == subject.name
        assert response.context['modified'].name == subject.name
        assert subject.notes == 'modified_notes'
        assert subject.keywords == 'modified_keyword'


@pytest.mark.django_db
class TestSubjectDelete(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            'test_user', 'test_user@test.com', 'password')
        self.admin_user.save()
        self.c = Client()
        self.c.force_login(self.admin_user)

    def test_subject_delete(self):
        """Test main delete menu is displayed."""
        subjects = factories.SubjectFactory.create_batch(3)
        response = self.c.get(reverse('admin_main_delete'))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/delete_subject.html'
        assert response.context['current_subject'] == ''
        assert response.context['child_error'] is None
        # Assert all subject objects that can be deleted are listed on html page
        for value in subjects:
            assert value.name.encode() in response.content

    def test_subject_delete_with_sub_id(self):
        """Test the browse structure is displayed."""
        subject = factories.SubjectFactory.create()
        subject_2 = factories.SubjectFactory.create(parent=subject.id)
        response = self.c.get(reverse('admin_delete', kwargs={'sub_id': subject.id}))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/delete_subject.html'
        assert response.context['current_subject'].name == subject.name
        # Assert subject object's subcategories are displayed
        assert b'Click a subject to view its subcategories.' in response.content
        assert subject_2 in response.context['browse_list']
        assert response.context['child_error'] is None

    def test_subject_delete_sub_delete_with_subcategory(self):
        """Test subject(s) with sub-categories/children do not get deleted."""
        subject = factories.SubjectFactory.create(name='test_sub')
        factories.SubjectFactory.create(parent=subject.id)
        response = self.c.get(reverse('admin_delete_subject',
                                      kwargs={'sub_id': subject.id, 'sub_delete': True}))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/delete_subject.html'
        assert response.context['current_subject'].name == subject.name
        assert response.context['browse_list'] == 'Deleted'
        # Child_error is set to 1 when the subject has sub categories and isn't deleted.
        assert response.context['child_error'] == 1
        # Refresh the object and check it is not deleted.
        subject.refresh_from_db()
        assert subject.name == 'test_sub'

    def test_subject_delete_sub_delete(self):
        """Test subject(s) with no sub-categories/children is/are deleted safely."""
        subject = factories.SubjectFactory.create(parent=0, lft=0, rght=1)
        response = self.c.get(reverse('admin_delete_subject',
                                      kwargs={'sub_id': subject.id, 'sub_delete': True}))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/delete_subject.html'
        assert response.context['current_subject'].name == subject.name
        assert response.context['browse_list'] == 'Deleted'
        # Child_error is set to 2 when the subject is safely deleted.
        assert response.context['child_error'] == 2
        # Assert subject object is deleted.
        with self.assertRaises(ObjectDoesNotExist):
            subject.refresh_from_db()
