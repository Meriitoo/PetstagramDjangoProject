def apply_likes_count(photo):
    photo.likes_count = photo.photolike_set.count()  # queryset all, filter, orderby
    return photo


def apply_user_liked_photo(photo):
    # TODO: fix this for current user when authentication is available

    photo.is_liked_by_user = photo.likes_count > 0
    return photo

