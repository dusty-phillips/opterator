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
        download_url="https://github.com/buchuki/opterator/archive/%s.tar.gz" % opterator.__version__,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
        ]
    )
