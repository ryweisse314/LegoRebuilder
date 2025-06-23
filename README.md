# LegoRebuilder

A tool that helps you rediscover LEGO by showing you what official sets you can build using the sets you already own.

## Features

- Input LEGO sets you own (with autocomplete!)
- View official LEGO sets you can fully build using those parts
- Powered by the Rebrickable API

## Example

Own:
- 10265 (Ford Mustang)
- 75257 (Millennium Falcon)

LegoRebuilder suggests:
- 31058 (Dinosaur Creator)
- 31087 (Dune Buggy)

## Getting Started

### Requirements

- Python 3.8+
- API Key from [Rebrickable](https://rebrickable.com/api/)

### Setup

```bash
git clone https://github.com/ryweisse314/LegoRebuilder.git
cd LegoRebuilder
pip install -r requirements.txt
touch .env  # Add REBRICKABLE_KEY=your_api_key
python backend/app.py
