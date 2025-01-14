import xbmc

from lib.libs import pykodi

try:
    import projectkeys
except ImportError:
    projectkeys = None

addon = pykodi.get_main_addon()

DEFAULT_IMAGESIZE = '1'
AVAILABLE_IMAGESIZES = {'0': (10000, 10000, 600), '1': (1920, 1080, 600), '2': (1280, 720, 480)}

PROGRESS_DISPLAY_FULLPROGRESS = '0'
PROGRESS_DISPLAY_WARNINGSERRORS = '1'
PROGRESS_DISPLAY_NONE = '2'  # Only add-on crashes

EXCLUSION_PATH_TYPE_FOLDER = '0'
EXCLUSION_PATH_TYPE_PREFIX = '1'
EXCLUSION_PATH_TYPE_REGEX = '2'


class Settings(object):
    def __init__(self):
        self.identify_alternatives = None
        self.apiconfig = None
        self.preferredsize = None
        self.enableservice_music = None
        self.minimum_size = None
        self.clean_imageurls = None
        self.language_fallback_en = None
        self.minimum_rating = None
        self.language_fallback_kodi = None
        self.language_override = None
        self.default_tvidsource = None
        self.savewith_basefilename = None
        self.cache_local_music_artwork = None
        self.progressdisplay = None
        self.recycle_removed = None
        self.cache_local_video_artwork = None
        self.remove_deselected_files = None
        self.savewith_basefilename_mvids = None
        self.albumartwithmediafiles = None
        self.use_tmdb_keyart = None
        self.save_extrafanart = None
        self.save_extrafanart_mvids = None
        self.final_notification = None
        self.setartwork_subdirs = None
        self.report_peritem = None
        self.titlefree_poster = None
        self.fanarttv_clientkey = None
        self.titlefree_fanart = None
        self.setartwork_fromparent = None
        self.enable_olditem_updates = None
        self.enableservice = None
        self.useragent = None
        self.pathexclusion = None
        self.addon_path = addon.path
        self.datapath = addon.datapath
        self._autoadd_episodes = ()
        self.update_settings()
        self.update_useragent()

    def update_useragent(self):
        beefversion = pykodi.get_main_addon().version
        if pykodi.get_kodi_version() < 17:
            from lib.libs import quickjson
            props = quickjson.get_application_properties(['name', 'version'])
            appversion = '{0}.{1}'.format(props['version']['major'], props['version']['minor'])
            self.useragent = 'ArtworkBeef/{0} {1}/{2}'.format(beefversion, props['name'], appversion)
            return
        self.useragent = 'ArtworkBeef/{0} '.format(beefversion) + xbmc.getUserAgent()

    def update_settings(self):
        self._autoadd_episodes = addon.get_setting('autoaddepisodes_list') \
            if addon.get_setting('episode.fanart') else ()
        self.enableservice = addon.get_setting('enableservice')
        self.enableservice_music = addon.get_setting('enableservice_music')
        self.enable_olditem_updates = addon.get_setting('enable_olditem_updates')
        self.titlefree_fanart = addon.get_setting('titlefree_fanart')
        self.titlefree_poster = addon.get_setting('titlefree_poster')
        self.setartwork_fromparent = addon.get_setting('setartwork_fromparent')
        self.setartwork_subdirs = addon.get_setting('setartwork_subdirs')
        self.identify_alternatives = addon.get_setting('identify_alternatives')
        self.report_peritem = addon.get_setting('report_peritem')
        self.fanarttv_clientkey = addon.get_setting('fanarttv_key')
        self.default_tvidsource = addon.get_setting('default_tvidsource')
        self.progressdisplay = addon.get_setting('progress_display')
        self.final_notification = addon.get_setting('final_notification')
        self.save_extrafanart = addon.get_setting('save_extrafanart')
        self.save_extrafanart_mvids = addon.get_setting('save_extrafanart_mvids')
        self.remove_deselected_files = addon.get_setting('remove_deselected_files')
        self.recycle_removed = addon.get_setting('recycle_removed')
        self.savewith_basefilename = addon.get_setting('savewith_basefilename')
        self.savewith_basefilename_mvids = addon.get_setting('savewith_basefilename_mvids')
        self.albumartwithmediafiles = addon.get_setting('albumartwithmediafiles')
        self.cache_local_video_artwork = addon.get_setting('cache_local_video_artwork')
        self.cache_local_music_artwork = addon.get_setting('cache_local_music_artwork')
        self.clean_imageurls = addon.get_setting('clean_imageurls')
        self.use_tmdb_keyart = addon.get_setting('use_tmdb_keyart')

        self.language_override = addon.get_setting('language_override')
        if self.language_override == 'None':
            self.language_override = None
        self.language_fallback_kodi = addon.get_setting('language_fallback_kodi')
        self.language_fallback_en = addon.get_setting('language_fallback_en')

        try:
            self.minimum_rating = int(addon.get_setting('minimum_rating'))
        except ValueError:
            self.minimum_rating = 5
            addon.set_setting('minimum_rating', "5")

        sizesetting = addon.get_setting('preferredsize')
        if sizesetting not in AVAILABLE_IMAGESIZES:
            sizesetting = DEFAULT_IMAGESIZE
            addon.set_setting('preferredsize', DEFAULT_IMAGESIZE)
        self.preferredsize = AVAILABLE_IMAGESIZES[sizesetting][0:2]
        self.minimum_size = AVAILABLE_IMAGESIZES[sizesetting][2]

        self.apiconfig = {}
        for provider in ('fanarttv', 'tvdb', 'tmdb', 'tadb'):
            key = addon.get_setting('apikey.' + provider).strip()
            self.apiconfig[provider] = {
                'apikey': key,
                'apikey-builtin': not key,
                'enabled': addon.get_setting('apienabled.' + provider)
            }
            if not key and projectkeys:
                self.apiconfig[provider]['apikey'] = get_projectkey(provider)
            pykodi.set_log_scrubstring(provider + '-apikey', key)

        self.pathexclusion = []
        for index in range(10):
            index_append = str(index+1)
            option = addon.get_setting('exclude.path.option_' + index_append)
            if option:
                exclusiontype = addon.get_setting('exclude.path.type_' + index_append)
                folder = addon.get_setting('exclude.path.folder_' + index_append)
                prefix = addon.get_setting('exclude.path.prefix_' + index_append)
                regex = addon.get_setting('exclude.path.regex_' + index_append)
                self.pathexclusion.append({"type": exclusiontype, "folder": folder, "prefix": prefix, "regex": regex})

        pykodi.set_log_scrubstring('fanarttv-client-apikey', self.fanarttv_clientkey)

    def get_apikey(self, provider):
        return self.apiconfig[provider]['apikey']

    def get_apienabled(self, provider):
        return self.apiconfig[provider]['enabled']

    def get_api_config(self, provider):
        return self.apiconfig[provider]

    @property
    def autoadd_episodes(self):
        return self._autoadd_episodes

    @autoadd_episodes.setter
    def autoadd_episodes(self, value):
        self._autoadd_episodes = value
        addon.set_setting('autoaddepisodes_list', value)


def get_projectkey(provider):
    return projectkeys.FANARTTV_PROJECTKEY if provider == 'fanarttv' else \
        projectkeys.THETVDB_PROJECTKEY if provider == 'tvdb' else \
        projectkeys.TMDB_PROJECTKEY if provider == 'tmdb' else \
        projectkeys.TADB_PROJECTKEY if provider == 'tadb' else \
        ''


settings = Settings()
