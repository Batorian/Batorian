import requests
import os

def get_latest_tweet(bearer_token):
    user_id = '4794829459'
    url = f'https://api.twitter.com/2/users/{user_id}/tweets'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
    }
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")  # Debugging-Ausgabe
    print(f"Response Text: {response.text}")  # Debugging-Ausgabe
    if response.status_code == 200:
        tweet_data = response.json()
        latest_tweet = tweet_data['data'][0]['text']
        return latest_tweet
    elif response.status_code == 403:
        raise Exception("Forbidden: The request is understood, but it has been refused or access is not allowed.")
    elif response.status_code == 401:
        raise Exception("Unauthorized: Authentication credentials were missing or incorrect.")
    else:
        raise Exception(f"Error fetching tweets: {response.status_code}")

def update_readme(tweet):
    with open("README.md", "r") as file:
        lines = file.readlines()

    with open("README.md", "w") as file:
        in_twitter_section = False
        for line in lines:
            if line.strip() == "<!-- TWITTER:START -->":
                in_twitter_section = True
                file.write(line)
                file.write(f"{tweet}\n")
            elif line.strip() == "<!-- TWITTER:END -->":
                in_twitter_section = False
            elif not in_twitter_section:
                file.write(line)

if __name__ == "__main__":
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if bearer_token is None:
        raise Exception("TWITTER_BEARER_TOKEN environment variable is not set.")
    latest_tweet = get_latest_tweet(bearer_token)
    update_readme(latest_tweet)
