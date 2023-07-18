from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import re
from .models import Profile
from django.forms import ValidationError
from datetime import date


class Usersignup(UserCreationForm):
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password1")
        email_validate = re.search(r"^[\w]+@([\w-]+\.)+[\w-]{2,4}$", str(email))
        if email_validate is None:
            raise ValidationError({"email": "Email NOT Match Regex"})
        password_validate = (
            r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])(?=.*[a-zA-Z]).{8,}$",
            str(password),
        )
        if password_validate is None:
            raise ValidationError({"password1": "password NOT Match Regex"})
        return cleaned_data

    def save(self):
        userobj = super().save()
        Profile.objects.create(user=userobj)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class userprofileform(forms.ModelForm):
    def calculate_age(self, born):
        today = date.today()
        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )

    def clean(self):
        cleaned_data = super().clean()
        # hobbies
        if cleaned_data["hobbies"]:
            hobbies = cleaned_data["hobbies"]
            list_of_hobbies = list(hobbies.split(" "))
            if len(list_of_hobbies) < 3:
                raise ValidationError(
                    {"hobbies": "Enter Alteast 3 hobbies in betweeen space"}
                )
        # phonenumber
        if cleaned_data["phonenumber"]:
            phonenumber = cleaned_data.get("phonenumber")
            phonenumber_validate = re.search(r"^[0-9]{10}$", str(phonenumber))
            if phonenumber_validate is None:
                raise ValidationError(
                    {"phonenumber": "Phone Number Must contect 10 digit"}
                )
            hobbies = cleaned_data.get("hobbies")
        # age
        if cleaned_data["date_of_birth"]:
            cleaned_data["age"] = self.calculate_age(cleaned_data["date_of_birth"])
        return cleaned_data

    class Meta:
        model = Profile
        exclude = ("user",)
        widgets = {"age": forms.HiddenInput()}
