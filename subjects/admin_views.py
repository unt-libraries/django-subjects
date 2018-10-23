from subjects.models import Subject
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.views import redirect_to_login
from django import forms
from django.forms.widgets import *
from django.views.decorators.csrf import csrf_protect
from subjects.traversal import TraversalUtils

class AddSubject(forms.Form):
    #The Add Subject form
    name = forms.CharField(max_length=100, label='', required=True)
    keywords = forms.CharField(widget=Textarea(attrs={'cols': 70, 'rows': 5}), label='', required=False)
    notes = forms.CharField(widget=Textarea(attrs={'cols': 70, 'rows': 5}), label='', required=False)

class ModifySubject(forms.Form):
    #The Modify Subject form
    keywords = forms.CharField(widget=Textarea(attrs={'cols': 70, 'rows': 5}), label='', required=False)
    notes = forms.CharField(widget=Textarea(attrs={'cols': 70, 'rows': 5}), label='', required=False)

@csrf_protect
def subject_add(request, sub_id=0, sub_name=''):
    #create the traversal object
    traversal = TraversalUtils()
    if not request.user.is_authenticated():
        redirect_to_login(request.path, login_url='subject/login')
    traversal.create_browse(Subject, sub_id, sub_name)
    s = None

    if request.method == 'POST':
        #get the form request data using the POST method
        new_data = request.POST.copy()
        new_data.update(request.FILES)
        form = AddSubject(new_data)
        if form.is_valid():
            #get the values of the form and save them
            clean_data = form.cleaned_data 
            s = Subject(name=clean_data['name'], keywords=clean_data['keywords'], notes=clean_data['notes'], \
                        parent=sub_id, lft=1, rght=2)
            s.save()
            traversal.rebuild_tree(Subject, 0, 0)
    else:
        #if the form doesn't exist yet, create it
        form = AddSubject()

    return render(
        request,
        "subjects/add_subject.html",
        {'form' : form,
         'browse_list' : traversal.children_subjects,
         'browse_nav' : traversal.structured_list,
         'browse_len' : len(traversal.structured_list),
         'browse_string' : traversal.structured_string,
         'saved' : s},
    )
subject_add = permission_required('subjects.add_subject')(subject_add)

def subject_delete(request, sub_id=0, sub_name='', sub_delete=False):
    #create the traversal object
    traversal = TraversalUtils()
    
    if not request.user.is_authenticated():
        redirect_to_login(request.path, login_url='subject/login')
    if sub_delete == False:
        traversal.create_browse(Subject, sub_id, sub_name)
    elif sub_delete == True and sub_id != 0:
        traversal.create_browse(Subject, sub_id, sub_name)
        traversal.children_subjects = "Deleted"
    
    if sub_id != 0:
        delete_subject = Subject.objects.get(id__exact=sub_id)
    else:
        delete_subject = ''
    child_err = None
    
    if sub_delete == True:
        #Delete the subject, if it has no children
        if int(delete_subject.rght) == (int(delete_subject.lft) + 1):
            delete_subject.delete()
            traversal.rebuild_tree(Subject, 0, 0)
            child_err = 2
        else:
            child_err = 1

    return render(
        request,
        "subjects/delete_subject.html",
        {'browse_list' : traversal.children_subjects,
         'browse_nav' : traversal.structured_list,
         'browse_len' : len(traversal.structured_list),
         'browse_string' : traversal.structured_string,
         'current_subject' : delete_subject,
         'child_error' : child_err},
    )
subject_delete = permission_required('subjects.delete_subject')(subject_delete)

@csrf_protect
def subject_modify(request, sub_id=0, sub_name=''):
    #create the traversal object
    traversal = TraversalUtils()
    
    if not request.user.is_authenticated():
        redirect_to_login(request.path, login_url='subject/login')
    traversal.create_browse(Subject, sub_id, sub_name)
    no_form = False
    modified_subject = current_subject = data = None
    if sub_id != 0:
        current_subject = Subject.objects.get(id__exact=sub_id)
        data = {'keywords' : current_subject.keywords,
                'notes' : current_subject.notes}

    if request.method == 'POST':
        #get the form request data using the POST method
        new_data = request.POST.copy()
        new_data.update(request.FILES)
        form = ModifySubject(new_data)
        if form.is_valid():
            #get the values of the form and save them
            clean_data = form.cleaned_data
            modified_subject = current_subject
            modified_subject.keywords = clean_data['keywords']
            modified_subject.notes = clean_data['notes']
            modified_subject.save()

    else:
        #if the form doesn't exist yet, create it, but only if it's not the main level
        form = ModifySubject(data)

    return render(
        request,
        "subjects/modify_subject.html",
        {'form' : form,
         'browse_list' : traversal.children_subjects,
         'browse_nav' : traversal.structured_list,
         'browse_len' : len(traversal.structured_list),
         'browse_string' : traversal.structured_string,
         'selected_subject' : current_subject,
         'modified' : modified_subject},
    )
subject_modify = permission_required('subjects.change_subject')(subject_modify)
