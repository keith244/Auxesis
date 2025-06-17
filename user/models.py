from django.db import models
from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Profile (models.Model):
    ROLE_CHOICES = [
        ('SHEPHERD','Shepherd'),
        ('CS','Community Shepherd'),
        ('MLS','Missional Location Shepherd'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices = ROLE_CHOICES)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} -- {self.get_role_display()}" # type: ignore

# class Role (models.Model):
#     name = models.CharField(max_length = 20, choices=[
#         ('SHEPHERD', 'Shepherd'),
#         ('CS', 'Community Shepherd')
#     ],unique=True)

#     def __str__(self):
#         return self.name