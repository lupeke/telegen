import logging
import tomllib
from pathlib import Path


confpath = Path(__file__).parent / 'config.toml'
with confpath.open(mode='rb') as cf:
    cfg = tomllib.load(cf)


# Set up basic logging
def load_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[CHATBOT] %(levelname)s: %(asctime)s => %(message)s',
        datefmt='%m/%d/%Y @ %I:%M%p')
    return logging
