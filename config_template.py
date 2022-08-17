import os

DB_NAME = os.getenv('DB_NAME', 'avsoft')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'hostname')
DB_PORT = os.getenv('DB_PORT', 'port')
DB_CHARSET = 'utf8mb4'
DB_CONN_STRING = (f'mysql://{DB_USER}:{DB_PASSWORD}@'
                  f'{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}')

RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'password')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'hostname')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 'port')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'vhost')
RABBITMQ_CONN_STRING = (f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@'
                        f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}?connection_attempts=20&retry_delay=1')
PARSING_QUEUE = 'Parsing'
ERRORS_QUEUE = 'Errors'

CELERY_BROKER_URL = (f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@'
                     f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}')
CELERY_RESULT_BACKEND = (f'rpc://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@'
                         f'{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}')

SMTP_USE_SSL = True
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp')
SMTP_PORT = os.getenv('SMTP_PORT', 'port')
SMTP_HOST_USER = os.getenv('SMTP_HOST_USER', 'user')
SMTP_HOST_PASSWORD = os.getenv('SMTP_HOST_PASSWORD', 'password')
SMTP_RECEIVER = os.getenv('SMTP_RECEIVER', 'receiver')

INPUT_PATH = os.getenv('INPUT_PATH', 'data/')
OUTPUT_PATH = os.getenv('OUTPUT_PATH', 'output/')
# Record will be deleted from the database if the word met more than N_TIMES
N_TIMES = os.getenv('N_TIMES', 5)
