from django.contrib import admin
from .models import Claim

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display  = ['claimant', 'item', 'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['claimant__username', 'item__title']
    actions       = ['approve_claims', 'reject_claims']

    def approve_claims(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_claims.short_description = 'Approve selected claims'

    def reject_claims(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_claims.short_description = 'Reject selected claims'
