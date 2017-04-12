# -*- coding: utf-8 -*-
from random import randint
from applicationserver.tests import utils

from django.test import TestCase
from accounts.models import User
from accounts.forms import LoginForm, InitialLogin

FORENAME = 'Terry'
SURNAME = 'Test'
EMAIL = 'test@example.com'
PASSWORD = 'o8v43t2h28348jjk'
USERNAME = randint(10000,99999)


class TestLoginForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.request = utils.mock_request()
        cls.user = User.objects.create_user(USERNAME, email=EMAIL, password=PASSWORD)


    def test_no_username(self):
        form = LoginForm(self.request, data={
            'password': PASSWORD
        })
        self.assertEqual(form.errors['username'], ['This field is required.'])



    def test_no_password(self):
        form = LoginForm(self.request, data={
            'username': USERNAME
        })
        self.assertEqual(form.errors['password'], ['This field is required.'])


    def test_invalid_username(self):
        try:
            form = LoginForm(self.request, data={
                'username': 'nope',
                'password': PASSWORD
            })
        except ValueError:
            self.assertTrue("Invalud username.")
        except:
            self.assertFalse("Should have thrown an exception")


    def test_username_not_registered(self):
        form = LoginForm(self.request, data={
            'username': 123456,
            'password': PASSWORD
        })
        self.assertEqual(
            form.errors.as_data()['__all__'][0].message,
            'Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.')


    def test_incorrect_password(self):
        form = LoginForm(self.request, data={
            'username': USERNAME,
            'password': 'nope'
        })
        self.assertFalse(form.is_valid())


    def test_inactive(self):
        self.user.is_active = False
        self.user.save()
        form = LoginForm(self.request, data={
            'username': USERNAME,
            'password': PASSWORD
        })
        self.assertEqual(
            form.errors.as_data()['__all__'][0].message,
            'Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.')


    def test_valid(self):
        form = LoginForm(self.request, data={
            'username': USERNAME,
            'password': PASSWORD
        })
        self.assertTrue(form.is_valid())


class TestInitialLogin(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.request = utils.mock_request()
        cls.user = User.objects.create_user(USERNAME, email=EMAIL, password=PASSWORD)

    def test_short_password(self):

        new_passsword = 'as'

        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : PASSWORD,
            'password1' : new_passsword,
            'password2' : new_passsword
        })

        self.assertTrue(form.is_valid())


    def test_numeric_password(self):
        new_passsword = '1231233123'

        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : PASSWORD,
            'password1' : new_passsword,
            'password2' : new_passsword
        })

        self.assertTrue(form.is_valid())

    def test_common_password(self):
        new_passsword = 'password'

        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : PASSWORD,
            'password1' : new_passsword,
            'password2' : new_passsword
        })

        self.assertTrue(form.is_valid())

    def test_register_existing_email(self):
        new_passsword = 'adminadmin'

        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : "alreadyregistered@test.com",
            'old_password' : PASSWORD,
            'password1' : new_passsword,
            'password2' : new_passsword
        })

        self.assertTrue(form.is_valid())

    def test_valid(self):
        new_passsword = 'ValidPassword'

        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : PASSWORD,
            'password1' : new_passsword,
            'password2' : new_passsword
        })

        self.assertTrue(form.is_valid())


    def test_missing_current_password(self):
        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'password1' : "ValidPassword",
            'password2' : "ValidPassword"
        })

        self.assertFalse(form.is_valid())


    def test_empty_current_password(self):
        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : '',
            'password1' : "ValidPassword",
            'password2' : "ValidPassword"
        })
        self.assertFalse(form.is_valid())

    def test_missing_new_password(self):
        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : PASSWORD,
            'password2' : "ValidPassword"
        })
        self.assertFalse(form.is_valid())

    def test_empty_new_password(self):
        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : PASSWORD,
            'password1' : "",
            'password2' : ""
        })
        self.assertFalse(form.is_valid())

    def test_related_password(self):
        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : PASSWORD,
            'password1' : "ValidPassword",
            'password2' : "ValidPassword"
        })
        self.assertTrue(form.is_valid())

    def test_current_password_incorrect(self):
        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : PASSWORD,
            'password1' : "ValidPassword",
            'password2' : "ValidPassword"
        })
        self.assertTrue(form.is_valid())

    def test_passwords_identical(self):
        form = InitialLogin(self.user, data={
            'first_name' : FORENAME,
            'last_name' : SURNAME,
            'email' : EMAIL,
            'old_password' : PASSWORD,
            'password1' : PASSWORD,
            'password2' : PASSWORD
        })
        self.assertFalse(form.is_valid())
