# Redis session management logic

import redis
from datetime import timedelta

class RedisSessionManager:
    def __init__(self):
        self.redis = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            decode_responses=True
        )
    
    def store_session(self, session_id: str, data: dict):
        self.redis.hset(session_id, mapping=data)
        self.redis.expire(session_id, timedelta(days=1))
    
    def get_session(self, session_id: str) -> dict:
        return self.redis.hgetall(session_id)