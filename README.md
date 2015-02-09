# Image filtering Python toolkit

This is a personal project, concerning the implementation of an image filtering toolkit in Python.

It's written in Python 3.4.

## Usage

Configure virtual enviroment and install requirements:
```bash
$ virtualenv .env -p $(which python3)
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Help:
```
$ ./cli.py -h
usage: cli.py [-h] [--average RANK] [--gauss STDEV,RANK] [--tone TONE]
              [--sharpen TYPE] [--prewitt TYPE] [--sobel TYPE] [--custom MASK]
              [--output OUTPUT_IMAGE]
              input_image

Toolkit for linear and nonlinear image filtering

positional arguments:
  input_image           Input image file name.

optional arguments:
  -h, --help            show this help message and exit
  --average RANK        average mask transform. rank must be unven
  --gauss STDEV,RANK    gauss average transform. rank must be uneven
  --tone TONE           tone mask transform. value between 0 and 1
  --sharpen TYPE        sharpen mask transform. available types 1,2,3
  --prewitt TYPE        prewitt mask transform. available types 1,2
  --sobel TYPE          sobel mask transform. available types 1,2
  --custom MASK         custom mask linear filter, json-style format
  --output OUTPUT_IMAGE
                        output image filename
```

Example:
```
$ ./cli.py image.jpg --gauss 2,5 --output output_image.jpg
> Opening file "image.jpg"...
> Image file opened.
> Applying Gauss filter with stdev 2.0 and size 5x5...
> Filtering completed.
> Saving file to "output_image.jpg"...
> File saved.
```
