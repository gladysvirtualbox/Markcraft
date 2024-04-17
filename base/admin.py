from django.contrib import admin
from .models import AddressZW, Stream, Course, Program, Student, Teacher, Mark


class AddressZWAdmin(admin.ModelAdmin):
    list_display = ['address_line_1', 'city', 'province', 'postal_code']
    search_fields = ['address_line_1', 'city', 'province', 'postal_code']

class StreamAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_active']
    list_filter = ['start_date', 'end_date']
    search_fields = ['name']
    date_hierarchy = 'start_date'

class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['code', 'name', 'description']

class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'total_courses']
    search_fields = ['name', 'description']
    filter_horizontal = ['courses']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'program', 'gender', 'national_id', 'phone_number']
    list_filter = ['program', 'gender', 'class_year']
    search_fields = ['student_id', 'first_name', 'last_name', 'national_id', 'phone_number']

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'gender', 'national_id', 'phone_number', 'address', 'qualifications', 'years_of_experience']
    list_filter = ['gender']
    search_fields = ['user__first_name', 'user__last_name', 'national_id', 'phone_number']

class MarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'mark', 'recorded_at']
    list_filter = ['course',]
    search_fields = ['student__first_name', 'student__last_name']

# Register your models with the custom admin classes
admin.site.register(AddressZW, AddressZWAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Mark, MarkAdmin)

