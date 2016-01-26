
from django.utils.translation import ugettext_lazy as _
from colab.plugins.utils.menu import colab_url_factory

# Gitlab plugin - Put this in plugins.d/gitlab.py to actiate ##
# from django.utils.translation import ugettext_lazy as _
# from colab.plugins.utils.menu import colab_url_factory

name = 'colab_superarchives'
verbose_name = 'Super Archives'

#upstream = 'localhost'
#middlewares = []

urls = {
    'include': 'colab_superarchives.urls',
    'prefix': '^archives/',
}

menu_title = _('Groups')

url = colab_url_factory('archives')

menu_urls = (
    url(display=_('Groups'), viewname='thread_list', auth=False),
)

# Imported settings from colab
LOCALE_PATHS = ('colab_superarchives/locale',)

# Super Archives
SUPER_ARCHIVES_PATH = '/var/lib/mailman/archives/private'
SUPER_ARCHIVES_EXCLUDE = []
SUPER_ARCHIVES_LOCK_FILE = '/var/lock/colab/import_emails.lock'
