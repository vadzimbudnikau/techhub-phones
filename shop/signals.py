from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a user profile when a new user is created.

    Args:
        sender (User): The sender model of the signal.
        instance (User): The instance of the newly created User.
        created (bool): Indicates whether the instance was just created.
        **kwargs: Additional keyword arguments.

    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save the user profile when the associated User instance is saved.

    Args:
        sender (User): The sender model of the signal.
        instance (User): The instance of the User being saved.
        **kwargs: Additional keyword arguments.

    """
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()
