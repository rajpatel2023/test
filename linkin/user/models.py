from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, F, Value, Q

from .choice import profation_choice, marrried_status_choice


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    phonenumber = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to="images/", null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    hobbies = models.CharField(max_length=100, null=True, blank=True)
    profation = models.CharField(
        max_length=100,
        choices=profation_choice,
        null=True,
        blank=True,
    )
    marrid_status = models.CharField(
        max_length=100,
        choices=marrried_status_choice,
        null=True,
        blank=True,
    )
    cast = models.CharField(max_length=100, null=True, blank=True)
    subcast = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} with  phonenumber = {self.phonenumber}"


class matchmodel(models.Model):
    base_user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="re_baseuser"
    )
    match_user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="re_matchuser"
    )

    def __str__(self):
        return f"{self.base_user} is connect with {self.match_user}"
