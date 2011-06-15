import sys
import os
import unittest
import nimp


class Test_Nimp(unittest.TestCase):
    def setUp(self):
        nimp.install()
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), "path1")))
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), "path2")))

    def tearDown(self):
        nimp.uninstall()

    def test_simple(self):
        from foo.bar.eggs import f1           # root package
        from foo.bar.eggs.ham import f2       # sub-packaged
        from foo.bar.eggs.bacon import f4     # root package merged as logical sub-package
        from foo.bar.spam import f3           # root package
        
        self.assertEqual(f1(), "foo.bar.eggs")
        self.assertEqual(f2(), "foo.bar.eggs.ham")
        self.assertEqual(f4(), "foo.bar.eggs.bacon")
        self.assertEqual(f3(), "foo.bar.spam")
    
    def test_relative(self):
        from foo.bar.eggs.bacon.relative import f5

        self.assertEqual(f5(), "foo.bar.eggs.bacon.relative calling foo.bar.eggs.ham")

    def test_absolute(self):
        from foo.bar.eggs.bacon.absolute import f6

        self.assertEqual(f6(), "foo.bar.eggs.bacon.absolute calling foo.bar.eggs.ham")


if __name__ == '__main__':
    unittest.main()
