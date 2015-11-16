This is the repository for Colab's plugin Super Archives


### Configuration

You should add the following in the */etc/colab/settings.d/super_archives.py* configuration file or the */etc/colab/settings.py*

```python
SUPER_ARCHIVES_PATH = '/var/lib/mailman/archives/private'
SUPER_ARCHIVES_EXCLUDE = []
SUPER_ARCHIVES_LOCK_FILE = '/var/lock/colab/import_emails.lock'
```
