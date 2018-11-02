from django.conf.urls import url
from subjects.views import viewall_subjects, browse_subjects, \
    search_subjects, about_subjects, json_list_subjects
from subjects.admin_views import subject_add, subject_delete, subject_modify

urlpatterns = [
    # subjects/:
    # All of the URLs are prefixed by the projects urls.py by using a
    # statement such as: url(r'^subjects/', include('subjects.urls')),
    # in urlpatterns. This example would give you example.com/subjects/ which
    # can be followed by any of these subcategories.

    # List View
    url(r'^list/$', viewall_subjects, name="list"),

    # Browse View
    url(r'^$', browse_subjects),
    url(r'^browse/$', browse_subjects, name="main_browse"),
    url(r'^browse/(?P<sub_id>\d+)/$', browse_subjects, name="browse"),
    url(r'^browse/(?P<sub_name>\w+)/$', browse_subjects),

    # Search View
    url(r'^search/$', search_subjects, name="search_subjects"),

    # About View
    url(r'^about/$', about_subjects, name="about_subjects"),

    # Hyphenated JSON list View
    url(r'^untl-bs.json$', json_list_subjects, name="untlbs_json"),

    # Admin View:
    url(r'^admin/$', subject_add),
    url(r'^admin/add/$', subject_add, name="admin_main_add"),
    url(r'^admin/add/(?P<sub_id>\d+)/$', subject_add, name="admin_add"),
    url(r'^admin/modify/$', subject_modify, name="admin_main_modify"),
    url(r'^admin/modify/(?P<sub_id>\d+)/$', subject_modify, name="admin_modify"),
    url(r'^admin/delete/$', subject_delete, name="admin_main_delete"),
    url(r'^admin/delete/(?P<sub_id>\d+)/$', subject_delete, name="admin_delete"),
    url(r'^admin/delete/(?P<sub_id>\d+)/deletion/$', subject_delete, {'sub_delete': True},
        name="admin_delete_subject"),
]
