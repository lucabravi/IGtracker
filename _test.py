from ensta import Guest
from .utils import get_media_type

account = "nekogirlsart"

guest = Guest()
profile = guest.profile(account)

follower_count = profile.follower_count
following_count = profile.following_count
total_post_count = profile.total_post_count
print(f'follower_count: {follower_count}, following_count: {following_count}, total_post_count: {total_post_count}')

posts = guest.posts(account)
for post in posts:
    post_id = post.post_id
    media_type = get_media_type(post.media_type)
    posted_at = post.taken_at
    comment_count = post.comment_count
    like_count = post.like_count

    print(f'post_id: {post_id}, media_type: {media_type}, posted_at: {posted_at}, comment_count: {comment_count}, like_count: {like_count}')
