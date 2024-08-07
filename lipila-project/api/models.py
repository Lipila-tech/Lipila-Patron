from django.db import models
from django.conf import settings


# Global variables
STATUS_CHOICES = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('success', 'success'),
    ('failed', 'failed'),
)


class LipilaDisbursement(models.Model):
    """Stores disbursement data"""
    api_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='disbursements',
                              on_delete=models.CASCADE,
                              null=True, blank=True)
    send_money_to = models.CharField(max_length=30)
    amount = models.FloatField()
    wallet_type = models.CharField(max_length=55)
    reference_id = models.CharField(max_length=120, unique=True, blank=False, null=False)
    processed_date = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['-updated_at']

    def get_reference_id(self):
        return self.reference_id

    def __str__(self):
        return f"Paid - {self.send_money_to} Amount - {self.amount} Status - {self.status}"


class LipilaCollection(models.Model):
    """
    Stores collection data.
    """
    api_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payments_received',
                              on_delete=models.CASCADE, null=True, blank=True)
    payer_account_number = models.CharField(max_length=30)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)
    wallet_type = models.CharField(max_length=55)
    reference_id = models.CharField(max_length=120, unique=True, blank=False, null=False)
    processed_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Payer {self.payer_account_number} Amount - {self.amount} Status {self.status}"
    
    class Meta:
        ordering = ['-updated_at']

    def get_reference_id(self):
        return self.reference_id

