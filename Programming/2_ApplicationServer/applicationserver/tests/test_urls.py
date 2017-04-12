# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse, resolve

from website.views import *
from accounts.views import *
from user_ballot_registration.views import *
from django.contrib.auth import views

class UrlTests(TestCase):
    """
    Ensure URL reversal works, and each URL triggers the correct view.
    """
    def test_reverse_register_for_ballot(self):
        self.assertEqual(reverse('register_for_ballot', args=(1234,)), '/register_for_ballot/1234/')
    def test_resolve_register_for_ballot(self):
        self.assertEqual(resolve('/register_for_ballot/1234/').func.view_class, RegisterForBallot)

    def test_reverse_login(self):
        self.assertEqual(reverse('login'), '/login/')

    def test_reverse_account_dashboard(self):
        self.assertEqual(reverse('dashboard'), '/dashboard/')
    def test_resolve_account_dashboard(self):
        self.assertEqual(resolve('/dashboard/').func.view_class, Dashboard)

    def test_reverse_account_security_change_password(self):
        self.assertEqual(reverse('password_change'), '/password_change/')
    def test_resolve_account_security_change_password(self):
        self.assertEqual( resolve('/password_change/').func, views.password_change)

    def test_reverse_logout(self):
        self.assertEqual(reverse('logout'), '/logout/')

    def test_resolve_logout(self):
        self.assertEqual(resolve('/logout/').func, views.logout)
