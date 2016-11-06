from music.cache import MediaCache


class ImageUtils(object):

    # TODO: Get base directory to do relative searching
    BASE_FOLDER = '/home/pi/rockberry-player/rockberry_player'
    IMG_FOLDER = BASE_FOLDER + '/images/'
    IMG_LOGO = IMG_FOLDER + 'neon_R.jpg'
    IMG_NONE = IMG_FOLDER + 'transparent.png'

    @classmethod
    def atlas_image(cls, atlas, item):
        if not atlas:
            return cls.IMG_NONE

        return 'atlas://{}{}/{}'.format(
            cls.IMG_FOLDER,
            atlas,
            item or 'null')

    @staticmethod
    def get_fittest_image(imagelist=[], size=None):

        def compare(a, b):
            return max(a, b) / float(min(a, b)) if a and b else 1.0

        if not imagelist:
            return ''

        if not size or len(imagelist) == 1:
            # Select first image
            item_fit = 0
        else:
            # Select closest image to size
            size_diff = [compare(image.get('width', 0) + image.get('height', 0),
                                 size[0] + size[1])
                         for image in imagelist]
            item_fit = size_diff.index(min(size_diff))

        image_url = imagelist[item_fit].get('uri', '')

        return image_url


# TODO: Total refactor. 
# Not inherit MediaCache but using cache object
# Rename to ImageItem ¿?
# Move most of AlbumCover (related to server images) here
class ImageCache(MediaCache):

    _cache = {}
    _requested_uris = set()
    _callbacks = {}
    interface = None

