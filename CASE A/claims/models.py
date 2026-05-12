"""
claims/models.py
A Claim links a claimant to an Item with a message and approval status.
Only the item owner can approve/reject.
"""

from django.db import models
from django.conf import settings
from items.models import Item


class Claim(models.Model):
    STATUS_CHOICES = [
        ('PENDING',  'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    item      = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='claims_made',
    )
    message    = models.TextField(help_text='Describe why this item belongs to you')
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # A user can only claim the same item once
        unique_together = [('item', 'claimant')]

    def __str__(self):
        return f"Claim by {self.claimant.username} on {self.item.title} [{self.status}]"
