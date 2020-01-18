import unittest

from tests.baseclass import ParserTest

from pykickstart.constants import KS_SCRIPT_POST, KS_SCRIPT_PRE, KS_SCRIPT_PREINSTALL, KS_SCRIPT_TRACEBACK, KS_SCRIPT_ONERROR
from pykickstart.parser import Script
from pykickstart.version import DEVEL

class Script_Object_TestCase(ParserTest):
    def runTest(self):
        # The parser object will never be set up by this test, which means the
        # Script object will get the version number of whatever ran last.  That
        # could be totally wrong.  Thus, cause the parser to be created here
        # so the version will be right.
        self.get_parser()

        body = "import sys\nsys.exit(1)\n"
        obj = Script(body, type=KS_SCRIPT_PRE, interp="/usr/bin/python", logfile="/tmp/log", errorOnFail=True)
        self.assertEqual(obj.type, KS_SCRIPT_PRE)
        self.assertEqual(obj.interp, "/usr/bin/python")
        self.assertEqual(obj.logfile, "/tmp/log")
        self.assertTrue(obj.errorOnFail)

        self.assertEqual(str(obj), """
%pre --interpreter=/usr/bin/python --logfile=/tmp/log --erroronfail
import sys
sys.exit(1)
%end
""")

        obj = Script("ls /", type=KS_SCRIPT_POST, inChroot=False)
        self.assertEqual(obj.type, KS_SCRIPT_POST)
        self.assertFalse(obj.inChroot)

        self.assertEqual(str(obj), """
%post --nochroot
ls /
%end
""")

        obj = Script("ls /", type=KS_SCRIPT_PREINSTALL)
        self.assertEqual(obj.type, KS_SCRIPT_PREINSTALL)

        self.assertEqual(str(obj), """
%pre-install
ls /
%end
""")

        obj = Script("ls /", type=KS_SCRIPT_TRACEBACK)
        self.assertEqual(obj.type, KS_SCRIPT_TRACEBACK)

        self.assertEqual(str(obj), """
%traceback
ls /
%end
""")

        obj = Script("ls /", type=KS_SCRIPT_ONERROR)
        self.assertEqual(obj.type, KS_SCRIPT_ONERROR)

        self.assertEqual(str(obj), """
%onerror
ls /
%end
""")

if __name__ == "__main__":
    unittest.main()
