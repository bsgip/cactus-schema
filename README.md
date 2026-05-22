# cactus-schema

Public facing models for the various CACTUS APIs

## Usage

`uv add cactus-schema`

`pip install cactus-schema`


## Development

Clone repo - then run:

```
# With uv
uv sync --all-extras
uv run pytest

# With pip
pip install -e .[dev,test,client]
pytest
```