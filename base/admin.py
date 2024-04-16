from django.contrib import admin
from .models import Student

# Register your models here.
# admin.site.register(Student)
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
     list_display=['name', 'surname', 'program']
     list_filter=['course', 'program']

# Register the admin class with the associated model
admin.site.register(Student, AuthorAdmin)
