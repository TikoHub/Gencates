from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from game.models import IncomeRoom, CatyCoin


class Command(BaseCommand):
    help = 'Create initial data for users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not IncomeRoom.objects.filter(user=user).exists():
                IncomeRoom.objects.create(user=user, name='Income Room 1')
            if not CatyCoin.objects.filter(user=user).exists():
                CatyCoin.objects.create(user=user, balance=100)
        self.stdout.write(self.style.SUCCESS('Successfully created initial data for users'))
