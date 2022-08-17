DB_NAME = 'avsoft'
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_CHARSET = 'utf8mb4'
DB_CONN_STRING = (f'mysql://{DB_USER}:{DB_PASSWORD}@'
                  f'{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}')

RABBITMQ_USER = 'admin'
RABBITMQ_PASSWORD = 'password'
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = '5672'
RABBITMQ_VHOST = 'vhost'
RABBITMQ_CONN_STRING = (f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@'
                        f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}?connection_attempts=20&retry_delay=1')
PARSING_QUEUE = 'Parsing'
ERRORS_QUEUE = 'Errors'

CELERY_BROKER_URL = (f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@'
                     f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}')
CELERY_RESULT_BACKEND = (f'rpc://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@'
                         f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}')
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

SMTP_USE_SSL = True
SMTP_HOST = 'smtp_server'
SMTP_PORT = 465
SMTP_HOST_USER = 'user'
SMTP_HOST_PASSWORD = 'password'
SMTP_RECEIVER = 'receiver'

INPUT_PATH = 'data/'
OUTPUT_PATH = 'output/'
# Record will be deleted from the database if the word met more than N_TIMES
N_TIMES = 5
