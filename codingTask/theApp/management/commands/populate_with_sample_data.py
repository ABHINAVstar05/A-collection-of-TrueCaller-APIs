from django.core.management.base import BaseCommand
from theApp.models.users import RegisteredUser, Contact
from theApp.models.spam import Spam
from django.contrib.auth.hashers import make_password
import random


class Command(BaseCommand) :
    help = 'Populate sample data for testing'

    def handle(self, *args, **kwargs) :
        self.populate_RegisteredUser()
        self.populate_Contact()
        self.populate_Spam()

    def populate_RegisteredUser(self) :
        for i in range(10) :
            RegisteredUser.objects.create(
                name = f"User {i+1}",
                phone_number = f"123456780{i}",
                email = f"user_{i+1}@example.com",
                password = make_password(f"password@{i}")
            )

        self.stdout.write(self.style.SUCCESS('Sample RegisteredUsers created successfully.'))

    def populate_Contact(self) : 
        for i in range(10) :
            contact = Contact.objects.create(
                name = f"Contact {i+1}",
                phone_number = f"23456789{i}"
            )

            # To add random 1 to 5 registered users to contacts
            random_users = random.sample(list(RegisteredUser.objects.all()), random.randint(1, 5))
            for user in random_users :
                contact.users.add(user)
        
        self.stdout.write(self.style.SUCCESS('Sample Contacts created successfully.'))

    def populate_Spam(self) :
        added_phone_numbers = set()

        for i in range(20) :
            phone_numbers = set()

            # To add phone numbers from RegisteredUser
            registered_users = RegisteredUser.objects.all()
            selected_registered_users = random.sample(list(registered_users), random.randint(1, 3))
            for user in selected_registered_users :
                phone_numbers.add(user.phone_number)

            # To add phone numbers from Contact
            contacts = Contact.objects.all()
            selected_contacts = random.sample(list(contacts), random.randint(1, 3))
            for contact in selected_contacts :
                phone_numbers.add(contact.phone_number)

            # To add random phone numbers    
            if i < 10 :
                random_number = f"12345678{i}0"
            else :
                random_number = f"12345678{i}"
            phone_numbers.add(random_number)

            # To remove already added phone numbers
            phone_numbers -= added_phone_numbers

            # Create Spam instances
            for phone_number in phone_numbers:
                Spam.objects.create(
                    phone_number = phone_number,
                    spam_reported_count = random.randint(1, 6)
                )

                # To add the phone number to the set of added phone numbers
                added_phone_numbers.add(phone_number)

        self.stdout.write(self.style.SUCCESS('Sample Spam reports created successfully.'))
