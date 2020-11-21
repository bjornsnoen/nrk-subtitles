from multiprocessing import cpu_count

bind = "unix:/tmp/gunicorn.sock"
workers = cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
