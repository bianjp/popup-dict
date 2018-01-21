from abc import ABC, abstractmethod
from typing import Optional

from popupdict.config import SpeechClientConfiguration


class AbstractSpeechClient(ABC):
    # 客户端 ID，需唯一，用于区分客户端（配置文件、缓存等）
    id = 'abstract'
    # 配置类
    config_class = SpeechClientConfiguration

    def __init__(self, config: SpeechClientConfiguration):
        config.validate()
        self.config = config

    @abstractmethod
    # save_path: 建议的发音文件保存路径
    # 返回发音路径
    def get(self, text: str, save_path: str) -> Optional[str]:
        pass
