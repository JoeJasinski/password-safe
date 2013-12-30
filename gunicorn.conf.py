import multiprocessing

pidfile = "/Users/jjasinski/Sites/filesafe/proj/psafe/var/run/gunicorn.pid"
bind = "unix:/Users/jjasinski/Sites/filesafe/proj/psafe/var/run/skokielibrary-django.socket"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 60


#def def_pre_fork(server, worker):
#    import psycogreen.gevent
#    psycogreen.gevent.patch_psycopg()
#    worker.log.info("Made Psycopg Green")
#
#pre_fork = def_pre_fork

