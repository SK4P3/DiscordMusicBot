# Simple YouTube music bot for Discord
This is a simple python discord bot to play music from YouTube.

Before you can start complete the steps below:

### 1. Create new discord application
https://discord.com/developers/applications

### 2. Invite the bot to your server with administrator rights
I haven't cleand up the rights the bot need yet so admin is probably not necessary but if it works don't touch it :)

### 3. Build the docker image
`docker build . -t music-bot`

### 4. Run docker compose
`docker compose -up -d`