import StorageServer
import sys
import xbmc
from abc import ABCMeta, abstractmethod
from requests.exceptions import HTTPError, Timeout, ConnectionError
from requests.packages import urllib3

from lib.libs.addonsettings import settings
from lib.libs.pykodi import log
from lib.libs.utils import SortedDisplay
from lib.libs.webhelper import Getter

urllib3.disable_warnings()

languages = ()

cache = StorageServer.StorageServer('script.artwork.beef', 72)
monitor = xbmc.Monitor()

# Result of `get_images` is dict of lists, keyed on art type
# {'url': URL, 'language': ISO alpha-2 code, 'rating': SortedDisplay, 'size': SortedDisplay, 'provider': self.name, 'preview': preview URL}
# 'title': optional image title
# 'subtype': optional image subtype, like disc dvd/bluray/3d, SortedDisplay
# language should be None if there is no title on the image

class AbstractProvider(object):
    __metaclass__ = ABCMeta

    name = SortedDisplay(0, '')
    mediatype = None
    contenttype = None

    def __init__(self):
        self.getter = Getter(self.contenttype, self.login)
        self.getter.session.headers['User-Agent'] = settings.useragent

    def doget(self, url, params=None, headers=None):
        try:
            return self.getter(url, params, headers)
        except (Timeout, ConnectionError) as ex:
            raise ProviderError, ("Cannot contact provider", ex), sys.exc_info()[2]
        except HTTPError as ex:
            raise ProviderError, ('HTTP error: ' + ex.message, ex), sys.exc_info()[2]

    def log(self, message, level=xbmc.LOGDEBUG):
        if self.mediatype:
            log(message, level, tag='%s:%s' % (self.name.sort, self.mediatype))
        else:
            log(message, level, tag='%s' % self.name.sort)

    def login(self):
        return False

class AbstractImageProvider(AbstractProvider):
    @abstractmethod
    def get_images(self, uniqueids, types=None):
        pass

class ProviderError(Exception):
    def __init__(self, message, cause=None):
        super(ProviderError, self).__init__(message)
        self.cause = cause
