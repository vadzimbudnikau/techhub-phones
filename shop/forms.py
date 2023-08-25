from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    A form to edit user profile information.

    This form is based on the UserProfile model and allows users to update their
    avatar, gender, phone number, email, and card details.

    Attributes:
        model (UserProfile): The UserProfile model class associated with the form.
        fields (tuple): A tuple specifying the fields to include in the form.

    """

    class Meta:
        model = UserProfile
        fields = ('avatar', 'gender', 'phone', 'email', 'card_details')
