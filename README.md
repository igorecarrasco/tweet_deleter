# Tweet Deleter

These are a few `python3` scripts to manage old tweets beyond the platform limitations. Twitter only allows third-party developers and users to delete the latest 3200 tweets on their account, but many (such as me) have way, way more. Furthermore, removing likes is a drag. 

## How to:

Here's how you, too, can delete them old tweetes (and likes).

### Libraries
This script uses external libraries to make the job easier: `Twython` and `PyYAML`. Install  and run everything as such:

```
pip install pipenv
pipenv install
pipenv run python delete.py (or unlike.py)
```

### Keys
You will need API keys to get this baby going. 

1. Go to https://apps.twitter.com/ 
2. If you don't already have a developer account, apply for one.
3. Create a new application.
4. Get the keys under "Keys and Access Tokens"
5. Create file "keys.yaml". It should look like this:
```
client_key: "*************"
client_secret: "***************"
access_token: "**********-**********************"
token_secret: "***********************************************"
```

### Tweet history

The deleter works is by parsing the standard `.js` Twitter exports when you ask for your archive. Instructions on how to download it can be found [here](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive).

Copy the `tweet.js` file from the base directory of the archive into this applications' base directory and you're good to go.

### Running the deleter

A simple ```pipenv run python delete.py``` will suffice. Let it run for as long as you feel comfortable -- it will delete as much as it can. If you want it to stop, hit Ctrl+C to interrupt running. If you run it again, it will pick right back up from where it stopped.

### Running the unliker

Do a ```pipenv run python unlike.py``` and you're golden. Let it run, it will pick up from the latest likes next time if you Ctrl+C it.
