from django.db import models
from django.conf import settings
from accounts.models import CreatorProfile
from api.utils import generate_reference_id

from accounts.globals import (
    CITY_CHOICES, STATUS_CHOICES, CREATOR_CATEGORY_CHOICES,
    ISP_CHOICES)


ONETIME_AMOUNT = 100
FAN_AMOUNT = 25
SUPERFAN_AMOUNT = 50


class Tier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        CreatorProfile, on_delete=models.CASCADE, related_name='tiers')
    updated_at = models.DateTimeField(auto_now=True)
    visible_to_fans = models.BooleanField(default=True)

    @classmethod
    def create_default_tiers(cls, creator):
        # Create default tiers if they don't exist
        defaults = [
            {"name": "Onetime", "price": ONETIME_AMOUNT,
                "desc": "Make a one-time Contribution to support the creator's work.",
                'creator': creator, 'visible': True},
            {"name": "Fan", "price": FAN_AMOUNT,
                "desc": "Support the creator and get access to exclusive content.",
                'creator': creator, 'visible': True},
            {"name": "Superfan", "price": SUPERFAN_AMOUNT,
                "desc": "Enjoy additional perks and behind-the-scenes content.",
                'creator': creator, 'visible': True}
        ]
        for tier_data in defaults:
            Tier.objects.create(
                name=tier_data["name"],
                description=tier_data["desc"],
                price=tier_data['price'],
                creator=tier_data['creator'],
                visible_to_fans=tier_data['visible']
            )

    def __str__(self):
        return f"{self.name}"


class TierSubscriptions(models.Model):
    patron = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    tier = models.ForeignKey(
        Tier, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f"{self.tier}"


class Transfer(models.Model):
    payer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tranfers')
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=False)
    payer_account_number = models.CharField(
        max_length=300, null=True, blank=False)
    send_money_to = models.CharField(max_length=300, null=True, blank=False)
    reference_id = models.CharField(
        max_length=40, unique=True, blank=False, null=False)
    wallet_type = models.CharField(
        max_length=20, choices=ISP_CHOICES, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')


class SubscriptionPayments(models.Model):
    payee = models.ForeignKey(
        TierSubscriptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=True)
    payer_account_number = models.CharField(
        max_length=300, blank=False, null=False)
    reference_id = models.CharField(
        max_length=40, unique=True, blank=False, null=False)
    wallet_type = models.CharField(
        max_length=20, choices=ISP_CHOICES, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.reference_id}"


class Contributions(models.Model):
    payee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='contributions_received')
    payer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='contributions_sent')
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=False)
    payer_account_number = models.CharField(
        max_length=300, null=True, blank=False)
    reference_id = models.CharField(
        max_length=40, unique=True, blank=False, null=False)
    wallet_type = models.CharField(
        max_length=20, choices=ISP_CHOICES, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.amount}"


class WithdrawalRequest(models.Model):
    processed_date = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(
        CreatorProfile, on_delete=models.CASCADE, related_name='withdrawal_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_number = models.CharField(max_length=30)
    reference_id = models.CharField(max_length=120, blank=False, null=False)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    wallet_type = models.CharField(
        max_length=20, choices=ISP_CHOICES, default='')
    reason = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        processed = True if self.processed_date else False
        return f"By - {self.creator.user.username} - Amount: {self.amount} - Processed - {self.processed_date}"


class ProcessedWithdrawals(models.Model):
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_withdrawals')
    rejected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_withdrawals')
    processed_date = models.DateTimeField(auto_now_add=True)
    request_date = models.CharField(max_length=120, blank=True, null=True)
    reference_id = models.CharField(max_length=120, blank=False, null=False)
    withdrawal_request = models.ForeignKey(
        WithdrawalRequest, on_delete=models.CASCADE, related_name='withdrawals')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    wallet_type = models.CharField(
        max_length=20, choices=ISP_CHOICES, default='mtn')
    reason = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.approved_by:
            return f"Withdrawal - {self.approved_by.username} - Status: {self.status}"
        else:
            return f"Withdrawal - Not Approved Yet - Status: {self.status}"
