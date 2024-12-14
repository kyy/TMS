from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import random
from django.contrib.auth.models import User as UserDjango
from django.utils import timezone
from task.models import Task  # noqa

from tqdm import tqdm

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

User: UserDjango = get_user_model()


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Delete Address instances")
    Task.objects.all().delete()


def create_datatables():
    """Creates an address object combining different elements from the list"""
    name = range(1000)
    status = [_[0] for _ in Task.status.field._choices]
    priority = [_[0] for _ in Task.priority.field._choices]
    visibility = [1, ]
    author = User.objects.values_list("id", flat=True)

    return Task(
        name="Задача №" + str(random.choice(name)),
        status=random.choice(status),
        description="Описание " * 10,
        priority=random.choice(priority),
        visibility=random.choice(visibility),
        author_id=random.choice(author),
        created_at=timezone.now(),
    ).save()


def run_seed(self, mode):
    clear_data()
    if mode == MODE_CLEAR:
        return

    for _ in tqdm(range(50)):
        create_datatables()
