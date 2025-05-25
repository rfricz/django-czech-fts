wsgi_app = "fts.wsgi"
bind = "unix:/run/gunicorn.sock"
preload_app = True
worker_tmp_dir = "/dev/shm"
