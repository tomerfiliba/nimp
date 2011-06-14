import sys
import os
import nimp

class Test_Nimp(object):
    def setup(self):
        nimp.install()
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), "path1")))
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), "path2")))

    def teardown(self):
        nimp.uninstall()

    def test_simple(self):
        from foo.bar.eggs import f1           # root package
        from foo.bar.eggs.ham import f2       # sub-packaged
        from foo.bar.eggs.bacon import f4     # root package merged as logical sub-package
        from foo.bar.spam import f3           # root package
        
        assert f1() == "foo.bar.eggs"
        assert f2() == "foo.bar.eggs.ham"
        assert f4() == "foo.bar.eggs.bacon"
        assert f3() == "foo.bar.spam"
    
    def test_relative(self):
        from foo.bar.eggs.bacon.relative import f5

        assert f5() == "foo.bar.eggs.bacon.relative calling foo.bar.eggs.ham"



