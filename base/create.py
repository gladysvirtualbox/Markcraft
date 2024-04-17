from django.contrib.auth.models import User
from faker import Faker
import random
from .models import Teacher, AddressZW

fake = Faker()



def create_fake_address():
    # Create a fake address
    street = fake.street_address()
    city = fake.city()
    state = fake.state()
    country = fake.country()
    address = AddressZW.objects.create(street=street, city=city, state=state, country=country)
    
    return address

# Usage example:
teacher = create_fake_teacher()
print(teacher)