import subjects
from tests import factories
from django.urls import reverse
import pytest
import os


@pytest.mark.django_db
class TestSubjectViews:

    def test_viewall_subjects(self, client):
        s1 = factories.SubjectFactory.create()
        s2 = factories.SubjectFactory.create()
        s3 = factories.SubjectFactory.create()
        response = client.get(reverse('list'))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/subject_list.html'
        assert '<a style="display:block;" href="/">{s1} - {s2} - {s3}</a>'\
               .format(s1=s1.name, s2=s2.name, s3=s3.name).encode() in response.content

    def test_browse_subjects(self, client):
        s1 = factories.SubjectFactory.create()
        s2 = factories.SubjectFactory.create()
        response = client.get(reverse('main_browse'))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/subject_browse.html'
        assert "<a href=\'/subjects/browse/{id}/\'>{name}</a>"\
               .format(id=s1.id, name=s1.name).encode() in response.content
        assert "<a href=\'/subjects/browse/{id}/\'>{name}</a>"\
               .format(id=s2.id, name=s2.name).encode() in response.content

    def test_browse_subjects_with_sub_id(self, client):
        sub = factories.SubjectFactory.create()
        response = client.get(reverse('browse', kwargs={'sub_id': sub.id}))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/subject_browse.html'
        assert "<input name=\'subject\' type=\'text\' size=\'57\' value=\'{name}\'>".format(
               name=sub.name).encode() in response.content

    def test_browse_subjects_with_sub_name(self, client):
        sub = factories.SubjectFactory.create()
        response = client.get(reverse('browse_sub_name', kwargs={'sub_name': sub.name}))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/subject_browse.html'
        assert "<input name=\'subject\' type=\'text\' size=\'57\' value=\'{name}\'>".format(
               name=sub.name).encode() in response.content

    def test_search_subjects(self, client):
        subject = factories.SubjectFactory.create()
        response = client.get(reverse('search_subjects') + '?q=' + subject.name)
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/subject_search.html'
        assert b'Search for a UNTLBS Subject.' in response.content
        assert '<span class="subject">{name}</span>'\
               .format(name=subject.name).encode() in response.content

    def test_empty_search_subjects(self, client):
        response = client.get(reverse('search_subjects'))
        assert response.status_code == 200
        assert response.templates[0].name == 'subjects/subject_search.html'
        assert b'Please enter a search term.' in response.content

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
