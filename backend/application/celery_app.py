from celery import Celery

celery = Celery("ppa_tasks")

def init_celery(app):
    celery.conf.broker_url = app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    celery.conf.result_backend = app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    celery.conf.timezone = 'Asia/Kolkata'

    # Force Redis RESP2 protocol for older Redis server compatibility
    celery.conf.broker_transport_options = {'protocol': 2}
    celery.conf.result_backend_transport_options = {'protocol': 2}

    celery.conf.beat_schedule = {
        'send-reminders-periodically': {
            'task': 'application.tasks.send_interview_reminders',
            'schedule': 20.0, # Run every 20 seconds for demonstration and verification logs
        },
        'generate-reports-periodically': {
            'task': 'application.tasks.generate_monthly_company_reports',
            'schedule': 60.0, # Run every 60 seconds for demonstration and verification logs
        }
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
