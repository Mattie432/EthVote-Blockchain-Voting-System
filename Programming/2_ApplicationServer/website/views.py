from django.shortcuts import render
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


class HomepageRedirect(View):
    """
    Redirects the site root to the dashboard page.
    """
    def get(self, request):
        return HttpResponseRedirect('/dashboard/')

class Dashboard(LoginRequiredMixin, View):
    """
    The dashboard page visible immediately after logging in.
    """
    def get(self, request):
        return  render(request, 'dashboard.html')
