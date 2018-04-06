import re
from typing import Optional


# 过滤选中文本（删除两端的非字符内容、数字）
# 暂时只支持英文
class SelectionFilter:
    FILTER_PATTERN = re.compile("^[\W\d]*([a-zA-Z\s'-]+)[\W\d]*$", re.ASCII)
    WHITESPACE_PATTERN = re.compile('\s+')

    # 选中内容最大长度
    MAX_LENGTH = 80
    # 过滤后内容的最小长度
    MIN_LENGTH = 2

    @staticmethod
    def filter(text: str) -> Optional[str]:
        if not text or len(text) < __class__.MIN_LENGTH or len(text) > __class__.MAX_LENGTH:
            return None

        # Remove soft hyphen
        # https://en.wikipedia.org/wiki/Soft_hyphen
        text = text.replace('\xad', '')

        # 主要处理合成词，暂不考虑 word break，（至少 PC 端）较少遇到
        # https://en.oxforddictionaries.com/punctuation/hyphen
        text = text.replace('-\n', '-')

        match = __class__.FILTER_PATTERN.fullmatch(text)
        if match:
            text = match.group(1).strip()
        else:
            return None

        # 压缩空白字符（包括换行符），替换为一个空格
        text = __class__.WHITESPACE_PATTERN.sub(' ', text)
        if len(text) < __class__.MIN_LENGTH:
            return None

        return text
