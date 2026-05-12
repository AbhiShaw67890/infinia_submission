"""
claims/views.py — Claim submission, approval, rejection.
Security: only the item owner can approve/reject a claim.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Claim
from .forms import ClaimForm
from items.models import Item


@login_required
def submit_claim_view(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    # Can't claim your own item
    if item.posted_by == request.user:
        messages.error(request, "You can't claim your own post.")
        return redirect('items:detail', pk=item_pk)

    # Can't claim a resolved item
    if item.is_resolved:
        messages.warning(request, 'This item has already been resolved.')
        return redirect('items:detail', pk=item_pk)

    # Check if already claimed
    existing = Claim.objects.filter(item=item, claimant=request.user).first()
    if existing:
        messages.info(request, 'You have already submitted a claim for this item.')
        return redirect('items:detail', pk=item_pk)

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item     = item
            claim.claimant = request.user
            claim.save()
            messages.success(request, 'Claim submitted! The owner will review it shortly.')
            return redirect('items:detail', pk=item_pk)
    else:
        form = ClaimForm()

    return render(request, 'claims/submit.html', {'form': form, 'item': item})


@login_required
def claims_received_view(request):
    """Shows claims received on items posted by the current user."""
    claims = Claim.objects.filter(
        item__posted_by=request.user
    ).select_related('claimant', 'item').order_by('-created_at')
    return render(request, 'claims/received.html', {'claims': claims})


@login_required
def claims_sent_view(request):
    """Shows claims the current user has submitted."""
    claims = Claim.objects.filter(
        claimant=request.user
    ).select_related('item', 'item__posted_by').order_by('-created_at')
    return render(request, 'claims/sent.html', {'claims': claims})


@login_required
def approve_claim_view(request, claim_pk):
    claim = get_object_or_404(Claim, pk=claim_pk)

    # Authorization: only the item owner can approve
    if claim.item.posted_by != request.user:
        messages.error(request, 'You are not authorised to approve this claim.')
        return redirect('claims:received')

    if request.method == 'POST':
        # Approve this claim
        claim.status = 'APPROVED'
        claim.save()

        # Reject all other pending claims for the same item
        Claim.objects.filter(item=claim.item, status='PENDING').exclude(pk=claim.pk).update(status='REJECTED')

        # Mark item as RESOLVED
        claim.item.status = 'RESOLVED'
        claim.item.save()

        messages.success(request, f'Claim approved! Item marked as resolved.')
        return redirect('claims:received')

    return render(request, 'claims/approve_confirm.html', {'claim': claim})


@login_required
def reject_claim_view(request, claim_pk):
    claim = get_object_or_404(Claim, pk=claim_pk)

    if claim.item.posted_by != request.user:
        messages.error(request, 'You are not authorised to reject this claim.')
        return redirect('claims:received')

    if request.method == 'POST':
        claim.status = 'REJECTED'
        claim.save()
        messages.info(request, 'Claim rejected.')
        return redirect('claims:received')

    return render(request, 'claims/reject_confirm.html', {'claim': claim})
