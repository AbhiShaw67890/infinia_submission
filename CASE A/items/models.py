"""
items/models.py
Core data model for the Lost & Found portal.
Indexes on item_type, status, category speed up the filtered feed queries.
"""

from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class Item(models.Model):
    ITEM_TYPE_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('RESOLVED', 'Resolved'),
    ]

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing',    'Clothing'),
        ('id_card',     'ID Card'),
        ('books',       'Books'),
        ('keys',        'Keys'),
        ('wallet',      'Wallet / Purse'),
        ('bag',         'Bag / Backpack'),
        ('jewellery',   'Jewellery'),
        ('sports',      'Sports Equipment'),
        ('other',       'Other'),
    ]

    title            = models.CharField(max_length=150)
    description      = models.TextField()
    category         = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    item_type        = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    date_of_incident = models.DateField(help_text='Date when item was lost/found')
    location         = models.CharField(max_length=200, help_text='e.g. Library 2nd floor, Hostel C')
    image            = CloudinaryField('image', blank=True, null=True)
    posted_by        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='items',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['item_type']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['location']),
            models.Index(fields=['item_type', 'status']),
        ]

    def __str__(self):
        return f"[{self.item_type}] {self.title}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return "https://placehold.co/600x400/e2e8f0/94a3b8?text=No+Image"

    @property
    def is_resolved(self):
        return self.status == 'RESOLVED'
