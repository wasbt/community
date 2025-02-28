# Copyright (C) 2015 Kevin Ross
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature


class OfficeSecurity(Signature):
    name = "office_security"
    description = "Attempts to modify Microsoft Office security settings"
    severity = 3
    categories = ["office"]
    authors = ["Kevin Ross"]
    minimum = "1.2"
    ttps = ["T1089"]  # MITRE v6
    ttps += ["T1112"]  # MITRE v6,7,8
    ttps += ["T1562"]  # MITRE v7,8
    mbcs = ["OB0006", "E1112", "F0004"]
    mbcs += ["OC0008", "C0036"]  # micro-behaviour

    def run(self):
        office_pkgs = ["ppt", "doc", "xls", "eml"]
        if any(e in self.results["info"]["package"] for e in office_pkgs):
            return False

        reg_indicators = (
            r".*\\SOFTWARE\\(Wow6432Node\\)?Microsoft\\Office\\.*\\Security\\.*",
            r".*\\SOFTWARE\\(Wow6432Node\\)?Policies\\Microsoft\\Office\\.*\\Security\\.*",
        )

        for indicator in reg_indicators:
            if self.check_write_key(pattern=indicator, regex=True):
                return True

        return False
