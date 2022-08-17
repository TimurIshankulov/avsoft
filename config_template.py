import os

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_CHARSET = 'utf8mb4'
DB_CONN_STRING = (f'mysql://{DB_USER}:{DB_PASSWORD}@'
                  f'{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}')

RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = os.environ['RABBITMQ_PORT']
RABBITMQ_VHOST = os.environ['RABBITMQ_VHOST']
RABBITMQ_CONN_STRING = (f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@'
                        f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}?connection_attempts=20&retry_delay=1')
PARSING_QUEUE = 'Parsing'
ERRORS_QUEUE = 'Errors'

CELERY_BROKER_URL = (f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@'
                     f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}')
CELERY_RESULT_BACKEND = (f'rpc://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@'
                         f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}')

SMTP_USE_SSL = True
SMTP_HOST = os.environ['SMTP_HOST']
SMTP_PORT = os.environ['SMTP_PORT']
SMTP_HOST_USER = os.environ['SMTP_HOST_USER']
SMTP_HOST_PASSWORD = os.environ['SMTP_HOST_PASSWORD']
SMTP_RECEIVER = os.environ['SMTP_RECEIVER']

INPUT_PATH = os.environ['INPUT_PATH']
OUTPUT_PATH = os.environ['OUTPUT_PATH']
# Record will be deleted from the database if the word met more than N_TIMES
N_TIMES = os.environ['N_TIMES']
