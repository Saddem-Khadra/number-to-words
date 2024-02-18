from fastapi import Request
from logger import logger
import time
import socket


async def log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "process_time": process_time,
        "client_ip": request.client.host,
        "user_agent": request.headers.get("User-Agent", "Unknown"),
        "container_id": socket.gethostname()
    }
    logger.info(log_dict, extra=log_dict)
    return response
