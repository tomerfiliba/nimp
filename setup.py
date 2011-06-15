from distutils.core import setup

long_desc = open("README", "r").read()

setup(name = "nimp",
    version = "0.9.2",
    description = "Nested Imports for Python",
    author = "Tomer Filiba",
    author_email = "tomerfiliba@gmail.com",
    license = "MIT",
    url = "http://github.com/tomerfiliba/nimp",
    py_modules = ['nimp'],
    platform = "OS Independent",
    keywords = "import hook, nested packages, namespace packages, java-like packages",
    long_description = long_desc,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.3",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2" ,       
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

