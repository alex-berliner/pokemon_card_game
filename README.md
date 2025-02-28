# Pokemon Cards Online

## Intro
This project provides a set of tools for interfacing with Pokemon Showdown to play online battles with real Pokemon cards!

[demo.webm](https://github.com/user-attachments/assets/be0a4c21-8879-446a-8b87-abc9e598ae17)

It can connect to real Pokemon Showdown servers to play against online players, or two clients can connect together to play head-to-head locally.

## Software requirements
Only [Raspberry Pi OS](https://www.raspberrypi.com/software/) is supported.

Raspberry Pi OS dependencies:

`sudo apt install -y npm libopenblas-dev`

## Hardware requirements
- Raspberry Pi 3 or greater
  - Pi 5 required if running the Pokemon Showdown server locally
- [PN532 dev board](https://www.elechouse.com/product/pn532-nfc-rfid-module-v4/)
- [MIFARE Classic 1K Tags](https://www.sparkfun.com/rfid-tag-adhesive-mifare-classicr-1k-13-56-mhz.html)

## Setup
Get the repository

`git clone https://github.com/alex-berliner/pokemon_card_game --recursive`

Set up your python virtual environment

```
python -m venv .pco
. .pco/bin/activate
pip install -r requirements.txt
```

- burn cards

- init service
