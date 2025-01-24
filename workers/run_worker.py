from workers import celery

if __name__ == "__main__":
    celery.worker_main(argv=["worker", "--loglevel=info", "--pool=solo"])
