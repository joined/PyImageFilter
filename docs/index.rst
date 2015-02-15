########################
Welcome to PyImageFilter
########################

Welcome to the PyImageFilter |version| documentation.

============
Installation
============
Clone the package from Github::

    $ git clone https://github.com/joined/pyimagefilter
    $ cd pyimagefilter

Create a new virtual enviroment named ``.env`` with the Python 3 executable, and activate it::

    $ virtualenv .env -p $(which python3)
    $ source .env/bin/activate

Install the required packages with ``pip``::

    $ pip install -r requirements.txt

That's all!

=====
Usage
=====
This toolkit includes a command line tool, represented by the file ``cli.py``.

Like every command line tool, there's an help function::

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

There is one mandatory argument, which is the input image, and several optional arguments.

The arguments ``average``, ``gauss``, ``sharpen``, ``prewitt``, ``average``
