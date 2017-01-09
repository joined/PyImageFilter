# Image filtering Python toolkit

This is a personal project, concerning the implementation of an image filtering toolkit in Python.

It's written in Python 3.4.

## Installation
```
$ git clone https://github.com/joined/pyimagefilter
$ cd pyimagefilter
$ virtualenv .env -p $(which python3)
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Usage

```
$ ./cli.py -h
usage: cli.py [-h] [--average RANK] [--gauss STDEV,RANK] [--sharpen TYPE]
              [--prewitt TYPE] [--sobel TYPE] [--volterra COEFFICIENT_FILE]
              [--custom MASK] [--no-parallel] [--output OUTPUT_IMAGE]
              input_image

Toolkit for linear and nonlinear image filtering

positional arguments:
  input_image           Input image file name.

optional arguments:
  -h, --help            show this help message and exit
  --average RANK        average mask transform. rank must be unven
  --gauss STDEV,RANK    gauss average transform. rank must be uneven
  --sharpen TYPE        sharpen mask transform. available types 1,2,3
  --prewitt TYPE        prewitt mask transform. available types 1,2
  --sobel TYPE          sobel mask transform. available types 1,2
  --volterra COEFFICIENT_FILE
                        quadratic volterra filtering. file must be json
  --custom MASK         custom mask linear filter, json-style format
  --no-parallel         disable parallel execution
  --output OUTPUT_IMAGE
                        output image filename
```

## License and Copyright

See `LICENSE`.
