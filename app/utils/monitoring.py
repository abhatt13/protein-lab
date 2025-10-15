import time
from functools import wraps
from typing import Callable
from app.core.logging_config import logger

class PerformanceMonitor:
    @staticmethod
    def track_time(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            execution_time = end_time - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")

            return result
        return wrapper

    @staticmethod
    def log_error(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
                raise
        return wrapper

class MetricsCollector:
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_proteins": 0,
            "total_users": 0
        }

    def increment_request(self, success: bool = True):
        self.metrics["total_requests"] += 1
        if success:
            self.metrics["successful_requests"] += 1
        else:
            self.metrics["failed_requests"] += 1

    def get_metrics(self):
        return self.metrics

metrics_collector = MetricsCollector()
