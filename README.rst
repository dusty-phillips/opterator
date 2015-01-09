Opterator
=========
Opterator is an option parsing script for Python that takes the boilerplate out
of option parsing.

Opterator is based on the idea that a main() function for a script can be
decorated to allow command-line arguments to be translated into method
parameters. This allows it to be self-documenting, and reduces errors in
creating and assigning options. I don't know if you'd want to use it for large
programs, but it's really useful for quick and dirty ones where you can't
decide if you want to bother with argparse, but querying sys.argv manually is a
bit too complicated.

For example, you can document a simple program for renaming a file using
opterator like this:

.. code-block:: python

  from opterator import opterate
  @opterate
  def main(source, dest, backup=False, interactive=False):
      '''A script for renaming files
      :param source: the source file
      :param dest: the destination
      :param backup: backup the file
      :param interactive: -p --interactive interatively
      move files...     '''
      # Move the file
   
  if __name__ == '__main__':
      main()

For comparison, an optparse program would take several more less readable 
lines of code:

.. code-block:: python

  from argparse import ArgumentParser

  def main():
      '''main entrypoint for renaming files. Accept two options, backup
      and interactive'''
      parser = ArgumentParser(usage="A script for renaming files")
      parser.add_argument("source", help="the source file")
      parser.add_argument("dest", help="the destination")
      parser.add_argument('-b', '--backup', action="store_true",
          help='backup the file')
      parser.add_argument('-p', '--interactive', action="store_true",
          help='interactively move files')
      arguments = parser.parse_args()
      # Move the file
      
  if __name__ == '__main__':
      main()


Opterator automatically generates help messages from the docstring. The main
part of the docstring becomes the main part of the help string. The individual
parameter docstrings become the helptext for the arguments. By default, the
long and short form of a given parameter come from the parameter name and the
first character of the parameter name. In Python 3, you can replace this with
a function annotation; or in Python 2 or 3 you can replace them by adding
options that begin with a ``-`` character between the parameter and the
docstring.

So, if your main function looks like this:

.. code-block:: python

  from opterator import opterate


  @opterate
  def main(filename1, filename2, recursive=False, backup=False,
           suffix='~', *other_filenames):
      '''An example copy script with some example parameters that might
      be used in a file or directory copy command.

      :param recursive: -r --recursive copy directories
          recursively
      :param backup: -b --backup backup any files you copy over
      :param suffix: -S --suffix override the usual backup
          suffix '''
      filenames = [filename1, filename2] + list(other_filenames)
      destination = filenames.pop()

      print("You asked to move %s to %s" % (filenames, destination))
      if recursive:
          print("You asked to copy directories recursively.")
      if backup:
          print("You asked to backup any overwritten files.")
          print("You would use the suffix %s" % suffix)

  if __name__ == '__main__':
      main()

Your help text will look like this::

.. code-block:: sh

  dusty:opterator $ python cp.py -h
  usage: cp.py [-h] [-r] [-b] [-S SUFFIX]
               filename1 filename2 [other_filenames [other_filenames ...]]

  An example copy script with some example parameters that might be used in a
  file or directory copy command.

  positional arguments:
    filename1
    filename2
    other_filenames

  optional arguments:
    -h, --help            show this help message and exit
    -r, --recursive       copy directories recursively
    -b, --backup          backup any files you copy over
    -S SUFFIX, --suffix SUFFIX
                          override the usual backup suffix

If you want to try out the funky function annotation syntax, give this
a shot:

.. code-block:: python

  from opterator import opterate


  @opterate
  def main(show_details:['-l']=False, cols:['-w', '--width']='', *files):
      '''
      List information about a particular file or set of files

      :param show_details: Whether to show detailed info about files
      :param cols: specify screen width
      '''
      print(files)
      print(show_details)
      print(cols)

  if __name__ == '__main__':
      main()


