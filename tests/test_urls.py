from django.urls import resolve
from subjects import views
from subjects import admin_views


def test_view_subjects():
    assert resolve('/subjects/list/').func == views.viewall_subjects


def test_browse_subjects():
    expected_view = views.browse_subjects
    assert resolve('/subjects/').func == expected_view
    assert resolve('/subjects/browse/').func == expected_view
    assert resolve('/subjects/browse/123/').func == expected_view
    assert resolve('/subjects/browse/sub/').func == expected_view


def test_search():
    assert resolve('/subjects/search/').func == views.search_subjects


def test_about():
    assert resolve('/subjects/about/').func == views.about_subjects


def test_json():
    assert resolve('/subjects/untl-bs.json').func == views.json_list_subjects


def test_admin():
    assert resolve('/subjects/admin/').func == admin_views.subject_add


def test_admin_add():
    expected_view = admin_views.subject_add
    assert resolve('/subjects/admin/add/').func == expected_view
    assert resolve('/subjects/admin/add/001/').func == expected_view


def test_admin_modify():
    expected_view = admin_views.subject_modify
    assert resolve('/subjects/admin/modify/').func == expected_view
    assert resolve('/subjects/admin/modify/001/').func == expected_view


def test_admin_delete():
    expected_view = admin_views.subject_delete
    assert resolve('/subjects/admin/delete/').func == expected_view
    assert resolve('/subjects/admin/delete/001/').func == expected_view
    assert resolve('/subjects/admin/delete/001/deletion/').func == expected_view
