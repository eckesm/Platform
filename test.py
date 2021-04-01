from unittest import TestCase
from flask import session
from app import app
import users

# unittest: python -m unittest test.py
# doctests: python -m doctest -v app.py


class FlaskTests(TestCase):

    def setUp(self):
        """Do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    # def tearDown(self):
    #     """Do after every test."""
    #     self.client.get('/logout')

    def test_index(self):
        """Test homepage screen."""
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))
            self.assertIn(
                b'<h1 class="display-2">Platform Home Page</h1>', response.data)

    def test_login(self):
        """Test login screen."""
        with self.client:
            response = self.client.get('/login')
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))
            self.assertIn(
                b'<form action="/login/attempt" method="POST" id="login_form">', response.data)

    def test_login_attempt(self):
        """Test login attempt."""
        with self.client:

            # Test unsuccessful login - wrong password / no redirect
            response = self.client.post(
                '/login/attempt', data={'email_address': 'test@testing.com', 'password': 'wrongpassword'})
            self.assertEqual(response.status_code, 302)
            self.assertFalse(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))

            # Test unsuccessful login - wrong password / redirect
            response = self.client.post(
                '/login/attempt', data={'email_address': 'test@testing.com', 'password': 'wrongpassword'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))
            self.assertIn(
                b'<div class="alert alert-danger" role="alert">Credentials entered were incorrect.  Please try again.</div>', response.data)

            # Test unsuccessful login - wrong email / no redirect
            response = self.client.post(
                '/login/attempt', data={'email_address': 'wrong@testing.com', 'password': 'correctpassword'})
            self.assertEqual(response.status_code, 302)
            self.assertFalse(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))

            # Test unsuccessful login - wrong email / redirect
            response = self.client.post(
                '/login/attempt', data={'email_address': 'wrong@testing.com', 'password': 'correctpassword'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))
            self.assertIn(
                b'<div class="alert alert-danger" role="alert">There is no user with the email address wrong@testing.com.  Please make sure you are entering the correct email address with the correct spelling.</div>', response.data)

            # Test successful login - no redirect
            response = self.client.post(
                '/login/attempt', data={'email_address': 'test@testing.com', 'password': 'correctpassword'})
            self.assertEqual(response.status_code, 302)
            self.assertTrue(session.get('logged-in'))
            self.assertIsNotNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertEqual(session.get('welcomed-user'), 0)

            self.client.get('/logout')

            # Test successful login - redirect
            response = self.client.post(
                '/login/attempt', data={'email_address': 'test@testing.com', 'password': 'correctpassword'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(session.get('logged-in'))
            self.assertIsNotNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertEqual(session.get('welcomed-user'), 1)
            self.assertIn(
                b'<div class="alert alert-info" role="alert">Login successful!</div>', response.data)

    def test_logout(self):
        """Test logout screen and procedure."""
        with self.client:
            self.client.post(
                '/login/attempt', data={'email_address': 'test@testing.com', 'password': 'correctpassword'}, follow_redirects=True)
            response = self.client.get('/logout')
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))
            self.assertIn(
                b'<div class="alert alert-info" role="alert">You have been logged out</div>', response.data)

    def test_new_user(self):
        """Test new user screen."""
        with self.client:
            response = self.client.get('/new-user')
            self.assertIn(
                b'<h1 class="display-2 text-center">New User Sign Up</h1>', response.data)

    def test_attempt_new_user(self):
        """Test attempt new user."""
        with self.client:

            self.client.get('/logout')

            # Test unsuccessful new user - reused email / redirect
            response = self.client.post(
                '/new-user/attempt', data={'first_name': 'NewFirst', 'last_name': 'NewLast', 'email_address': 'meckes@gmail.com', 'password': 'newpassword', 'preferred_pronouns': 'they/them', 'pronouns_other_subject': '', 'pronouns_other_object': '', 'agree_terms': 'on'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))
            self.assertIn(
                b'<div class="alert alert-warning" role="alert">meckes@gmail.com is associated with an existing user.  Please log in using this email address or create a new account using a different email address.</div>', response.data)

            # Test unsuccessful new user - bad first name / redirect
            response = self.client.post(
                '/new-user/attempt', data={'first_name': 'NewFirst/', 'last_name': 'NewLast', 'email_address': 'new@testing.com', 'password': 'newpassword', 'preferred_pronouns': 'they/them', 'pronouns_other_subject': '', 'pronouns_other_object': '', 'agree_terms': 'on'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))
            self.assertIn(
                b'<div class="alert alert-warning" role="alert">First name must be at least one character in length and may contain only letters and the following characters:', response.data)

            # Test unsuccessful new user - missing custom pronouns / redirect
            response = self.client.post(
                '/new-user/attempt', data={'first_name': 'NewFirst', 'last_name': 'NewLast', 'email_address': 'new@testing.com', 'password': 'newpassword', 'preferred_pronouns': 'other', 'pronouns_other_subject': '', 'pronouns_other_object': '', 'agree_terms': 'on'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(session.get('logged-in'))
            self.assertIsNone(session.get('user'))
            self.assertIsNone(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))
            self.assertIn(
                b'<div class="alert alert-info" role="alert">If selecting other preferred pronouns, enter a Subject Pronoun containing only letters.</div>', response.data)

            # Test successful new user - no redirect
            response = self.client.post(
                '/new-user/attempt', data={'first_name': 'NewFirst', 'last_name': 'NewLast', 'email_address': 'new@testing.com', 'password': 'newpassword', 'preferred_pronouns': 'they/them', 'pronouns_other_subject': '', 'pronouns_other_object': '', 'agree_terms': 'on'})
            self.assertEqual(response.status_code, 302)
            self.assertTrue(session.get('logged-in'))
            self.assertIsNotNone(session.get('user'))
            self.assertTrue(session.get('first-login'))
            self.assertIsNone(session.get('welcomed-user'))

            # Test successful new user - redirect
            response = self.client.post(
                '/login/attempt', data={'first_name': 'NewFirst', 'last_name': 'NewLast', 'email_address': 'new@testing.com', 'password': 'newpassword', 'preferred_pronouns': 'they/them', 'pronouns_other_subject': '', 'pronouns_other_object': '', 'agree_terms': 'on'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(session.get('logged-in'))
            self.assertIsNotNone(session.get('user'))
            self.assertTrue(session.get('first-login'))
            self.assertEquals(session.get('welcomed-user'), 1)
