import sys
import os
import unittest
import nimp
import shutil


class Test_Distribution(unittest.TestCase):
    def setUp(self):
        self.workdir = os.getcwd()
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__name__), "proj")))

    def tearDown(self):
        os.chdir(self.workdir)

    def test_sdist(self):
        shutil.rmtree("build", True)
        shutil.rmtree("dist", True)
        self.assertEqual(os.system("python setup.py sdist"), 0)
        shutil.rmtree("build", True)
        shutil.rmtree("dist", True)
    
    def test_install(self):
        shutil.rmtree("tmp", True)
        self.assertEqual(os.system("python setup.py install --prefix=tmp"), 0)
        for dir, subdirs, files in os.walk("tmp"):
            if os.path.basename(dir) == "foo-bar-baz" and "__init__.py" in files:
                break
        else:
            self.fail("could not find foo-bar-baz/__init__.py")
        shutil.rmtree("tmp", True)


if __name__ == '__main__':
    unittest.main()
