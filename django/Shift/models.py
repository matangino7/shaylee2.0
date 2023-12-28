from django.db import models
from User.models import User
from datetime import date, timedelta
from django.utils import timezone

def default_end_date():
    return timezone.now() + timedelta(days=1)

class Shift(models.Model):
    SHIFT_TYPES = [
        ('A', 'Shift A'),
        ('B', 'Shift B'),
        ('MANNING_POST', 'Manning Post'),
    ]

    first_guard = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_guard_shifts')
    second_guard = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_guard_shifts')
    shift_type = models.CharField(max_length=12, choices=SHIFT_TYPES)

class GuardRound(models.Model):
    start_date = models.DateField(default=timezone.now, unique=True)
    end_date = models.DateField(default=default_end_date, unique=True)
    a_post = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='a_shift_rounds')
    b_post = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='b_shift_rounds')
    manning_post = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='manning_post_rounds')
