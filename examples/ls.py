# This example uses function annotations, thus it only works on Python 3.3+

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
