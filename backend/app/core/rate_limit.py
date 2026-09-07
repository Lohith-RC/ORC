from fastapi import Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

def get_client_ip(request: Request) -> str:
    """
    Resolves client IP behind reverse proxies (Cloudflare, Render, AWS ALB).
    Falls back to direct connection IP.
    """
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip.strip()
    
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
        
    return request.client.host if request.client else "127.0.0.1"

limiter = Limiter(key_func=get_client_ip)
rate_limit_handler = _rate_limit_exceeded_handler
