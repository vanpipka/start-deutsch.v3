from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Test
from .utils.tests_counter import rebuild_test_counters


@receiver(post_save, sender=Test)
def update_counter_on_save(sender, instance, **kwargs):
    rebuild_test_counters()


@receiver(post_delete, sender=Test)
def update_counter_on_delete(sender, instance, **kwargs):
    rebuild_test_counters()