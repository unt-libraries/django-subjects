import os
import json
from operator import itemgetter
import subjects
from subjects.models import Subject
from subjects.traversal import TraversalUtils
from django.shortcuts import render
from django.http import HttpResponse
from django import forms


# View: Subjects List Tab
# Functionality: Creates a list of all of subjects_subjects row objects,
# and puts them in a hierarchical string
def viewall_subjects(request):
    subject_list = []

    # create the traversal object
    traversal = TraversalUtils()

    # Makes a list of hierarchical strings (structure show by hyphens) for each node
    # from the root down to the iterated node
    # subject.objects.filter(rght__exact=lft+1)
    for current_subject in Subject.objects.all():
        traversal.get_structured_list(Subject, current_subject)
        subject_list.append(traversal.subject_dict)

    subject_list = sorted(subject_list, key=itemgetter('hyphenated'))

    return render(
        request,
        "subjects/subject_list.html",
        {'viewall_list': subject_list},
    )


# View: Subjects Browse Tab
# Functionality: Creates a list of all children objects of the given node.
# Also creates a hierarchical list of the currently browsed subject to the root node.
# Args: [sub_id] - id of the given node to browse [sub_name] - name of the given
# node to browse
def browse_subjects(request, sub_id=0, sub_name=''):
    # create the traversal object
    traversal = TraversalUtils()
    traversal.create_browse(Subject, sub_id, sub_name)

    return render(
        request,
        "subjects/subject_browse.html",
        {'browse_list': traversal.children_subjects,
         'browse_nav': traversal.structured_list,
         'browse_len': len(traversal.structured_list),
         'browse_string': traversal.structured_string},
    )


def detail_subjects(request, sub_id=0):
    # create the traversal object
    traversal = TraversalUtils()
    detailed_subject = Subject.objects.get(id__exact=sub_id)
    traversal.get_structured_list(Subject, detailed_subject)

    return render(
        request,
        "subjects/subject_detail.html",
        {'subject_name': traversal.structured_string,
         'keywords': detailed_subject.keywords,
         'usage': detailed_subject.notes},
    )


# Definition of the SearchForm, used in the Search Tab
class SearchForm(forms.Form):
    # The search box portion of the form
    q = forms.CharField(max_length=100, label='', required=False)


# View: Subjects Search Tab
# Functionality: Creates a list of all children objects of the given node.
# Creates a hierarchical list and strings of all search result subjects using the icontains
# filter.
# Args: [sub_id] - id of the given node to browse [sub_name] - name of the given
# node to browse
def search_subjects(request):
    # query_string = ''

    # create the traversal object
    traversal = TraversalUtils()

    if request.method == 'GET':
        # get the form request data using the GET method
        new_data = request.GET.copy()
        new_data.update(request.FILES)
        form = SearchForm(new_data)
        if form.is_valid():
            # get the value in the search box "q"
            clean_data = form.cleaned_data
            search_item = clean_data['q']

            if search_item is not None and search_item != '':
                # query_structured_list = []
                query_list = []

                # for all subjects returned using the icontains filter, create a hierarchical
                # structured list and also a hyphenated string with that structure
                for query_result in Subject.objects.filter(name__icontains=search_item):
                    traversal.get_structured_list(Subject, query_result)
                    query_list.append(traversal.subject_dict)

                query_list = sorted(query_list, key=itemgetter('hyphenated'))
            else:
                query_list = []
        else:
            query_list = []
    else:
        query_list = []
        # if the form doesn't exist yet, create it
        form = SearchForm()

    return render(
        request,
        "subjects/subject_search.html",
        {'form': form,
         'results_len': len(query_list),
         'search_results': query_list,
         'query_string': search_item},
    )


def about_subjects(request):
    # Get the path of the application
    app_path = subjects.__path__[0]
    # Join the app path and the filename
    about_filepath = os.path.join(app_path, 'about_markdown.txt')
    # Open the file
    try:
        f = open(about_filepath, "r")
    except IOError:
        raise IOError("Couldn't open about_markdown.txt")
    # Get the file data
    about_markdown = f.read()

    return render(
        request,
        "subjects/subject_about.html",
        {
            'about_markdown': about_markdown,
        },
    )


def json_list_subjects(request):
    """View used to return the subjects as a hyphenated json list"""
    subject_list = []

    # create the traversal object
    traversal = TraversalUtils()

    # Makes a list of hierarchical strings (structure show by hyphens) for each node
    # from the root down to the iterated node
    # subject.objects.filter(rght__exact=lft+1)
    for current_subject in Subject.objects.all():
        traversal.get_structured_list(Subject, current_subject)
        subject_list.append(traversal.subject_dict['hyphenated'])

    subject_list = sorted(subject_list)

    return HttpResponse(json.dumps(subject_list), content_type='application/json')
