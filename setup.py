import ez_setup
ez_setup.use_setuptools()
from setuptools import setup
import opterator

setup(
        name = "opterator",
        version = opterator.__version__,
        py_modules = ['opterator'],
        author = "Dusty Phillips",
        author_email = "dusty@linux.ca",
        license = "MIT",
        keywords = "opterator option parse parser options",
        url = "http://github.com/buchuki/opterator/",
        long_description = """At heart, a decorator for a script's main
entry point that uses a function function signature and docstring to
pseudo-automatically create an option parser. When invoked, the option parser
automatically maps command-line arguments to function parameters.""",
        download_url = "http://cloud.github.com/downloads/buchuki/opterator/opterator-0.1.tar.gz"
        )
