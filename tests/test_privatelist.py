# -*- coding:utf-8 -*-
from mock import patch
from mock import Mock
import requests
from requests.exceptions import Timeout
from colab_superarchives.utils import mailman
from django.test import TestCase, Client
from colab_superarchives.widgets.dashboard_latest_threads import DashboardLatestThreadsWidget
from colab_superarchives.views import ThreadView

class ArchivesViewTest(TestCase):

    fixtures = ['mailinglistdata.json']

    def setUp(self):
        self.client = Client()

    def authenticate_user(self):
        self.client.login(username='johndoe', password='1234')

    def test_see_only_private_list_if_member(self):
        mailman.get_user_mailinglists = Mock(
            return_value=[{'listname': 'privatelist'}])
        mailman.extract_listname_from_list = Mock(
            return_value=['privatelist'])
        mailman.list_users = Mock(return_value="['johndoe@example.com']")

        self.authenticate_user()
        request = self.client.get('/archives/thread/')

        list_data = request.context['lists']

        self.assertEqual('lista', list_data[0].name)
        self.assertEqual('privatelist', list_data[1].name)
        self.assertEqual(2, len(list_data))

    def test_see_only_public_if_not_logged_in(self):
        request = self.client.get('/archives/thread/')

        list_data = request.context['lists']

        self.assertEqual('lista', list_data[0].name)
        self.assertEqual(1, len(list_data))

    def test_see_private_thread_in_dashboard_if_member(self):
        mailman.get_user_mailinglists = Mock(
            return_value="[{'listname': 'privatelist'}]")
        mailman.extract_listname_from_list = Mock(
            return_value="['privatelist']")

        self.authenticate_user()
        request = self.client.get('/dashboard')

        widget = DashboardLatestThreadsWidget()
        context = widget.generate_content(context={'user': request.context['user']})

        latest_threads = request.context['latest_threads']

        self.assertEqual(4, len(latest_threads))

    def test_dont_see_private_thread_if_logged_out(self):
        request = self.client.get('/dashboard')

        widget = DashboardLatestThreadsWidget()
        context = widget.generate_content(context={'user': request.context['user']})

        latest_threads = context['latest_threads']
        self.assertEqual(1, len(latest_threads))

    def test_dont_see_private_threads_in_profile_if_logged_out(self):
        request = self.client.get('/dashboard')
        request = self.client.get('/account/johndoe')

        emails = request.context['emails']

        self.assertEqual(1, len(emails))

class ThreadViewTest(TestCase):

    fixtures = ['mailinglistdata.json']

    def setUp(self):
        self.client = Client()
        self.thread_view = ThreadView()
        self.data = {
            'in_reply_to': 1,
            'email_from': "test@test.com",
            'name_from': "John Doe",
            'subject': "Subject Test",
            'body': "Email body test",
        }
        url = "http://localhost/"

        self.response = requests.post(url, data=self.data, timeout=2)

    def authenticate_user(self):
        self.client.login(username='johndoe', password='1234')

    def test_mailing_list_in_user_list(self):
        self.authenticate_user()

        user_name = "johndoe"
        list_name = "privatelist"

        list_in_user = self.thread_view.mailing_list_in_user_list(user_name,
                                                                  list_name)
        self.assertTrue(list_in_user)

    def test_error_message_empty_email(self):
        self.response.status_code = 400
        error_message = self.thread_view.return_error_message(self.response)
        self.assertEqual(error_message, 'You cannot send an empty email')

    def test_error_message_mailing_list_not_exist(self):
        self.response.status_code = 404
        error_message = self.thread_view.return_error_message(self.response)
        self.assertEqual(error_message, 'Mailing list does not exist')

    def test_error_message_unknown_error(self):
        self.response.status_code = 999999
        error_message = self.thread_view.return_error_message(self.response)
        self.assertEqual(error_message,
                         'Unknown error trying to connect to Mailman API')

    def test_error_message_with_response_none(self):
        response = None
        error_message = self.thread_view.return_error_message(response)
        self.assertEqual(error_message,
                         'Unknown error trying to connect to Mailman API')

    def test_get_response_connection_error(self):
        wrong_url = "http://error.url.not.exist"
        return_message = self.thread_view.get_response_message_sent(
            wrong_url, self.data)[1]
        self.assertEqual(return_message,
                         'Error trying to connect to Mailman API')

    @patch('requests.post', side_effect=Timeout())
    def test_get_response_timeout(self, mock):
        any_url = "http://anything.com"
        return_message = self.thread_view.get_response_message_sent(
            any_url, self.data)[1]
        self.assertEqual(return_message,
                         'Timeout trying to connect to Mailman API')

    @patch('requests.post', return_value=None)
    def test_get_response_successfully(self, mock):
        any_url = "http://anything.com"
        return_message = self.thread_view.get_response_message_sent(
            any_url, self.data)[1]
        self.assertEqual(return_message, None)
