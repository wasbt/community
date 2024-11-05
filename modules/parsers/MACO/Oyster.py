
from maco.extractor import Extractor
from maco.model import ExtractorModel as MACOModel
from cape_parsers.CAPE.core.Oyster import extract_config
from modules.parsers.utils import get_YARA_rule


def convert_to_MACO(raw_config: dict):
    if not raw_config:
        return None

    parsed_result = MACOModel(family="Oyster", other=raw_config)

    for address in raw_config.get("C2", []):
        parsed_result.http.append(MACOModel.Http(uri=address, usage="c2"))

    if "Dll Version" in raw_config:
        parsed_result.version = raw_config["Dll Version"]

    if "Strings" in raw_config:
        parsed_result.decoded_strings = raw_config["Strings"]

    return parsed_result


class Oyster(Extractor):
    author = "kevoreilly"
    family = "Oyster"
    last_modified = "2024-10-26"
    sharing = "TLP:CLEAR"
    yara_rule = get_YARA_rule(family)

    def run(self, stream, matches):
        return convert_to_MACO(extract_config(stream.read()))
