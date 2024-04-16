from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Avg

from .models import Course, Mark, Student, Teacher

@login_required
def teacher_home(request):
    # Retrieve the teacher associated with the current user
    teacher = get_object_or_404(Teacher, user=request.user)
    
    # Retrieve all courses taught by the teacher
    courses = Course.objects.filter(teacher=teacher)
    
    # Calculate total students across all courses
    total_students = Student.objects.filter(course__in=courses).count()
    
    # Calculate total subjects (courses) taught by the teacher
    total_subjects = courses.count()
    
    # Retrieve the average mark of students associated with the courses taught by the teacher
    average_student_mark = Mark.objects.filter(course__in=courses).aggregate(Avg('mark'))['mark__avg']
    
    # Retrieve recent marks recorded for students associated with the courses taught by the teacher
    recent_marks = Mark.objects.filter(course__in=courses).order_by('-recorded_at')[:5]
    
    # Construct context data
    context = {
        'page_title': f'Teacher Panel - {teacher.user.last_name} ({teacher.course})',
        'total_students': total_students,
        'total_subjects': total_subjects,
        'average_student_mark': average_student_mark,
        'recent_marks': recent_marks,
    }
    
    # Render the template with the context data
    return render(request, 'home_content.html', context)
