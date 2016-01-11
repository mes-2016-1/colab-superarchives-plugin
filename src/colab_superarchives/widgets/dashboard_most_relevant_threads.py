from colab.widgets.widget_manager import Widget
from colab_superarchives.utils.collaborations import get_user_threads
from colab_superarchives.utils import mailman
from colab_superarchives.models import Thread


class DashboardMostRelevantThreadsWidget(Widget):
    name = 'most relevant threads'
    template = 'widgets/dashboard_most_relevant_threads.html'

    def generate_content(self, **kwargs):
        highest_score_threads = Thread.highest_score.all()
        lists_for_user = []
        if kwargs['context']['user'].is_authenticated():
            lists_for_user = mailman.get_user_mailinglists(
                kwargs['context']['user'])

        kwargs['context']['hottest_threads'] = get_user_threads(
            highest_score_threads, lists_for_user,
            lambda t: t.latest_message)[:10]

        return super(DashboardMostRelevantThreadsWidget,
                     self).generate_content(**kwargs)
