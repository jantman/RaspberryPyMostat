"""
The latest version of this package is available at:
<http://github.com/jantman/RPyMostat>

##################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of RPyMostat, also known as RPyMostat.

    RPyMostat is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RPyMostat is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with RPyMostat.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
##################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/RPyMostat> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
##################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
##################################################################################
"""

import sys
from klein import Klein
from rpymostat.engine.api.v1 import APIv1

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import patch, call, Mock, DEFAULT  # noqa
else:
    from unittest.mock import patch, call, Mock, DEFAULT  # noqa

pbm = 'rpymostat.engine.api.v1'
pb = '%s.APIv1' % pbm


class TestClass(APIv1):

    def __init__(self, apiserver, app, dbconn, prefix):
        pass


class TestAPIv1(object):

    def setup(self):
        self.app = Mock(spec=Klein)
        self.prefix = ['my', 'parent']
        self.apiserver = Mock()
        self.dbconn = Mock()
        self.cls = TestClass(self.apiserver, self.app, self.dbconn, self.prefix)
        self.cls.app = self.app
        self.cls.prefix = self.prefix
        self.cls.dbconn = self.dbconn
        self.cls.apiserver = self.apiserver

    def test_class(self):
        with patch.multiple(
            pbm,
            autospec=True,
            Sensors=DEFAULT,
            Status=DEFAULT
        ) as mocks:
            self.cls.setup_routes()
        assert mocks['Sensors'].mock_calls == [
            call(self.cls, self.app, self.dbconn, self.prefix),
            call().setup_routes()
        ]
        assert mocks['Status'].mock_calls == [
            call(self.cls, self.app, self.dbconn, self.prefix),
            call().setup_routes()
        ]
