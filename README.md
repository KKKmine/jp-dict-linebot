# Japanese Dictionary Line Bot
* Search a Japanese word using kanji, kana or romaji by sending message to LINE bot
* The dictionary is crawled from [dict.ac](https://dict.asia/).

# Preparation
* Get a LINE Channel form [LINE developers](https://developers.line.biz/en/)

# Deploy on Heroku
1. Get the channel secret and channel access token from LINE Developers Console. They will be found in **Basic settings > Channel secret** and  **Messaging API > Channel access token**.
2. Add `LINE_CHANNEL_ACCESS_TOKEN` and `LINE_CHANNEL_SECRET` in **Heroku app > Settings > Config Vars** and fill the values from step 1 you get.
3. Set Webhook URL in **Messaging API > LINE bot channel** to `https://{your Heroku app names}.herokuapp.com/jpdictbot/callback`
4. Deploy the project to Heroku

# Deploy on your PC
1. Get the channel secret and channel access token from LINE Developers Console. They will be found in **Basic settings > Channel secret** and  **Messaging API > Channel access token**.
2. Change `LINE_CHANNEL_ACCESS_TOKEN` and `LINE_CHANNEL_SECRET` in **mylinebot/setting.py** to the values from step 1 you get.
3. Change `ALLOWED_HOSTS` in **mylinebot/setting.py** to your domain. Use [ngrok](https://ngrok.com/) if you don't have one.
4. Run python
    ```
    python manage.py runserver
    ```