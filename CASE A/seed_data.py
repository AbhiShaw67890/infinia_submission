# -*- coding: utf-8 -*-
"""
seed_data.py -- Create demo users and items for development/demo purposes.
Run with: python seed_data.py
"""

import os
import sys
import django

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound.settings.development')
django.setup()

from accounts.models import User
from items.models import Item
from datetime import date, timedelta

print("Seeding demo data...")

# --- Create users ---
users_data = [
    {'username': 'alice',   'email': 'alice@campus.edu',   'first_name': 'Alice',  'last_name': 'Johnson',  'college': 'IIT Kharagpur'},
    {'username': 'bob',     'email': 'bob@campus.edu',     'first_name': 'Bob',    'last_name': 'Smith',    'college': 'IIT Kharagpur'},
    {'username': 'charlie', 'email': 'charlie@campus.edu', 'first_name': 'Charlie','last_name': 'Brown',    'college': 'IIT Kharagpur'},
]

users = []
for ud in users_data:
    user, created = User.objects.get_or_create(username=ud['username'], defaults=ud)
    if created:
        user.set_password('demo1234')
        user.save()
        print(f"  [OK] Created user: {user.username}")
    else:
        print(f"  [EXISTS] User: {user.username}")
    users.append(user)

today = date.today()

# --- Create items ---
items_data = [
    {
        'title': 'Black JBL Earphones',
        'description': 'Left them in the library near the charging stations. Black JBL earphones in a round case with a small sticker on it.',
        'category': 'electronics',
        'item_type': 'LOST',
        'date_of_incident': today - timedelta(days=2),
        'location': 'Central Library, 2nd Floor',
        'posted_by': users[0],
    },
    {
        'title': 'Blue Boat Shoes (Size 9)',
        'description': 'Found a pair of blue Boat brand shoes near the swimming pool area. Size 9. No other marks.',
        'category': 'clothing',
        'item_type': 'FOUND',
        'date_of_incident': today - timedelta(days=1),
        'location': 'Swimming Pool, Main Building',
        'posted_by': users[1],
    },
    {
        'title': 'Student ID Card - Ravi Kumar',
        'description': 'Found an ID card near the canteen. Belongs to Ravi Kumar, 3rd Year CSE.',
        'category': 'id_card',
        'item_type': 'FOUND',
        'date_of_incident': today,
        'location': 'Main Canteen',
        'posted_by': users[2],
    },
    {
        'title': 'Black Leather Wallet',
        'description': 'Lost my black leather wallet somewhere between the hostel and the lecture hall. Contains my ID card and some cash.',
        'category': 'wallet',
        'item_type': 'LOST',
        'date_of_incident': today - timedelta(days=3),
        'location': 'Hostel D to LH-5 route',
        'posted_by': users[0],
    },
    {
        'title': 'Silver MacBook Charger (MagSafe)',
        'description': 'Left a MacBook MagSafe charger in LH-3 Row C. 61W, Apple original.',
        'category': 'electronics',
        'item_type': 'LOST',
        'date_of_incident': today - timedelta(days=1),
        'location': 'Lecture Hall 3',
        'posted_by': users[1],
    },
    {
        'title': 'Yellow Water Bottle',
        'description': 'Found a bright yellow Nalgene water bottle near the gym. Has stickers on it.',
        'category': 'other',
        'item_type': 'FOUND',
        'date_of_incident': today,
        'location': 'Gymnasium',
        'posted_by': users[2],
    },
]

for idata in items_data:
    item, created = Item.objects.get_or_create(
        title=idata['title'],
        posted_by=idata['posted_by'],
        defaults=idata
    )
    if created:
        print(f"  [OK] Created item: {item.title}")
    else:
        print(f"  [EXISTS] Item: {item.title}")

print("\nSeeding complete!")
print("Demo credentials:")
print("  Username: alice / Password: demo1234")
print("  Username: bob   / Password: demo1234")
