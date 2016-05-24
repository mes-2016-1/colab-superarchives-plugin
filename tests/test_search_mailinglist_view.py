from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from mock import patch

class SearchMailingListViewTest(TestCase):

    fixtures = ['mailinglistviewdata.json', 'test_user.json']

    all_lists = [{'listname': 'listA'}, {'listname': 'norrislist'}]

    def setUp(self):
        self.client = Client()
        self.username = 'chucknorris'
        self.url_to_test = reverse('archives:user_list_subscriptions', kwargs={'username': self.username})

    def authenticate_user(self):
        self.client.login(username=self.username, password='admin')

    @patch('colab_superarchives.views.mailman.all_lists',return_value=all_lists )
    def test_show_all_mailinglist_for_subscription(self, mock):

        self.authenticate_user()

        response = self.client.post(self.url_to_test, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertContains(response, self.all_lists[0]['listname'],status_code=200)
        self.assertContains(response, self.all_lists[1]['listname'],status_code=200)
        self.client.logout()

    @patch('colab_superarchives.views.mailman.all_lists',return_value=all_lists )
    def test_show_searched_mailinglist_for_subscription(self, mock):

        self.authenticate_user()
        
        data = {'listname':"listA"}

        response = self.client.post(self.url_to_test, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertContains(response, data['listname'],status_code=200)
        self.assertNotContains(response, self.all_lists[1]['listname'],status_code=200)
        self.client.logout()

    @patch('colab_superarchives.views.mailman.all_lists',return_value=all_lists)
    def test_show_message_mailinglist_not_found_for_subscription(self, mock):

        self.authenticate_user()
        
        data = {'listname':"listB"}

        response = self.client.post(self.url_to_test, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        message = _("List not found.")
        self.assertContains(response, message, status_code=200)
        self.assertNotContains(response, self.all_lists[0]['listname'],status_code=200)
        self.assertNotContains(response, self.all_lists[1]['listname'],status_code=200)
        self.client.logout()