from colab.widgets.widget_manager import Widget
from colab_superarchives.utils.collaborations import get_visible_threads


class LatestPostedWidget(Widget):
    name = 'last posted'
    template = 'widgets/latest_posted.html'

    def generate_content(self, **kwargs):
        query = get_visible_threads(
            kwargs['context']['user'], kwargs['context']['object'])
        kwargs['context']['emails'] = query.order_by('-received_time')[:10]
        return super(LatestPostedWidget, self).generate_content(**kwargs)
