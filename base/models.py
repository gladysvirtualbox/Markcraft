from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class AddressZW(models.Model):
    """
    Represents a Zimbabwean address.
    """
    address_line_1 = models.CharField(max_length=255, help_text="First line of the address.")
    address_line_2 = models.CharField(max_length=255, blank=True, help_text="Second line of the address (optional).")
    city = models.CharField(max_length=100, help_text="City of the address.")
    province = models.CharField(max_length=100, help_text="Province of the address.")
    postal_code = models.CharField(max_length=20, help_text="Postal code of the address.")

    def __str__(self):
        """
        Returns a string representation of the address.
        """
        address_lines = self.address_line_1
        if self.address_line_2:
            address_lines += f"\n{self.address_line_2}"
        return f"{address_lines}\n{self.city}, {self.province} ({self.postal_code})"


class Stream(models.Model):
    """
    Represents an academic stream or cohort.
    """
    name = models.CharField(max_length=100, help_text="Name of the stream.")
    start_date = models.DateField(help_text="Start date of the stream.")
    end_date = models.DateField(help_text="End date of the stream.")

    def __str__(self):
        """
        Returns a string representation of the stream.
        """
        return self.name

    def is_active(self):
        """
        Checks if the stream is currently active based on the start and end dates.
        Returns True if active, False otherwise.
        """
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def duration(self):
        """
        Calculates the duration of the stream in days.
        Returns an integer representing the duration.
        """
        return (self.end_date - self.start_date).days

    def upcoming_streams(self):
        """
        Retrieves streams that are scheduled to start in the future.
        Returns a queryset of upcoming streams.
        """
        today = timezone.now().date()
        return Stream.objects.filter(start_date__gte=today).order_by('start_date')

    def past_streams(self):
        """
        Retrieves streams that have already ended.
        Returns a queryset of past streams.
        """
        today = timezone.now().date()
        return Stream.objects.filter(end_date__lt=today).order_by('-end_date')

    def current_streams(self):
        """
        Retrieves streams that are currently active.
        Returns a queryset of current streams.
        """
        today = timezone.now().date()
        return Stream.objects.filter(start_date__lte=today, end_date__gte=today)
        

class Course(models.Model):
    """
    Represents a course offered in an educational program.
    """
    code = models.CharField(max_length=20, unique=True, help_text="Unique code for the course.")
    name = models.CharField(max_length=120, help_text="Name of the course.")
    description = models.TextField(blank=True, help_text="Description of the course.")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the course was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the course was last updated.")

    def __str__(self):
        """
        Returns a string representation of the course.
        """
        return f"{self.code} - {self.name}"

    def total_students(self):
        """
        Calculates the total number of students enrolled in the course.
        Returns an integer representing the total number of students.
        """
        return self.student_set.count()

    def average_mark(self):
        """
        Calculates the average mark of students enrolled in the course.
        Returns a float representing the average mark.
        """
        marks = self.mark_set.all()
        if marks.exists():
            total_marks = sum([float(mark.marks) for mark in marks])
            return total_marks / len(marks)
        else:
            return 0.0

    def recent_marks(self, num=5):
        """
        Retrieves the most recent marks recorded for the course.
        Parameters:
            - num (int): Number of recent marks to retrieve (default is 5).
        Returns a queryset of recent marks.
        """
        return self.mark_set.all().order_by('-recorded_at')[:num]

    def enroll_student(self, student):
        """
        Enrolls a student in the course.
        Parameters:
            - student (Student): Student object to enroll in the course.
        """
        self.student_set.add(student)

    def remove_student(self, student):
        """
        Removes a student from the course.
        Parameters:
            - student (Student): Student object to remove from the course.
        """
        self.student_set.remove(student)

class Program(models.Model):
    """
    Represents an educational program offered by an institution.
    """
    name = models.CharField(max_length=120, help_text="Name of the program.")
    description = models.TextField(blank=True, help_text="Description of the program.")
    courses = models.ManyToManyField('Course', help_text="Courses included in the program.")

    def __str__(self):
        """
        Returns a string representation of the program.
        """
        return self.name

    def total_courses(self):
        """
        Calculates the total number of courses included in the program.
        Returns an integer representing the total number of courses.
        """
        return self.courses.count()

    def enrolled_students(self):
        """
        Retrieves the students enrolled in the program.
        Returns a queryset of enrolled students.
        """
        return Student.objects.filter(program=self)

class Student(models.Model):
    """
    Represents a student enrolled in an educational program.
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    student_id = models.CharField(max_length=100, help_text="Student ID.")
    first_name = models.CharField(max_length=100, help_text="First name of the student.")
    last_name = models.CharField(max_length=100, help_text="Last name of the student.")
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True,
                                help_text="Program in which the student is enrolled.")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text="Gender of the student.")
    national_id = models.CharField(max_length=20, unique=True, help_text="National ID of the student.")
    address = models.ForeignKey(AddressZW, on_delete=models.CASCADE, help_text="Address of the student.")
    phone_number = models.CharField(max_length=15, help_text="Phone number of the student.")
    parent_name = models.CharField(max_length=100, help_text="Name of the student's parent/guardian.")
    parent_phone_number = models.CharField(max_length=15, help_text="Phone number of the student's parent/guardian.")
    class_year = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True,
                                   help_text="Class year/stream of the student.")

    def __str__(self):
        """
        Returns a string representation of the student.
        """
        return f"{self.first_name} {self.last_name}"

    def marks(self):
        """
        Retrieves the marks obtained by the student in various courses.
        Returns a queryset of marks.
        """
        return Mark.objects.filter(student=self)

class Teacher(models.Model):
    """
    Represents a teacher in an educational institution.
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="User associated with the teacher.")
    date_of_birth = models.DateField(help_text="Date of birth of the teacher.")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, help_text="Gender of the teacher.")
    national_id = models.CharField(max_length=20, unique=True, help_text="National ID of the teacher.")
    phone_number = models.CharField(max_length=20, help_text="Phone number of the teacher.")
    address = models.ForeignKey(AddressZW, null=True, blank=True, on_delete=models.CASCADE,
                                help_text="Address of the teacher.")
    qualifications = models.TextField(help_text="Qualifications of the teacher.")
    years_of_experience = models.PositiveIntegerField(help_text="Years of experience of the teacher.")

    def __str__(self):
        """
        Returns a string representation of the teacher.
        """
        return f"{self.user.first_name} {self.user.last_name}"

    def assigned_courses(self):
        """
        Retrieves the courses assigned to the teacher.
        Returns a queryset of assigned courses.
        """
        return Course.objects.filter(teacher=self)
    
    def average_student_mark(self):
        """
        Calculates the average mark of students associated with the courses taught by the teacher.
        Returns a float representing the average mark.
        """
        total_marks = 0
        total_students = 0
        for student in self.students():
            for mark in student.marks():
                total_marks += mark.mark
                total_students += 1
        if total_students > 0:
            return total_marks / total_students
        else:
            return 0.0
        

    def recent_marks(self, num=5):
        """
        Retrieves the most recent marks recorded for the students associated with the courses taught by the teacher.
        Parameters:
            - num (int): Number of recent marks to retrieve (default is 5).
        Returns a queryset of recent marks.
        """
        recent_marks = []
        for student in self.students():
            recent_marks.extend(student.marks().order_by('-recorded_at')[:num])
        return recent_marks

class Mark(models.Model):
    """
    Represents a mark recorded for a student in a course by a teacher.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, help_text="Student associated with the mark.")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, help_text="Course associated with the mark.")
    mark = models.DecimalField(max_digits=5, decimal_places=2, help_text="Mark recorded for the student.")
    recorded_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the mark was recorded.")
    file_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', help_text="Upload file with student marks.", null=True)
    
    def __str__(self):
        """
        Returns a string representation of the mark.
        """
        return f"{self.student} - {self.course}: {self.mark}"
