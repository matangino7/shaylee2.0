from datetime import timezone, datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
import random

class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, blank=False, null=False, validators=[MaxValueValidator(999999999), MinValueValidator(100000000)])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?972\d{8,10}$', message="Israeli phone number must be in the format +972XXXXXXXXX")])
    commander_contact = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?972\d{8,10}$', message="Israeli phone number must be in the format +972XXXXXXXXX")])
    off_day1 = models.DateField(blank=True, null=True)
    off_day2 = models.DateField(blank=True, null=True)
    off_weekend = models.DateField(blank=True, null=True)
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
        self.password = self.generate_random_password()
        if self.birth_date is not None and not isinstance(self.birth_date, str):
            self.birth_date = str(self.birth_date)

            try:
                self.birth_date = datetime.fromisoformat(self.birth_date)
            except (ValueError, TypeError):
                pass

        super(User, self).save(*args, **kwargs)