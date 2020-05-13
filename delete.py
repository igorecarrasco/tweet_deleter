"""
Deletes old tweets based on the standard
Twitter history .csv file provided when
exporting an user's twitter history.

Instructions on how to download such
history can be found under this link:

https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive
"""
import csv
import sys
import time
import json

from twython import Twython
from twython.exceptions import TwythonRateLimitError, TwythonError, TwythonAuthError
import yaml

from spinner import SpinCursor


class TwitterDelete:
    """
    Deletes old tweets.
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

    def pull_ids(self, file_name: str = "tweet.js", deleted_csvs: str = "deleted.csv") -> list:
        """
        Reads a Twitter .csv file and returns a
        list of IDs from an users' history.

        Parameters:
        ----------
        file_name: str
            A file name for the Tweet archive
        """
        tweet_ids: list = []
        deleted_ids: list = []

        with open(file_name, "r") as file:
            tweets = file.readlines()[1:]
            tweets.insert(0, "[{")
            tweets = "".join(tweets)

            tweet_history = json.loads(tweets)

            for row in tweet_history:
                tweet_ids.append(row["tweet"].get("id"))

        try:
            with open(deleted_csvs, "r") as deleteds_file:
                deleted_tweets = csv.reader(deleteds_file)
                for row in deleted_tweets:
                    deleted_id = row[0]
                    deleted_ids.append(deleted_id)
        except FileNotFoundError:
            pass

        tweet_ids = list(set(tweet_ids) - set(deleted_ids))

        return tweet_ids

    def delete_tweets(self, tweet_ids: list, deleted_file_name: str = "deleted.csv") -> list:
        """
        Deletes tweets from a list of tweet ids.

        Parameters:
        ----------
        tweet ids: list
            List of tweet ids.
        """
        deleted: list = []
        persist: bool = True

        try:
            while persist == True:
                with open(deleted_file_name, "a") as deleted_file:
                    deleted_write = csv.writer(deleted_file)
                    try:
                        for tweet_id in tweet_ids:
                            try:
                                self.twitter.destroy_status(id=tweet_id)
                                deleted.append(tweet_id)
                                deleted_write.writerow([tweet_id])
                            except TwythonRateLimitError as e:
                                time.sleep(int(e.retry_after) - time.time())
                                continue
                            except TwythonError as e:
                                try:
                                    self.twitter.request(
                                        endpoint="statuses/unretweet",
                                        method="POST",
                                        params={"id": tweet_id},
                                    )

                                except TwythonError:
                                    print(str(e))
                                    continue
                                else:
                                    print(str(e))
                                    continue

                    except StopIteration:
                        persist = False
                        break

        except KeyboardInterrupt:
            return deleted

        return deleted


if __name__ == "__main__":
    spin = SpinCursor(msg="Running Tweet Deleter.", speed=3)
    spin.start()
    deleter = TwitterDelete()
    ids = deleter.pull_ids(file_name="tweet.js")
    returns = deleter.delete_tweets(ids)
    print(f"Deleted {len(returns)} tweets.")
    spin.stop()
