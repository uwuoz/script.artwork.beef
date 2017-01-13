
from lib import mediatypes
from base import ProviderError

from artfiles import ArtFilesSeriesProvider, ArtFilesMovieProvider, ArtFilesEpisodeProvider
from fanarttv import FanartTVSeriesProvider, FanartTVMovieProvider
from nfofile import NFOFileSeriesProvider, NFOFileMovieProvider, NFOFileEpisodeProvider
from themoviedb import TheMovieDBProvider, TheMovieDBEpisodeProvider
from thetvdbv2 import TheTVDBProvider

external = {
    mediatypes.TVSHOW: (TheTVDBProvider(), FanartTVSeriesProvider()),
    mediatypes.MOVIE: (TheMovieDBProvider(), FanartTVMovieProvider()),
    mediatypes.EPISODE: (TheMovieDBEpisodeProvider(),)
}

forced = {
    mediatypes.TVSHOW: (ArtFilesSeriesProvider(), NFOFileSeriesProvider()),
    mediatypes.MOVIE: (ArtFilesMovieProvider(), NFOFileMovieProvider()),
    mediatypes.EPISODE: (ArtFilesEpisodeProvider(), NFOFileEpisodeProvider())
}