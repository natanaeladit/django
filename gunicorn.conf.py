import os

bind = "0.0.0.0:8000"
worker_class = "gthread"
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = int(os.environ.get("GUNICORN_THREADS", "4"))
preload_app = True
max_requests = 1000
max_requests_jitter = 100
timeout = 30
graceful_timeout = 30
keepalive = 5
worker_tmp_dir = "/dev/shm"
accesslog = "-"
errorlog = "-"
