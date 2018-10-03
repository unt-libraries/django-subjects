from django.db import models

#subjects Model
class Subject(models.Model):
    name = models.TextField(editable=False)
    parent = models.IntegerField(editable=False, default=0)
    lft = models.IntegerField('left Traversal')
    rght = models.IntegerField('right Traversal')
    keywords = models.TextField()
    notes = models.TextField()
    
    def __str__(self):
        return self.name
