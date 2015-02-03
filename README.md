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

Use:
```
$ ./cli.py -h
usage: cli.py [-h] [-a RANK] [-m RANK] [-t TONE] [-s TYPE] [-p TYPE]
              [-sb TYPE] [-o OUTPUT_IMAGE] [-c MASK]
              input_image

Script for linear and nonlinear image filtering. LG 2015

positional arguments:
  input_image           input image filename

optional arguments:
  -h, --help            show this help message and exit
  -a RANK, --average RANK
                        average mask
  -m RANK, --median RANK
                        median transform
  -t TONE, --tone TONE  tone mask, must be between 0 and 1
  -s TYPE, --sharpen TYPE
                        sharpen transform mask
  -p TYPE, --prewitt TYPE
                        prewitt transform mask
  -sb TYPE, --sobel TYPE
                        sobel transform mask
  -o OUTPUT_IMAGE, --output OUTPUT_IMAGE
                        output image filename
  -c MASK, --custom MASK
                        custom mask transform
```
