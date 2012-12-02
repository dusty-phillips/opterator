'''So you want a quick and dirty command line app without screwing around
with optparse or getopt, but also without a complicated if-else on the length
of sys.argv. You don't really need a comprehensive help file, cause it's just
you running the script and knowing what options are available is enough.
How many boilerplate lines of code is it gonna take?'''

from opterator import opterate                      # 1


@opterate                                           # 2
def main(filename, color='red', verbose=False):     # 3
    print(filename, color, verbose)

main()                                              # 4

''' Answer: 4 lines.

You get a program that you can call on the command line like so:

  $ python examples/basic.py this_file
  this_file red False

or so:

  python examples/basic.py this_file --color=blue
  this_file blue False

or even so:

  $ python examples/basic.py --color=purple another_file --verbose
  another_file purple True

And you get a not too useless helpfile:

  $ python examples/basic.py -h
  Usage: basic.py [options] filename



Options:
  -h, --help            show this help message and exit
  -c COLOR, --color=COLOR
  -v, --verbose
'''