Opterator
=========
Opterator is an option parsing script for Python that takes the boilerplate out
of option parsing.

Opterator is based on the idea that a main() function for a script can be
decorated to allow command-line arguments to be translated into method
parameters. This allows it to be self-documenting, and reduces errors in
creating and assigning options. I don't know if you'd want to use it for large
scripts, but it's really useful for quick and dirty ones where you can't decide
if you want to bother with optparse, but querying sys.argv manually is a bit
too complicated.

For example, an optparse program for renaming a file might look like this:

.. code-block:: python

  from optparse import OptionParser
  def main():
      '''main entrypoint for renaming files. Accept two options, backup
      and interactive'''
      parser = OptionParser(usage="A script for renaming files")
      parser.add_option('-b', '--backup', action=store_true,
          help='backup the file')
      parser.add_option('-p', '--interactive', action=store_true,
          help='interactively move files')
      # Move the file
      
  if __name__ == '__main__':
      main()


The equivalent code using opterator looks like this:

.. code-block:: python

  from opterator import opterate
  @opterate
  def main(source, dest, backup=False, interactive=False):
      '''A script for renaming files
      :param backup: backup the file
      :param interactive: -p --interactive interatively
      move files...     '''
      # Move the file
   
  if __name__ == '__main__':
      main()

Opterator automatically generates help messages from the docstring. The main part
of the docstring becomes the main part of the help string. The individual 
parameter docstrings become the helptext for the arguments. By default, the
long and short form of a given parameter come from the parameter name and the
first character of the parameter name. You can replace either or both of these
by adding options that begin with a ``-`` character between the parameter and
the helptext.

If your
main function looks like this:

.. code-block:: python

  @opterate
  def main(filename1, filename2, recursive=False, backup=False,
          suffix='~', *other_filenames):
      '''An example copy script with some example parameters that might
      be used in a copy command.
      
      :param recursive: copy directories
          recursively
      :param backup: -b --backup backup any files you copy over
      :param suffix: -S --suffix override the usual backup
          suffix '''
      pass

Your help text will look like this::

  dusty:opterator $ python copy.py -h
  Usage: copy.py [options] filename1 filename2 [other_filenames]

  An example copy script with some example parameters that might
      be used in a copy command.
      
  Options:
    -h, --help            show this help message and exit
    -r, --recursive       copy directories recursively
    -b, --backup          backup any files you copy over
    -S SUFFIX, --suffix=SUFFIX
                          override the usual backup suffix

