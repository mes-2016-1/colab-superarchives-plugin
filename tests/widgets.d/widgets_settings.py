# Widget Manager handles all widgets and must be imported to register them
from colab.widgets.widget_manager import WidgetManager

from colab.accounts.widgets.group_membership import GroupMembershipWidget
from colab.accounts.widgets.latest_posted import LatestPostedWidget
from colab.accounts.widgets.latest_contributions import LatestContributionsWidget
from colab.accounts.widgets.group import GroupWidget
from colab.accounts.widgets.collaboration_chart import CollaborationChart
from colab.accounts.widgets.participation_chart import ParticipationChart
from colab_superarchives.widgets.dashboard_most_relevant_threads import DashboardMostRelevantThreadsWidget
from colab_superarchives.widgets.dashboard_latest_threads import DashboardLatestThreadsWidget
from colab_superarchives.widgets.dashboard_collaboration_graph import DashboardCollaborationGraphWidget
from colab_superarchives.widgets.dashboard_latest_collaborations import DashboardLatestCollaborationsWidget

WidgetManager.register_widget('group', GroupWidget())
WidgetManager.register_widget('button', GroupMembershipWidget())
WidgetManager.register_widget('list', LatestPostedWidget())
WidgetManager.register_widget('list', LatestContributionsWidget())
WidgetManager.register_widget('collaboration_chart', CollaborationChart())
WidgetManager.register_widget('participation_chart', ParticipationChart())
WidgetManager.register_widget('dashboard_latest_threads', DashboardLatestCollaborationsWidget())
WidgetManager.register_widget('dashboard_most_relevant_threads', DashboardMostRelevantThreadsWidget())
WidgetManager.register_widget('dashboard_collaboration_graph', DashboardCollaborationGraphWidget())
WidgetManager.register_widget('dashboard_latest_collaborations', DashboardLatestCollaborationsWidget())
