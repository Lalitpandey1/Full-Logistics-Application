from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ("COMPANY_ADMIN", "Company Admin"),
        ("DISTRIBUTOR_MANAGER", "Distributor Manager"),
        ("STORE_MANAGER", "Store Manager"),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"