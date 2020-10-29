import subjects
from tests import factories
from django.urls import reverse
import pytest
import os


@pytest.mark.django_db
class TestSubjectViews:

	def test_viewall_subjects(self, client):
		factories.SubjectFactory.create()
		response = client.get(reverse('list'))
		assert response.status_code == 200
		assert response.templates[0].name == 'subjects/subject_list.html'

	def test_browse_subjects(self, client):
		factories.SubjectFactory.create()
		response = client.get(reverse('main_browse'))
		assert response.status_code == 200
		assert response.templates[0].name == 'subjects/subject_browse.html'

	def test_browse_subjects_with_sub_id(self, client):
		sub = factories.SubjectFactory.create()
		response = client.get(reverse('browse', kwargs={'sub_id': sub.id}))
		assert response.status_code == 200
		assert response.templates[0].name == 'subjects/subject_browse.html'

	def test_browse_subjects_with_sub_name(self, client):
		sub = factories.SubjectFactory.create()
		response = client.get(reverse('browse_sub_name', kwargs={'sub_name': sub.name}))
		assert response.status_code == 200
		assert response.templates[0].name == 'subjects/subject_browse.html'

	def test_search_subjects(self, client):
		factories.SubjectFactory.create()
		response = client.get(reverse('search_subjects'))

		assert response.status_code == 200
		assert response.templates[0].name == 'subjects/subject_search.html'

	def test_about_subjects(self, client):
		# Get the path of app path and the filename
		app_path = subjects.__path__[0]
		about_filepath = os.path.join(app_path, 'about_markdown.txt')
		response = client.get(reverse('about_subjects'))
		with open(about_filepath, 'r') as about_file:
			about_markdown = about_file.read()

		assert response.status_code == 200
		assert response.templates[0].name == 'subjects/subject_about.html'
		assert response.context['about_markdown'] == about_markdown

	def test_json_list_subjects(self, client):
		factories.SubjectFactory.create(name='sub1')
		factories.SubjectFactory.create(name='sub2')
		factories.SubjectFactory.create(name='sub3')
		response = client.get(reverse('untlbs_json'))
		assert response.status_code == 200
		assert response.content == \
			b'["sub1 - sub2 - sub3", "sub1 - sub2 - sub3", "sub1 - sub2 - sub3"]'
