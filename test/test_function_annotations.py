from opterator import opterate
import py


class Checker(object):
    '''Just something to get closure-like behaviour so I can call the internal
    function and set or check values to ensure the decorator is behaving
    correctly.'''
    pass


def test_annotated_keyword_arg():
    result = Checker()

    @opterate
    def main(var1, var2: ["-m", "--variable"]=""):
        result.var1 = var1
        result.var2 = var2

    main(["hello", "--variable", "world"])
    assert result.var1 == "hello"
    assert result.var2 == "world"

    main(["hello2", "-m", "world2"])
    assert result.var1 == "hello2"
    assert result.var2 == "world2"

    main(["hello3"])
    assert result.var1 == "hello3"
    assert result.var2 == ""


def test_annotated_keyword_arg_default_helptext():
    capture = py.io.StdCapture()

    @opterate
    def main(var1, var2: ["-m", "--variable"]=""):
        'list files'
        pass
    py.test.raises(SystemExit, main,
                   ['--help'])
    out, error = capture.reset()
    assert error == ''
    assert out.strip() == """usage: py.test [-h] [-m VAR2] var1

list files

positional arguments:
  var1

optional arguments:
  -h, --help            show this help message and exit
  -m VAR2, --variable VAR2"""


def test_annotated_keyword_arg_param_helptext():
    capture = py.io.StdCapture()

    @opterate
    def main(var1, var2: ["-m", "--variable"]=""):
        '''list files
        :param var1: The first variable
        :param var2: The second variable'''
        pass
    py.test.raises(SystemExit, main,
                   ['--help'])
    out, error = capture.reset()
    assert error == ''
    print(out.strip())
    assert out.strip() == """usage: py.test [-h] [-m VAR2] var1

list files

positional arguments:
  var1                  The first variable

optional arguments:
  -h, --help            show this help message and exit
  -m VAR2, --variable VAR2
                        The second variable"""
