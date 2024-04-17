import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from base.models import AddressZW, Stream, Course, Program, Student, Teacher, Mark

fake = Faker()


class Command(BaseCommand):
    help = 'Populates the database with random data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of records to create')

    def handle(self, *args, **options):
        count = options['count']

        for _ in range(count):
            # self.create_address()
            # self.create_stream()
            # self.create_course()
            # self.create_program()
            self.create_student()
            # self.create_teacher()
            # self.create_mark()

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {count} records.'))

    def create_address(self):
        address_line_1 = fake.street_address()
        address_line_2 = fake.secondary_address() if random.choice([True, False]) else ''
        city = fake.city()
        province = fake.state()
        postal_code = fake.zipcode()

        AddressZW.objects.create(
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            province=province,
            postal_code=postal_code
        )

    def create_stream(self):
        name = fake.word()
        start_date = fake.date_between(start_date='-1y', end_date='-1d')
        end_date = fake.date_between(start_date='+1d', end_date='+1y')

        Stream.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date
        )

    def create_course(self):
        code = fake.unique.random_number(digits=5)
        name = fake.catch_phrase()
        description = fake.paragraph()

        Course.objects.create(
            code=code,
            name=name,
            description=description
        )

    def create_program(self):
        name = fake.job()
        description = fake.paragraph()
        courses = Course.objects.order_by('?')[:random.randint(1, 5)]

        program = Program.objects.create(
            name=name,
            description=description
        )

        program.courses.set(courses)

    def create_student(self):
        gender = random.choice(['M', 'F'])
        first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
        last_name = fake.last_name()
        program = Program.objects.order_by('?').first()
        print(program)
        national_id = fake.unique.random_number(digits=10)
        address = AddressZW.objects.order_by('?').first()
        phone_number = fake.phone_number()
        parent_name = fake.name()
        parent_phone_number = fake.phone_number()
        class_year = Stream.objects.order_by('?').first()

        Student.objects.create(
            student_id=fake.unique.random_number(digits=8),
            first_name=first_name,
            last_name=last_name,
            program=program,
            gender=gender,
            national_id=national_id,
            address=address,
            phone_number=phone_number,
            parent_name=parent_name,
            parent_phone_number=parent_phone_number,
            class_year=class_year,
        )

    def create_teacher(self):
        # Create a fake user
        username = fake.user_name()
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = fake.password()
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        
        # Create a fake teacher
        date_of_birth = fake.date_of_birth(minimum_age=25, maximum_age=65)
        gender = random.choice(['M', 'F'])
        national_id = fake.unique.random_number(digits=10)
        phone_number = fake.phone_number()
        address = self.create_address()  # Use self.create_address() to avoid infinite recursion
        qualifications = fake.paragraph()
        years_of_experience = random.randint(1, 20)
        
        Teacher.objects.create(user=user, date_of_birth=date_of_birth, gender=gender, national_id=national_id,
                                            phone_number=phone_number, address=address, qualifications=qualifications,
                                            years_of_experience=years_of_experience)
        

        def create_mark(self):
            student = Student.objects.order_by('?').first()
            course = Course.objects.order_by('?').first()
            mark = random.randint(0, 100)

            Mark.objects.create(
                student=student,
                course=course,
                mark=mark
            )
