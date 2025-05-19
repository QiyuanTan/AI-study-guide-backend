from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.CharField(max_length=50)
    syllabus = models.FileField(upload_to='syllabi/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Note(models.Model):
    course = models.ForeignKey(Course, related_name='notes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title