import time 
from functools import wraps

def timer_decorator(func):
    """装饰器，用于计算函数运行的时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 运行耗时: {end_time - start_time:.4f} 秒")
        return result
    return wrapper

