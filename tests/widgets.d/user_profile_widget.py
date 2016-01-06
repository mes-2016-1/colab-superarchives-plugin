from colab.widgets.widget_manager import WidgetManager
from colab.accounts.widgets.latest_contributions import LatestContributionsWidget
from colab_superarchives.widgets.group import GroupWidget
from colab_superarchives.widgets.group_membership import GroupMembershipWidget
from colab_superarchives.widgets.latest_posted import LatestPostedWidget


WidgetManager.register_widget('group', GroupWidget())
WidgetManager.register_widget('button', GroupMembershipWidget())
WidgetManager.register_widget('list', LatestPostedWidget())
WidgetManager.register_widget('list', LatestContributionsWidget())
