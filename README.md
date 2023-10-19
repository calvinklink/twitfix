# Twitfix Discord Bot

A simple Discord python bot based on [pycord](https://github.com/Pycord-Development/pycord) API that replaces Discord messages containing Twitter/X links with [FixTweet](https://github.com/FixTweet/FixTweet) embeds.

### Features:
- Replaces messages containing multiple links
- Quotes original message content and formatting if present
- Strips URL tracking params
- Fixes video embeds in Discord
- Replaces message replies
- Optionally configure bot on a per-server basis via slash commands and Redis.
- View bot statistics via /info

## Running
Install requirements `pip install -r requirements.txt`

Create a `.env` file in the `main.py` directory containing your API key:
`TOKEN='APIKEY'`

At the very least, this bot requires `&permissions=10240&scope=bot` (**bot** scope: **Send Messages** and **Manage Messages**)

## Screenshot Example
![image](https://github.com/calvinklink/twitfix/assets/73358533/c3f60efc-260b-477d-ae32-40186a0fc735)
