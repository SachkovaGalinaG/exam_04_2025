import os

SECRET_KEY = os.environ.get('8ygubzt*q(ksnghes-+cw^066@(6=m)dq*4@81a&v-^na-4se&')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '*' 
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'django_db'),
        'USER': os.environ.get('DB_USER', 'django'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'secret'),
        'HOST': os.environ.get('DB_HOST', 'mysql'),
        'PORT': '3306',
    }
}

#kubectl create secret generic django-secrets \--from-literal=SECRET_KEY='8ygubzt*q(ksnghes-+cw^066@(6=m)dq*4@81a&v-^na-4se&'




#kubectl create secret generic django-secrets \--from-literal=SECRET_KEY='8ygubzt*q(ksnghes-+cw^066@(6=m)dq*4@81a&v-^na-4se&' \--from-literal=DB_PASSWORD='secret'
