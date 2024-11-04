
from maco.extractor import Extractor
from maco.model import ExtractorModel as MACOModel
from cape_parsers.CAPE.community.XenoRAT import extract_config
from modules.parsers.utils import get_YARA_rule


def convert_to_MACO(raw_config: dict):
    if not raw_config:
        return None

    parsed_result = MACOModel(family="XenoRAT", other=raw_config)

    return parsed_result


class XenoRAT(Extractor):
    author = "kevoreilly"
    family = "XenoRAT"
    last_modified = "2024-10-26"
    sharing = "TLP:CLEAR"
    yara_rule = get_YARA_rule(family)

    def run(self, stream, matches):
        return convert_to_MACO(extract_config(stream.read()))
