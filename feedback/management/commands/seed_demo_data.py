import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from feedback.models import Category, Feedback, StudentProfile

CATEGORIES = [
    ('Course Content', 'Feedback about syllabus, materials, and course structure.'),
    ('Faculty', 'Feedback about teaching staff and instruction quality.'),
    ('Facilities', 'Feedback about classrooms, labs, and campus infrastructure.'),
    ('Administration', 'Feedback about office processes and student services.'),
    ('Events', 'Feedback about workshops, seminars, and campus events.'),
]

SAMPLE_SUBJECTS = [
    'Great use of real-world examples in lectures',
    'Lab equipment often out of order',
    'Timetable clashes between electives',
    'Excellent support from the placement cell',
    'Library needs more updated reference books',
    'Wi-Fi connectivity issues in hostel blocks',
    'Would love more hands-on project time',
    'Grading turnaround could be faster',
    'Canteen food quality has improved a lot',
    'Request for more online submission options',
]


class Command(BaseCommand):
    help = 'Seeds the database with demo categories, students, and feedback for local testing.'

    def add_arguments(self, parser):
        parser.add_argument('--students', type=int, default=8, help='Number of demo student accounts to create.')
        parser.add_argument('--feedback', type=int, default=25, help='Number of demo feedback entries to create.')

    def handle(self, *args, **options):
        categories = []
        for name, description in CATEGORIES:
            category, _ = Category.objects.get_or_create(name=name, defaults={'description': description})
            categories.append(category)
        self.stdout.write(self.style.SUCCESS(f'Ensured {len(categories)} categories exist.'))

        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'ChangeMe123!')
            self.stdout.write(self.style.SUCCESS('Created superuser "admin" / password "ChangeMe123!" — change this immediately.'))
        else:
            admin = User.objects.get(username='admin')

        students = []
        for i in range(1, options['students'] + 1):
            username = f'student{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'first_name': f'Student', 'last_name': str(i), 'email': f'{username}@example.com'},
            )
            if created:
                user.set_password('ChangeMe123!')
                user.save()
                StudentProfile.objects.create(user=user, roll_number=f'ROLL{1000 + i}', department='Computer Science', year_of_study=random.randint(1, 4))
            students.append(user)
        self.stdout.write(self.style.SUCCESS(f'Ensured {len(students)} demo student accounts exist (password: ChangeMe123!).'))

        created_count = 0
        for _ in range(options['feedback']):
            Feedback.objects.create(
                student=random.choice(students),
                category=random.choice(categories),
                subject=random.choice(SAMPLE_SUBJECTS),
                message='This is sample demo feedback generated for local testing purposes.',
                rating=random.randint(1, 5),
                is_anonymous=random.random() < 0.2,
                status=random.choice([Feedback.STATUS_PENDING, Feedback.STATUS_REVIEWED, Feedback.STATUS_RESOLVED]),
            )
            created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} demo feedback entries.'))
        self.stdout.write(self.style.WARNING(f'Superuser login: admin / ChangeMe123!'))
