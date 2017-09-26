from __future__ import division


class ImageUtils(object):

    IMG_LOGO = 'neon_R.jpg'
    IMG_NONE = 'transparent.png'

    IMAGES_TYPE = {
        'directory': 'browse_folder.png',
        'playlist': 'browse_pl.png',
        'track': 'default_track.png',
        'album': 'default_album.jpg',
        'artist': 'browse_artist.png'}

    @staticmethod
    def get_type_image(reftype):
        return ImageUtils.IMAGES_TYPE.get(reftype) or ImageUtils.IMG_LOGO

    @staticmethod
    def atlas_image(atlas, item, default=IMG_NONE):
        if not atlas:
            return default

        return 'atlas://{}/{}'.format(
            atlas,
            item or 'null')

    @staticmethod
    def get_fittest_image(imagelist=[], size=None):

        if not imagelist:
            return {}  # imagelist is a list of dicts
        if not size or len(imagelist) == 1:
            return imagelist[0]

        def abs_ratio(a, b):
            return max(a, b) / min(a, b) if a and b else float('inf')

        def compare_to_size (image):
            return abs_ratio(
                image.get('width', 0) + image.get('height', 0),
                size[0] + size[1])

        return min(imagelist, key=compare_to_size)
