from django.db import models
from apps.users.models import UserModel


class Payment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.provider} - {self.status}"
