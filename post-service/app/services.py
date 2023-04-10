import logging


from app import reposistory


def delete_user_posts(username):
    try:
        logging.info(f"Deleting {username}'s posts")
        posts = reposistory.get_by_username(username)
        for post in posts:
            reposistory.delete(str(post[0]), post[1])

    except Exception as e:
        logging.error(f"Failed to delete {username}'s posts: {e}")
