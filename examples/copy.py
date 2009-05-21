from opterator import opterate
@opterate
def main(filename1, filename2, recursive=False, backup=False,
        suffix='~', *other_filenames):
    '''An example copy script with some example parameters that might
    be used in a copy command.
    
    @param recursive store_true -r --recursive copy directories
        recursively
    @param backup store_true -b --backup backup any files you copy over
    @param suffix store -S --suffix override the usual backup
        suffix '''
    filenames = [filename1, filename2] + list(other_filenames)
    destination = filenames.pop()

    print "You asked to move %s to %s" % (filenames, destination)
    if recursive:
        print "You asked to copy directories recursively."
    if backup:
        print "You asked to backup any overwritten files."
        print "You would use the suffix %s" % suffix

if __name__ == '__main__':
    main()
