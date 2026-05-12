from django.shortcuts import redirect

def home_view(request):
    """Redirect root URL to the item feed."""
    return redirect('items:feed')
