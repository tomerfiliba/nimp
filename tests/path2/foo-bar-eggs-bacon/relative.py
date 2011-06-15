# this module "thinks" it actually mounted on foo.bar.eggs
from ..ham import f2

def f5():
    return "foo.bar.eggs.bacon.relative calling " + f2()

