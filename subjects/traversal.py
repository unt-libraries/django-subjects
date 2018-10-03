class TraversalUtils:
    def __init__(self):
        self.structured_list = []

    #Recursively recreate the traversal structure when a new subject is added.
    def rebuild_tree(self, subject, parent, left):
        right = left + 1

        #Grabs the children objects of the parent node
        children_subjects = subject.objects.filter(parent__exact=parent)

        #Recurses through each child node to change their traversal numbers
        for row in children_subjects:
            right = self.rebuild_tree(subject, row.id, right)

        #Updates the parents left and right traversal
        if parent != 0:
           p = subject.objects.get(id__exact=parent)
           p.lft = left
           p.rght = right
           try:
               p.save()
           except:
               pass

        return right+1

    #Functionality: Creates a list of parent objects of the browse_subject(child) object. The list is comprised
    #of every parent's parent from the browse_subject node(child) to the root node.
    #Args: [current_object] - a model object [browse_subject] - table row object(s) 
    def get_structured_list(self, current_object, browse_subject):
        self.structured_list = []
        self.structured_string = ''

        #This statment is equivalent to:
        #SELECT name from widget_subject where lft <= (left traversal) and rght >= (right traversal) order by lft ASC;
        #Grabs all parent objects from the browse_subject all the way up to the root
        parent_subjects = current_object.objects.filter(lft__lte=browse_subject.lft, rght__gte=browse_subject.rght).order_by('lft')

        #Creates a list of the parents
        for current_parent in parent_subjects:
            self.structured_list.append(current_parent)
            #Create a hierarchical string, denoted with hyphens
            if self.structured_string == '':
                self.structured_string = "%s" % (current_parent.name)
            else:
                self.structured_string = "%s - %s" % (self.structured_string, current_parent.name)

        self.subject_dict = {
            'hyphenated': self.structured_string,
            'subject_object': browse_subject,
            }
    
    def create_browse(self, subject, subject_id, subject_name):

        if subject_id != '' and subject_id != None and subject_name == '':
            if subject_id != 0:
                #Grabs the row object of the given node
                current_subject = subject.objects.get(id__exact=subject_id)
            #Grabs the children objects of the given node
            self.children_subjects = subject.objects.filter(parent__exact=subject_id).order_by('name')
        elif subject_name != '' and subject_name != None:
            #Grabs the row object of the given node
            current_subject = subject.objects.get(name__exact=subject_name)
            subject_id = current_subject.id
            #Grabs the children objects of the given node
            self.children_subjects = subject.objects.filter(parent__exact=subject_id).order_by('name')

        self.structured_list = []

        if subject_id != 0 or subject_name != '':
            #Create a hierarchical string of the current browse subject
            self.get_structured_list(subject, current_subject)
        else:
            self.structured_string = ''
