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
usage: cli.py [-h] [--average RANK] [--median RANK] [--tone TONE]
              [--sharpen TYPE] [--prewitt TYPE] [--sobel TYPE]
              [--output OUTPUT_IMAGE] [--custom MASK]
              input_image

Toolkit for linear and nonlinear image filtering. LG 2015

positional arguments:
  input_image           input image filename

optional arguments:
  -h, --help            show this help message and exit
  --average RANK        average mask
  --median RANK         median transform
  --tone TONE           tone mask, must be between 0 and 1
  --sharpen TYPE        sharpen transform mask
  --prewitt TYPE        prewitt transform mask
  --sobel TYPE          sobel transform mask
  --output OUTPUT_IMAGE
                        output image filename
  --custom MASK         custom mask linear filter, json-style format
```

Example:
```
$ ./cli.py my_image.jpg --sharpen=1 --tone=0.5 --average=5 --output=output_image.jpg
Opening file "my_image.jpg"...
Image file opened.
Applying sharpen mask type 1...
Applying tone mask with tone 0.5...
Applying average mask with size 5x5...
Filtering completed.
Saving file to "output_image.jpg"...
File saved.
```
