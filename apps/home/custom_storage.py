from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

class StaticFileSystemStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.STATICFILES_DIRS[0]
        super().__init__(*args, **kwargs)

    def url(self, name):
        return os.path.join(settings.STATIC_URL, name)