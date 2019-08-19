"""
Deletes old likes from Twitter.
"""
import sys
import time

from twython import Twython
from twython.exceptions import TwythonRateLimitError, TwythonError, TwythonAuthError
import yaml

from spinner import SpinCursor


class TwitterUnlike:
    """
    Deletes old likes.
    """

    def __init__(self, keys_file: str = "keys.yaml") -> None:
        self.count = 0
        with open(keys_file, "r") as file:
            keys = yaml.safe_load(file)

        self.twitter = Twython(*keys.values())

        self.twitter.verify_credentials()

    def pull_ids(self) -> list:
        """
        Pulls latest 20 likes from user
        """
        likes = self.twitter.get_favorites(count=200)
        like_ids = [i.get("id") for i in likes]

        return like_ids

    def delete_likes(self, like_ids: list) -> None:
        """
        Deletes tweets from a list of tweet ids.

        Parameters:
        ----------
        like_ids: list
            List of liked tweet ids.
        """
        for like_id in like_ids:
            try:
                self.twitter.destroy_favorite(id=like_id)
                self.count += 1
            except TwythonRateLimitError as e:
                time.sleep(int(e.retry_after) - time.time())
                continue


if __name__ == "__main__":
    spin = SpinCursor(msg="Running Tweet Unliker.", speed=2)

    try:
        unliker = TwitterUnlike()
    except TwythonAuthError as e:
        print(str(e))
        sys.exit()

    while True:
        spin.start()
        try:
            ids = unliker.pull_ids()
            unliker.delete_likes(ids)
        except TwythonRateLimitError as e:
            time.sleep(int(e.retry_after) - time.time())
        except (TwythonError, TwythonAuthError) as e:
            print(str(e))
            break
        except KeyboardInterrupt:
            break
        finally:
            spin.stop()
            print(f"Unliked {unliker.count} tweets.")
            break

    sys.exit()
