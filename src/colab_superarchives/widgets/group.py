from django.db.models import Count

from colab.widgets.widget_manager import Widget
from colab_superarchives.utils.collaborations import get_visible_threads


class GroupWidget(Widget):
    name = 'group'
    template = 'widgets/group.html'

    def generate_content(self, **kwargs):
        query = get_visible_threads(
            kwargs['context']['user'], kwargs['context']['object'])
        count_by = 'thread__mailinglist__name'
        kwargs['context']['list_activity'] = dict(query.values_list(count_by)
                                                  .annotate(Count(count_by))
                                                  .order_by(count_by))

        return super(GroupWidget, self).generate_content(**kwargs)
