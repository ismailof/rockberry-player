class ImageUtils(object):

    # TODO: Get base directory to do relative searching
    IMG_LOGO = 'neon_R.jpg'
    IMG_NONE = 'transparent.png'

    @staticmethod
    def get_type_image(reftype):
        IMAGES_TYPE = {'directory': 'browse_folder.png',
                       'playlist': 'browse_pl.png',
                       'track': 'default_track.png',
                       'album': 'default_album.jpg',
                       'artist': 'browse_artist.png'}
        return IMAGES_TYPE.get(reftype) or ImageUtils.IMG_LOGO

    @staticmethod
    def atlas_image(atlas, item, default=IMG_NONE):
        if not atlas:
            return default

        return 'atlas://{}/{}'.format(
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
