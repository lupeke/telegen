# TeleGPT Chatbot
A simple chatbot that integrates the OpenAI's ChatGPT API to provide an AI powered chat experience on Telegram.

## Basic usage
1. Rename `config.example.toml` to `config.toml` and open it.
2. Provide your own `TELEGRAM_TOKEN` and `OPENAI_API_KEY` (visit [OpenAI](https://beta.openai.com/account/api-keys) and 
[Telegram](https://core.telegram.org/bots/features#botfather) if you don't have these authorizations).
2. Build the Docker image.
```shell
docker build -t telegpt .
```
4. Create and run the container
```shell
docker run --rm -it telegpt
```
Add `--volume $(pwd):/usr/src/telegpt` to play with the code.
