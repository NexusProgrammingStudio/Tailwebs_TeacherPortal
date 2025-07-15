from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from Portal.models import Student

class Command(BaseCommand):
    help = 'Seed initial data including superuser and student data'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Create Superuser
        admin_username = 'admin'
        admin_email = 'admin@example.com'
        admin_password = 'admin123'

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser '{admin_username}' created"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{admin_username}' already exists"))

        if Student.objects.exists():
            self.stdout.write(self.style.WARNING("Students already loaded. Skipping."))
            return

        Student.objects.bulk_create([
            Student(name="Sean Abot", subject="Maths", marks=77),
            Student(name="Shawn Tate", subject="English", marks=72),
            Student(name="Shivam", subject="Physics", marks=78),
            Student(name="Mitchelle", subject="Maths", marks=78),
            Student(name="Shiv Yadav", subject="Chemistry", marks=80),
            Student(name="Shiv Yadav", subject="Hindi", marks=76),
            Student(name="Shiv Yadav", subject="Physics", marks=77),
        ])

        self.stdout.write(self.style.SUCCESS("Successfully seeded student data!"))
