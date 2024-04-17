from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MarkUploadForm
from .models import Mark, Student, Course
import csv

def upload_marks(request):
    if request.method == 'POST':
        form = MarkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if not file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
                return redirect('upload_marks')
            
            try:
                # Process the CSV file
                decoded_file = file.read().decode('utf-8')
                csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
                
                # Check if the CSV file is not empty
                if len(list(csv_data)) < 2:
                    messages.error(request, 'The CSV file is empty or does not contain valid data.')
                    return redirect('upload_marks')
                
                # Reset the file cursor to the beginning for iteration
                file.seek(0)
                
                for row in csv_data:
                    # Assuming CSV format: student_id, course_code, mark
                    student_id, course_code, mark_value = row
                    student = Student.objects.get(student_id=student_id)
                    course = Course.objects.get(code=course_code)
                    Mark.objects.create(student=student, course=course, mark=mark_value)
                    
                messages.success(request, 'File uploaded successfully.')
                return redirect('upload_marks')
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {e}')
                return redirect('upload_marks')
    else:
        form = MarkUploadForm()
    return render(request, 'upload_marks.html', {'form': form})
