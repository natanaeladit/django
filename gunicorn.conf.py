"""Gunicorn configuration. Size per deployment with WEB_CONCURRENCY and GUNICORN_THREADS."""

import os

bind = "0.0.0.0:8000"  # all interfaces: the container network is the boundary
worker_class = "gthread"
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = int(os.environ.get("GUNICORN_THREADS", "4"))
preload_app = True  # import once, then fork: workers share memory pages
max_requests = 1000  # recycle workers to cap slow memory growth
max_requests_jitter = 100
timeout = 30
graceful_timeout = 30
keepalive = 5  # raise above the load balancer's idle timeout when behind one
worker_tmp_dir = "/dev/shm"  # noqa: S108 - heartbeat on tmpfs, immune to slow disks
accesslog = "-"
errorlog = "-"
