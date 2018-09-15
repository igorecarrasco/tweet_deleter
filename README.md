# Tweet Deleter

This is a simple `python3` script to delete old tweets beyond the platform limitations. Twitter only allows third-party developers and users to delete the latest 3200 tweets on their account, but many (such as me) have way, way more.

## How to:

Here's how you, too, can delete them old tweetes.

### Libraries
This script uses two external libraries to make the job easier: `Twython` and `PyYAML`. Install them as such:

```virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
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

The way this script works is by parsing the standard `.csv` Twitter exports when you ask for your archive. Instructions on how to download it can be found [here](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive).

Copy the `tweets.csv` file from the base directory of the archive into this applications' base directory and you're good to go.

### Running that baby

A simple 
```
python3 delete.py``` 
will suffice.
