# -*- coding: utf-8 -*-
from random import randint

from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from applicationserver.tests import utils

EMAIL = 'user@test.com'
FORENAME = 'Terry'
SURNAME = 'Test'
FULL_NAME = FORENAME + ' ' + SURNAME
PASSWORD = '8yt7jpwr3'
USERNAME = randint(10000,99999)

class TestIndex(TestCase):

    NAME = 'dashboard'

    def test_get_loads(self):
        response = self.client.get(reverse(TestIndex.NAME))
        self.assertEqual(response.status_code, 302)

    def test_post_fails(self):
        response = self.client.post(reverse(TestIndex.NAME))
        self.assertEqual(response.status_code, 302)


class TestLogin(TestCase):

    NAME = 'login'

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(USERNAME, email=EMAIL, password=PASSWORD)

    def test_get_loads(self):
        response = self.client.get(reverse(TestLogin.NAME))
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        response = self.client.post(reverse(TestLogin.NAME), {
            'username': USERNAME,
            'password': PASSWORD
        })
        self.assertRedirects(response, reverse('dashboard'), status_code=302, target_status_code=302)
        self.assertRedirects(response, reverse('dashboard'), status_code=302, target_status_code=302)

    def test_successful_login_redirect(self):
        redirect = reverse('dashboard')
        response = self.client.post(
            reverse(TestLogin.NAME) + '?next=' + redirect,
            {
                'username': USERNAME,
                'password': PASSWORD
            })
        self.assertRedirects(response, redirect, status_code=302, target_status_code=302)

    def test_unsuccessful_login(self):
        response = self.client.post(reverse(TestLogin.NAME), {
            'username': USERNAME,
            'password': 'wrong'
        })


        self.assertContains(response,
                            'Please enter a correct username and password')

class TestDashboardView(TestCase):

    NAME = 'dashboard'

    def test_view_get_denies_anon(self):
        response = self.client.get(reverse(TestDashboardView.NAME), follow=True)
        self.assertRedirects(
            response, '{0}?next={1}'.format(reverse('login'),
                                            reverse(TestDashboardView.NAME)))

    def test_view_post_denies_anon(self):
        response = self.client.post(reverse(TestDashboardView.NAME), follow=True)
        self.assertRedirects(
            response, '{0}?next={1}'.format(reverse('login'),
                                            reverse(TestDashboardView.NAME)))

class TestChangePassword(TestCase):

    NAME = 'password_change'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(USERNAME, email=EMAIL, password=PASSWORD)

    def setUp(self):
        self.client.login(email=EMAIL, password=PASSWORD)

    def test_get_loads(self):
        response = self.client.get(reverse(TestChangePassword.NAME))
        self.assertEqual(response.status_code, 302)
