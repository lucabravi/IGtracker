def get_media_type(media_type):
    if media_type == 1:
        return "image"
    elif media_type == 2:
        return "video"
    elif media_type == 8:
        return "album"
    else:
        return "unknown"