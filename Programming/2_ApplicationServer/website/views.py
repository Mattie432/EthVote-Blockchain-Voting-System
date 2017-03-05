from django.shortcuts import render
from django.views import View
from django.shortcuts import render

# Create your views here.
class Login(View):
    """
    The login page.
    """

    def get(self, request):
        return render(request, 'login.html')
