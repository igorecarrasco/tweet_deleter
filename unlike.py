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
        with open(keys_file, "r") as file:
            keys = yaml.safe_load(file)

        self.twitter = Twython(*keys.values())

        try:
            self.twitter.verify_credentials()
        except TwythonAuthError:
            print("Invalid (or missing) credentials.")
            sys.exit()

    def pull_ids(self) -> list:
        """
        Pulls latest 20 likes from user
        """
        likes = self.twitter.get_favorites(count=200)
        like_ids = [i.get("id") for i in likes]

        return like_ids

    def delete_likes(self, like_ids: list) -> int:
        """
        Deletes tweets from a list of tweet ids.

        Parameters:
        ----------
        like_ids: list
            List of liked tweet ids.
        """
        count = 0

        for like_id in like_ids:
            try:
                self.twitter.destroy_favorite(id=like_id)
                count += 1
            except TwythonRateLimitError as e:
                time.sleep(int(e.retry_after))
                continue
            except TwythonError as e:
                print(str(e))

        return count


if __name__ == "__main__":
    spin = SpinCursor(msg="Running Tweet Unliker.", speed=2)
    spin.start()
    unliker = TwitterUnlike()

    while True:
        try:
            ids = unliker.pull_ids()
            returns = unliker.delete_likes(ids)
        except TwythonError:
            break
        except KeyboardInterrupt:
            break

    print(f"Unliked {returns} tweets.")
    spin.stop()
