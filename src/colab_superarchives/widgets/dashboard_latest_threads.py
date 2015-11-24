from colab.widgets.widget_manager import Widget
from colab.accounts.models import User
from colab_superarchives.utils import mailman
from colab_superarchives.models import Thread
from django.template.loader import render_to_string


def get_user_threads(threads, lists_for_user, key):
    visible_threads = []
    listnames_for_user = mailman.extract_listname_from_list(lists_for_user)
    for t in threads:
        if not t.mailinglist.is_private or \
           t.mailinglist.name in listnames_for_user:
                visible_threads.append(key(t))

    return visible_threads


class DashboardLatestThreadsWidget(Widget):
    name = 'latest threads'

    def get_body(self):
        return self.content

    def generate_content(self, **kwargs):
        request = kwargs.get('context').get('request')
        all_threads = Thread.objects.all()
        latest_threads = []
        lists_for_user = []

        if request.user.is_authenticated():
            user = User.objects.get(username=request.user)
            lists_for_user = mailman.get_user_mailinglists(user)

        latest_threads = get_user_threads(
            all_threads, lists_for_user, lambda t: t)

        context = {
            'latest_threads': latest_threads[:6],
        }

        template = 'widgets/dashboard_latest_threads.html'
        self.content = render_to_string(template, context)
        return context
