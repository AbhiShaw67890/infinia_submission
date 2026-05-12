"""
items/views.py — All item-related views.
Uses function-based views for clarity and beginner-friendliness.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Item
from .forms import ItemForm, SearchForm
from core.services import get_matches


def feed_view(request):
    """
    Public home feed — shows ACTIVE items.
    Supports tab filtering: Lost / Found / All.
    """
    item_type = request.GET.get('type', '')
    qs = Item.objects.filter(status='ACTIVE').select_related('posted_by')
    if item_type in ('LOST', 'FOUND'):
        qs = qs.filter(item_type=item_type)
    return render(request, 'items/feed.html', {
        'items': qs,
        'active_type': item_type,
    })


def item_detail_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user_claim = None
    if request.user.is_authenticated:
        from claims.models import Claim
        user_claim = Claim.objects.filter(item=item, claimant=request.user).first()

    # Get possible matches from the matching engine
    matches = get_matches(item, limit=4)

    return render(request, 'items/detail.html', {
        'item': item,
        'user_claim': user_claim,
        'matches': matches,
    })


def search_view(request):
    form = SearchForm(request.GET)
    items = Item.objects.filter(status='ACTIVE').select_related('posted_by')

    if form.is_valid():
        q         = form.cleaned_data.get('q', '')
        category  = form.cleaned_data.get('category', '')
        location  = form.cleaned_data.get('location', '')
        item_type = form.cleaned_data.get('item_type', '')

        if q:
            items = items.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            items = items.filter(category=category)
        if location:
            items = items.filter(location__icontains=location)
        if item_type:
            items = items.filter(item_type=item_type)

    return render(request, 'items/search.html', {
        'form': form,
        'items': items,
        'query': request.GET.get('q', ''),
    })


@login_required
def create_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            item.save()
            messages.success(request, 'Item posted successfully! 🎉')
            return redirect('items:detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'items/create.html', {'form': form, 'action': 'Post'})


@login_required
def edit_item_view(request, pk):
    item = get_object_or_404(Item, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated!')
            return redirect('items:detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/create.html', {'form': form, 'action': 'Update', 'item': item})


@login_required
def delete_item_view(request, pk):
    item = get_object_or_404(Item, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted.')
        return redirect('accounts:profile')
    return render(request, 'items/confirm_delete.html', {'item': item})


@login_required
def my_posts_view(request):
    items = Item.objects.filter(posted_by=request.user).order_by('-created_at')
    return render(request, 'items/my_posts.html', {'items': items})
