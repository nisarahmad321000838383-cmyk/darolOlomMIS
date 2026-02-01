"""
Management command to create a super admin user
"""
from django.core.management.base import BaseCommand
from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Create a super admin user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for super admin', default='superadmin')
        parser.add_argument('--password', type=str, help='Password for super admin', default='Admin@123')
        parser.add_argument('--name', type=str, help='Name for super admin', default='Super Admin')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        name = options['name']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return

        user = User.objects.create_superuser(
            username=username,
            password=password,
            name=name
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created super admin: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
