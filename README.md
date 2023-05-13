<div align="center">
    <img src="https://storage.googleapis.com/lupeke/telegen.png" alt="telegen" width="250" /><br />
</div>

# telegen

A simple generative chatbot that integrates OpenAI's ChatGPT API to provide an AI-powered chat experience on Telegram.

## Basic usage

### Requirements

* Python >= 3.11
* [OpenAI](https://beta.openai.com/account/api-keys) and [Telegram](https://core.telegram.org/bots/features#botfather) authorization tokens

### Running

1. Rename `config.example.toml` to `config.toml` and open it.
2. Provide your own `TELEGRAM_TOKEN` and `OPENAI_API_KEY`
3. Build the Docker image.
```shell
docker build -t telegen .
```
4. Create and run the container
```shell
docker run --rm -it telegen
```
Add `--volume $(pwd):/usr/src/telegen` if you want play with the code.

### Commands

* `/restart` to clear chat history
* `/system [instruction]` will change the behavior of the assistant

## Wishlist

- [ ] Use Redis to handle chat history
- [ ] Create CD pipeline actions
- [ ] Add unit tests
