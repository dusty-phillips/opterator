from setuptools import setup
import opterator

setup(
        name="opterator",
        version=opterator.__version__,
        py_modules=['opterator', 'test_opterator'],
        author="Dusty Phillips",
        author_email="dusty@buchuki.com",
        license="MIT",
        keywords="opterator option parse parser options",
        url="http://github.com/buchuki/opterator/",
        description="Easy option parsing introspected from function signature.",
        long_description="""A decorator for a script's main
entry point that uses a function signature and docstring to
pseudo-automatically create an option parser. When invoked, the option parser
automatically maps command-line arguments to function parameters.""",
        download_url="http://cloud.github.com/downloads/buchuki/opterator/opterator-0.1.tar.gz",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
        ]        )
