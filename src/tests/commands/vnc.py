import unittest, shlex
import warnings
from tests.baseclass import *

from pykickstart.errors import *
from pykickstart.commands.vnc import *
#from pykickstart.base import *
#from pykickstart.options import *

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("vnc", "vnc\n")
        self.assert_parse("vnc --connect=HOSTNAME", "vnc --connect=HOSTNAME\n")
        self.assert_parse("vnc --connect=HOSTNAME:PORT", "vnc --connect=HOSTNAME:PORT\n")
        self.assert_parse("vnc --password=PASSWORD", "vnc --password=PASSWORD\n")
        self.assert_parse("vnc --connect=HOSTNAME --password=PASSWORD", "vnc --connect=HOSTNAME --password=PASSWORD\n")

        # fail
        self.assert_parse_error("vnc --connect")
        self.assert_parse_error("vnc --password")

class FC6_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("vnc", "vnc\n")
        self.assert_parse("vnc --host=HOSTNAME", "vnc --host=HOSTNAME\n")
        self.assert_parse("vnc --connect=HOSTNAME", "vnc --host=HOSTNAME\n")
        self.assert_parse("vnc --connect=HOSTNAME:PORT", "vnc --host=HOSTNAME --port=PORT\n")
        self.assert_parse("vnc --port=PORT", "vnc\n")
        self.assert_parse("vnc --password=PASSWORD", "vnc --password=PASSWORD\n")
        self.assert_parse("vnc --connect=HOSTNAME --password=PASSWORD", "vnc --host=HOSTNAME --password=PASSWORD\n")
        self.assert_parse("vnc --connect=HOSTNAME:PORT --password=PASSWORD", "vnc --host=HOSTNAME --port=PORT --password=PASSWORD\n")

        # Ensure --connect has been deprecated
        self.assert_deprecated("vnc", "connect")

        # fail
        self.assert_parse_error("vnc --connect")
        self.assert_parse_error("vnc --password")

class F9_TestCase(CommandTest):
    def runTest(self):
        # pass
        self.assert_parse("vnc", "vnc\n")
        self.assert_parse("vnc --host=SYSTEM", "vnc --host=SYSTEM\n")
        self.assert_parse("vnc --port=PORT", "vnc\n")
        self.assert_parse("vnc --password=PASSWORD", "vnc --password=PASSWORD\n")

        # Ensure --connect has been removed
        self.assert_removed("vnc", "connect")

        # Any --connect use should raise KickstartParseError
        self.assert_parse_error("vnc --host=HOSTNAME --connect=HOSTNAME --password=PASSWORD")
        self.assert_parse_error("vnc --host=HOSTNAME --connect=HOSTNAME --password=PASSWORD")
        self.assert_parse_error("vnc --connect=HOSTNAME --password=PASSWORD")
        self.assert_parse_error("vnc --connect=HOSTNAME")
        self.assert_parse_error("vnc --connect")
        self.assert_parse_error("vnc --password")

if __name__ == "__main__":
    unittest.main()
