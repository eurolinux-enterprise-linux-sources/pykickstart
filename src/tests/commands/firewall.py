#
# Martin Gracik <mgracik@redhat.com>
#
# Copyright 2009 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc.
#

import unittest
from tests.baseclass import *

class FC3_TestCase(CommandTest):
    def runTest(self):
        # pass
        # enable firewall
        self.assert_parse("firewall --enabled --trust=eth0 --ssh --port=imap:tcp",
                          "firewall --enabled --port=22:tcp,imap:tcp --trust=eth0\n")
        self.assert_parse("firewall --enable --trust=eth0,eth1 --ssh --telnet --http --smtp --ftp --port=1234:udp"
                          "firewall --enabled --port=22:tcp,23:tcp,80:tcp,443:tcp,25:tcp,21:tcp,1234:udp --trust=eth0,eth1\n")
        self.assert_parse("firewall --enabled --ssh --ftp", "firewall --enabled --port=22:tcp,21:tcp\n")
        self.assert_parse("firewall --enable --port=1234:udp,4321:tcp", "firewall --enabled --port=1234:udp,4321:tcp\n")

        # disable firewall
        self.assert_parse("firewall --disabled", "firewall --disabled\n")
        self.assert_parse("firewall --disable", "firewall --disabled\n")

        # enable by default
        self.assert_parse("firewall --trust=eth0", "firewall --enabled --trust=eth0\n")
        self.assert_parse("firewall", "firewall --enabled\n")

        # deprecated
        self.assert_deprecated("firewall", "--high")
        self.assert_deprecated("firewall", "--medium")

        # fail
        # unknown option
        self.assert_parse_error("firewall --bad-flag", KickstartParseError)
        # unexpected argument
        self.assert_parse_error("firewall arg", KickstartValueError)

class F9_TestCase(FC3_TestCase):
    def runTest(self):
        # run FC3 test case
        FC3_TestCase.runTest(self)

        # removed
        self.assert_removed("firewall", "--high")
        self.assert_removed("firewall", "--medium")

class F10_TestCase(F9_TestCase):
    def runTest(self):
        # pass
        # enable firewall
        self.assert_parse("firewall --enabled --trust=eth0 --ssh --port=imap:tcp",
                          "firewall --enabled --port=imap:tcp --trust=eth0 --service=ssh\n")
        self.assert_parse("firewall --enable --trust=eth0,eth1 --ssh --http --smtp --ftp --port=1234:udp"
                          "firewall --enabled --port=1234:udp --trust=eth0,eth1 --service=ssh,http,smtp,ftp\n")
        self.assert_parse("firewall --enabled --ssh --ftp", "firewall --enabled --service=ssh,ftp\n")
        self.assert_parse("firewall --enable --port=1234:udp,4321:tcp", "firewall --enabled --port=1234:udp,4321:tcp\n")

        # disable firewall
        self.assert_parse("firewall --disabled", "firewall --disabled\n")
        self.assert_parse("firewall --disable", "firewall --disabled\n")

        # enable by default
        self.assert_parse("firewall --trust=eth0", "firewall --enabled --trust=eth0\n")
        self.assert_parse("firewall", "firewall --enabled\n")

        # deprecated
        self.assert_deprecated("firewall", "--telnet")

        # fail
        # unknown option
        self.assert_parse_error("firewall --bad-flag", KickstartParseError)
        # unexpected argument
        self.assert_parse_error("firewall arg", KickstartValueError)

if __name__ == "__main__":
    unittest.main()
