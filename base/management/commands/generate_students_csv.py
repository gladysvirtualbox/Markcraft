import csv
import os
from django.core.management.base import BaseCommand
from base.models import Student

class Command(BaseCommand):
    help = 'Generate CSV file with 500 students'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.getcwd(), 'students.csv')
        
        with open(file_path, mode='w', newline='') as csv_file:
            fieldnames = ['Student ID', 'First Name', 'Last Name', 'Gender', 'National ID', 'Phone Number']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            writer.writeheader()
            
            # Generate 500 students and write to CSV
            for i in range(1, 501):
                student_id = f'ST{i}'
                first_name = f'John{i}'
                last_name = f'Doe{i}'
                gender = 'M' if i % 2 == 0 else 'F'
                national_id = f'123456{i:03}'
                phone_number = f'123456{i:03}'
                
                writer.writerow({
                    'Student ID': student_id,
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Gender': gender,
                    'National ID': national_id,
                    'Phone Number': phone_number
                })

        self.stdout.write(self.style.SUCCESS(f'Successfully generated CSV file: {file_path}'))
