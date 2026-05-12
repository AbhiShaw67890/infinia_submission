from django.urls import path
from . import views

app_name = 'claims'

urlpatterns = [
    path('submit/<int:item_pk>/',   views.submit_claim_view,   name='submit'),
    path('received/',               views.claims_received_view, name='received'),
    path('sent/',                   views.claims_sent_view,     name='sent'),
    path('<int:claim_pk>/approve/', views.approve_claim_view,   name='approve'),
    path('<int:claim_pk>/reject/',  views.reject_claim_view,    name='reject'),
]
