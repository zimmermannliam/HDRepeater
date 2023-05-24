# HDRepeater
An application for series-processing High Dynamic Range images using HDRGen and Radiance

## Description
This project is meant to give a way to go and grab a coffee while all your calibrated High Dynamic Range images generate.

## Getting Started

### Dependencies

- Tested on Arch Linux
- Python 3.11.3
- SSH authentication in GitHub (needed for submodule update)

### Installing

```bash
$ git clone https://github.com/zimmermannliam/HDRepeater.git
$ cd HDRepeater
$ git submodule update --init --recursive --remote
$ pip3 install -r requirements.txt
```

### Executing program

``` bash
python3 hdrepeater.py example.json
```

## How to use

See example.json
