from colab.widgets.widget_manager import WidgetManager
from colab.widgets.dashboard.dashboard_latest_collaborations\
    import DashboardLatestCollaborationsWidget
from colab.widgets.dashboard.dashboard_collaboration_graph\
    import DashboardCollaborationGraphWidget
from colab_superarchives.widgets.dashboard_most_relevant_threads\
    import DashboardMostRelevantThreadsWidget
from colab_superarchives.widgets.dashboard_latest_threads\
    import DashboardLatestThreadsWidget


WidgetManager.register_widget(
    'dashboard', DashboardLatestCollaborationsWidget())
WidgetManager.register_widget(
    'dashboard', DashboardCollaborationGraphWidget())
WidgetManager.register_widget(
    'dashboard', DashboardMostRelevantThreadsWidget())
WidgetManager.register_widget(
    'dashboard', DashboardLatestThreadsWidget())
