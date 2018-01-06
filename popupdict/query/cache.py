from collections import OrderedDict
from typing import Optional, Dict
import pickle
import os.path
import time

from .result import QueryResult
from popupdict.util import cache_dir, logger


# 缓存查询结果
# 不同查询客户端的缓存相互独立
# 使用内存做缓存，定期持久化到文件系统
# TODO 进程退出前自动持久化缓存
class QueryCache:
    # 单个客户端的最大缓存条目数
    MAX_COUNT = 1000
    # 将缓存持久化到硬盘的时间间隔，避免频繁写入硬盘。单位：秒
    PERSIST_INTERVAL = 60
    CACHE_FILE = os.path.join(cache_dir, 'query.cache')
    # 保存 QueryResult 的版本号，避免类结构变化
    CACHE_VERSION_FILE = os.path.join(cache_dir, 'query.cache-version')

    def __init__(self):
        self.clients = __class__.load_cache() or {}  # type: Dict[str, OrderedDict]
        self.last_persist_time = time.time()

    def get(self, client_id: str, query: str) -> Optional[QueryResult]:
        if client_id not in self.clients or query not in self.clients[client_id]:
            return
        self.clients[client_id].move_to_end(query)
        return self.clients[client_id][query]

    def put(self, client_id: str, query: str, query_result: QueryResult):
        if client_id not in self.clients:
            self.clients[client_id] = OrderedDict()
        self.clients[client_id][query] = query_result

        if len(self.clients[client_id]) > __class__.MAX_COUNT:
            self.clients[client_id].pop(False)

        if time.time() - self.last_persist_time > __class__.PERSIST_INTERVAL:
            self.persist()

    def persist(self):
        __class__.persist_cache(self.clients)
        self.last_persist_time = time.time()

    # 加载缓存
    @staticmethod
    def load_cache():
        if not os.path.exists(__class__.CACHE_VERSION_FILE) or not os.path.exists(__class__.CACHE_FILE):
            return
        # noinspection PyBroadException
        try:
            with open(__class__.CACHE_VERSION_FILE, 'r') as f:
                query_result_version = int(f.read().strip())
                if query_result_version != QueryResult.VERSION:
                    logger.debug('Ignore cache for old version %d, current version is %d',
                                 query_result_version, QueryResult.VERSION)
                    return
            with open(__class__.CACHE_FILE, 'rb') as f:
                data = pickle.load(f)
                return data
        except Exception:
            return

    # 将缓存持久化到文件系统
    @staticmethod
    def persist_cache(obj):
        with open(__class__.CACHE_FILE, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        with open(__class__.CACHE_VERSION_FILE, 'w') as f:
            f.write(str(QueryResult.VERSION))

    # 清空缓存
    @staticmethod
    def clear_cache():
        if os.path.exists(__class__.CACHE_FILE):
            os.remove(__class__.CACHE_FILE)
        if os.path.exists(__class__.CACHE_VERSION_FILE):
            os.remove(__class__.CACHE_VERSION_FILE)
