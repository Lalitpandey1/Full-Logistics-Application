from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        User,on_delete=models.CASCADE,
        related_name="created_companies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Distributor(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="distributors"
    )
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="managed_distributors"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.company.name}"


class Store(models.Model):
    distributor = models.ForeignKey(
        Distributor,
        on_delete=models.CASCADE,
        related_name="stores"
    )
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="managed_stores"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.distributor.name}"