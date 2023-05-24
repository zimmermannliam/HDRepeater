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
python3 hdrepeater.py <root directory of batch>
```

## How to use

REQUIRED file names:
```
vignetting          -> vignetting.cal
fisheye             -> fisheye.cal
ndfilter            -> ndfilter.cal
calibration factor  -> CF.cal
response function   -> response.rsp
camera parameters   -> params.txt
```

Optionally, you may include the file:
```
none.txt
```
and list the steps you want to skip/autogenerate, which can be:
```
vignetting
fisheye
ndfilter
cf
response
```
and must be separated by newlines. This will override the existence of the file.

Batch structure:
```
<root directory of batch>
├ default .cal files
├ default .rsp files
├ default .txt file
├ outputs/
| ├ <Initially blank>
├ <hdr img 1>/
| ├ desired .cal files
| ├ desired .rsp files
| ├ img/
| | ├ img1.jpg
| | ├ ...
| | ├ imgn.jpg
├ ...
├ <hdr img n>/
| ├ desired .cal files
| ├ desired .rsp files
| ├ img/
| | ├ img1.jpg
| | ├ ...
| | ├ imgn.jpg
```

