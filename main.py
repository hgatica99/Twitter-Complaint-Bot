from twitterBot import InternetSpeedTwitterBot

PROMISED_UP = 500
PROMISED_DOWN = 500
PROVIDER = "users_provider"
USER_NAME = "users_login"
PASSWORD = "users_password"

bot = InternetSpeedTwitterBot(upload=PROMISED_DOWN, download=PROMISED_DOWN, provider=PROVIDER)

bot.get_internet_speed()

if not bot.results_match():
    bot.tweet_at_provider(user_name=USER_NAME, password=PASSWORD)
