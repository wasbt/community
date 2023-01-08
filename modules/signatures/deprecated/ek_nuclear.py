# Copyright (C) 2015 Will Metcalf william.metcalf@gmail.com
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


class Nuclear_JS(Signature):
    name = "nuclear_js"
    description = "Executes obfuscated JavaScript indicative of Nuclear Exploit Kit"
    weight = 3
    severity = 3
    categories = ["exploit_kit"]
    families = ["Nuclear"]
    authors = ["Will Metcalf"]
    minimum = "1.3"
    evented = True
    ttps = ["T1064"]  # MITRE v6
    ttps += ["T1059", "T1190", "T1203"]  # MITRE v6,7,8
    ttps += ["T1059.007"]  # MITRE v7,8
    mbcs = ["OB0008", "E1190", "OB0009", "E1059", "E1203"]

    filter_categories = set(["browser"])
    # backward compat
    filter_apinames = set(["JsEval", "COleScript_Compile", "COleScript_ParseScriptText"])

    def on_call(self, call, process):
        if call["api"] == "JsEval":
            buf = self.get_argument(call, "Javascript")
        else:
            buf = self.get_argument(call, "Script")

        if "window.runer = true;" in buf and "function flash_run(fu," in buf:
            if self.pid:
                self.mark_call()
            return True