"""
Module to integrate 3rd party extensions to our app.
"""
import os

from dotenv import load_dotenv
from flask_caching import Cache
from redis import Redis

load_dotenv()
# Initialize Redis connection
# Example Redis URL, change as needed
redis_url = os.getenv('REDIS_URL')
redis = Redis.from_url(redis_url)

# Initialize Flask-Caching with Redis as the cache backend
cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': redis_url,  # Use the same Redis URL
    # Set a default cache timeout (e.g., 5 minutes)
    'CACHE_DEFAULT_TIMEOUT': 300
})
