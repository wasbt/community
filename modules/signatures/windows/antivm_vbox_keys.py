# Copyright (C) 2012,2016 Claudio "nex" Guarnieri (@botherder), Brad Spengler
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


class VBoxDetectKeys(Signature):
    name = "antivm_vbox_keys"
    description = "Detects VirtualBox through the presence of a registry key"
    severity = 3
    categories = ["anti-vm"]
    authors = ["nex", "Brad Spengler"]
    minimum = "0.5"
    ttps = ["T1012", "T1057", "T1497"]  # MITRE v6,7,8
    ttps += ["U1332"]  # Unprotect
    mbcs = ["OB0001", "B0009", "B0009.005", "OB0007"]
    mbcs += ["OC0008", "C0036", "C0036.005"]  # micro-behaviour

    def run(self):
        indicators = [
            r".*\\SOFTWARE\\(Wow6432Node\\)?Oracle\\VirtualBox\\ Guest\\ Additions$",
            r".*\\SOFTWARE\\(Wow6432Node\\)?Microsoft\\Windows\\CurrentVersion\\Uninstall\\Oracle\\ VM\\ VirtualBox\\ Guest\\ Additions$",
            r".*\\SYSTEM\\(CurrentControlSet|ControlSet001)\\Enum\\PCI\\VEN_80EE&DEV_BEEF&SUBSYS_00000000&REV_00$",
            r".*\\SYSTEM\\(CurrentControlSet|ControlSet001)\\Enum\\PCI\\VEN_80EE&DEV_CAFE&SUBSYS_00000000&REV_00$",
            r".*\\SYSTEM\\(CurrentControlSet|ControlSet001)\\Control\\VirtualDeviceDrivers$",
            r".*\\HARDWARE\\ACPI\\(DSDT|FADT|RSDT)\\VBOX__.*",
        ]
        for indicator in indicators:
            if self.check_key(pattern=indicator, regex=True):
                return True

        return False
