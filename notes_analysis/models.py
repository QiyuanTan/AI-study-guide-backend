from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)
    # Add other fields as needed
    syllabus = models.FileField(upload_to='syllabi/', null=True, blank=True)
    
    def __str__(self):
        return self.name