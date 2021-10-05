from datetime import date

from django.core.management.base import BaseCommand

from online_journal.models import Post


class Command(BaseCommand):
    help = 'Reset post rating fields'

    def handle(self, *args, **options):
        today = date.today()
        Post.objects.update(daily_rating=0)
        if today.day == 1:
            Post.objects.update(monthly_rating=0)
            if today.month == 1:
                Post.objects.update(yearly_rating=0)