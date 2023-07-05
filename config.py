import tomllib
from pathlib import Path


confpath = Path(__file__).parent / 'config.toml'
with confpath.open(mode='rb') as cf:
    cfg = tomllib.load(cf)
