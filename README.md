<div align="center">
    <img src="https://storage.googleapis.com/lupeke.dev/telegen.png" alt="telegen" width="250" /><br />
</div>

# About

A simple AI chatbot that integrates ChatGPT API on Telegram.

## Basic usage

### Requirements

* Python >= 3.11.
* [OpenAI](https://beta.openai.com/account/api-keys) and [Telegram](https://core.telegram.org/bots/features#botfather) authorization tokens.

### Running

1. Rename `.env.template` and provide your own `TELEGRAM_TOKEN` and `OPENAI_API_KEY`. 
2. Build the Docker image.
```shell
docker build -t telegen .
```
4. Create and run the container.
```shell
docker run --rm -v $(pwd):/usr/local/src -p 5000:5000 --env-file=.env telegen
```
5. Visit [localhost:5000](http://localhost:5000) in your browser. 

### Commands

* `/restart` to clear chat history.
* `/system <instruction>` will change the behavior of the assistant.

## Deploy

This project should be easily deployable as a Cloud Run service on GCP. Just make sure to set up all environment variables and change the _maximum number of instances_ to 1 (you shouldn't have more than one bot instance running at the same time).

<hr />
Icons created by <a href="https://www.flaticon.com/free-icons/pinocchio" title="pinocchio icons">rcherem</a>
and <a href="https://www.flaticon.com/free-icons/botnet" title="botnet icons">juicy_fish</a> - Flaticon
