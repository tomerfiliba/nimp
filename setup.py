from distutils.core import setup

long_desc = open("README", "r").read()

setup(name = "nimp",
    version = "0.9",
    description = "Nested Imports for Python",
    author = "Tomer Filiba",
    author_email = "tomerfiliba@gmail.com",
    license = "MIT",
    url = "http://github.com/tomerfiliba/nimp",
    py_modules = ['nimp'],
    keywords = "import hook, nested packages, namespace packages, java-like packages",
    long_description = long_desc,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

