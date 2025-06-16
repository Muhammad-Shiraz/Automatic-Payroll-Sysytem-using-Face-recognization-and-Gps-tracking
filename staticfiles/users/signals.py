from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    """Ensure 'Employee' and 'HR' groups exist after migrations."""
    if sender.name == 'django.contrib.auth':  # Only run after auth app migrations
        Group.objects.get_or_create(name='Employee')
        Group.objects.get_or_create(name='HR')
