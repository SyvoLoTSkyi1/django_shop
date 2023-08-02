from shop import celery_app


@celery_app.task(bind=True, default_retry_delay=10)
def test_task(self, x, y, z=10):
    print('TEST BEFORE')
    try:
        x['key']
    except (KeyError, TypeError) as exc:
        raise self.retry(exc=exc, countdown=3)
    print('TEST AFTER')
    return x + y * z
