import unittest, shlex
import warnings
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.authconfig import *
#from pykickstart.base import *
#from pykickstart.options import *

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("authconfig")
        self.assert_parse("authconfig --cheese", "auth --cheese\n")
        self.assert_parse("authconfig --cracker=CRUNCHY", "auth --cracker=CRUNCHY\n")
        self.assert_parse("auth")
        self.assert_parse("auth --cheese", "auth --cheese\n")
        self.assert_parse("auth --cracker=CRUNCHY", "auth --cracker=CRUNCHY\n")

if __name__ == "__main__":
    unittest.main()
