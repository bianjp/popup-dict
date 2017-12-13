import re
from typing import Optional


# 过滤选中文本（删除两端的非字符内容、数字）
# 暂时只支持英文
class SelectionFilter:
    FILTER_PATTERN = re.compile('^[\W\d]*([a-zA-Z\s-]+)[\W\d]*$', re.ASCII)
    WHITESPACE_PATTERN = re.compile('\s+')

    @staticmethod
    def filter(text: str) -> Optional[str]:
        if not text or len(text) == 0 or len(text) > 80:
            return None

        match = __class__.FILTER_PATTERN.fullmatch(text)
        if match:
            text = match.group(1)
        else:
            return None

        # 压缩空白字符（包括换行符），替换为一个空格
        text = __class__.WHITESPACE_PATTERN.sub(' ', text)
        if len(text) == 0:
            return None

        return text
