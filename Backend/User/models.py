from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
import random

class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, blank=False, null=False, validators=[MaxValueValidator(999999999), MinValueValidator(100000000)])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateTimeField(null=True, help_text="Format: dd-mm-yyyy")
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?972\d{8,10}$', message="Israeli phone number must be in the format +972XXXXXXXXX")])
    commander_contact = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?972\d{8,10}$', message="Israeli phone number must be in the format +972XXXXXXXXX")])
    off_day1 = models.CharField(max_length=10, blank=True, help_text="Format: dd-mm-yyyy")
    off_day2 = models.CharField(max_length=10, blank=True, help_text="Format: dd-mm-yyyy")
    off_weekend = models.BooleanField(default=False, help_text="Format: dd-mm-yyyy")
    password = models.CharField(max_length=10, default='')
    month_frequency = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    b_objection=models.BooleanField(default=False)
    lieutenant=models.BooleanField(default=False)

    def generate_random_password(self):
        return str(random.randint(1000000000, 9999999999))

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = self.generate_random_password()
        super(User, self).save(*args, **kwargs)
