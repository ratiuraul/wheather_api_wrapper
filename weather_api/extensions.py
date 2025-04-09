from flask_caching import Cache
from redis import Redis


# Initialize Redis connection
# Example Redis URL, change as needed
redis = Redis.from_url("redis://localhost:6379/0")

# Initialize Flask-Caching with Redis as the cache backend
cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',  # Use the same Redis URL
    # Set a default cache timeout (e.g., 5 minutes)
    'CACHE_DEFAULT_TIMEOUT': 300
})
