from django.urls import path
from subjects.views import viewall_subjects, browse_subjects, \
    search_subjects, about_subjects, json_list_subjects
from subjects.admin_views import subject_add, subject_delete, subject_modify

urlpatterns = [
    # subjects/:
    # All of the URLs are prefixed by the projects urls.py by using a
    # statement such as: path('subjects/', include('subjects.urls')),
    # in urlpatterns. This example would give you example.com/subjects/ which
    # can be followed by any of these subcategories.

    # List View
    path('list/', viewall_subjects, name="list"),

    # Browse View
    path('', browse_subjects),
    path('browse/', browse_subjects, name="main_browse"),
    path('browse/<int:sub_id>/', browse_subjects, name="browse"),
    path('browse/<slug:sub_name>/', browse_subjects, name='browse_sub_name'),

    # Search View
    path('search/', search_subjects, name="search_subjects"),

    # About View
    path('about/', about_subjects, name="about_subjects"),

    # Hyphenated JSON list View
    path('untl-bs.json', json_list_subjects, name="untlbs_json"),

    # Admin View:
    path('admin/', subject_add),
    path('admin/add/', subject_add, name="admin_main_add"),
    path('admin/add/<int:sub_id>/', subject_add, name="admin_add"),
    path('admin/modify/', subject_modify, name="admin_main_modify"),
    path('admin/modify/<int:sub_id>/', subject_modify, name="admin_modify"),
    path('admin/delete/', subject_delete, name="admin_main_delete"),
    path('admin/delete/<int:sub_id>/', subject_delete, name="admin_delete"),
    path('admin/delete/<int:sub_id>/deletion/', subject_delete, {'sub_delete': True},
         name="admin_delete_subject"),
]
