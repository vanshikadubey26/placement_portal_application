import redis
import json


r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, protocol=2)

def get_cache(key):
    try:
        data = r.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"Redis get_cache error: {e}")
    return None

def set_cache(key, value, timeout=300):
    try:
        r.setex(key, timeout, json.dumps(value))
        return True
    except Exception as e:
        print(f"Redis set_cache error: {e}")
    return False

def delete_cache(key):
    try:
        r.delete(key)
        return True
    except Exception as e:
        print(f"Redis delete_cache error: {e}")
    return False
