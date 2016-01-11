from colab.widgets.widget_manager import Widget
from colab_superarchives.utils.collaborations import get_user_threads
from colab_superarchives.utils import mailman
from colab_superarchives.models import Thread


class DashboardLatestThreadsWidget(Widget):
    name = 'latest threads'
    template = 'widgets/dashboard_latest_threads.html'

    def generate_content(self, **kwargs):
        all_threads = Thread.objects.all()
        lists_for_user = []
        if kwargs['context']['user'].is_authenticated():
            lists_for_user = mailman.get_user_mailinglists(
                kwargs['context']['user'])

        kwargs['context']['latest_threads'] = get_user_threads(
            all_threads, lists_for_user, lambda t: t)[:10]

        return super(DashboardLatestThreadsWidget,
                     self).generate_content(**kwargs)
