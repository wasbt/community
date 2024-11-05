import os

from maco.extractor import Extractor
from maco.model import ExtractorModel as MACOModel
from cape_parsers.CAPE.core.GuLoader import extract_config
from modules.parsers.utils import get_YARA_rule


def convert_to_MACO(raw_config: dict):
    if not raw_config:
        return None

    parsed_result = MACOModel(family="GuLoader", other=raw_config)

    for url in raw_config.get("URLs", []):
        parsed_result.http.append(MACOModel.Http(uri=url, usage="download"))

    return parsed_result


class GuLoader(Extractor):
    author = "kevoreilly"
    family = "GuLoader"
    last_modified = "2024-10-26"
    sharing = "TLP:CLEAR"
    yara_rule = get_YARA_rule("Guloader")

    def run(self, stream, matches):
        return convert_to_MACO(extract_config(stream.read()))
