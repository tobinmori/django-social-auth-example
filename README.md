
# Social Django Demo App

## About

This is a sample demo app that implements Akamai Identity Cloud using Social Django. Definitely, not for prod use, as it's running Django via 'runserver.'

- https://github.com/python-social-auth/social-app-django
- https://www.digitalocean.com/community/tutorials/django-authentication-with-facebook-instagram-and-linkedin


## Installation

1. cp ./docker/.env.example -> ./docker/.env and fill in the values of your AIC client
2. whitelist this redirect in your AIC login policy: http://localhost:8000/social-auth/complete/aic/
3. `docker-compose up`
4. if you'd like to log in and see the django admin console:
    `docker exec -it [container] /bin/bash` and `python manage.py createsuperuser` 
5. go to http://localhost:8000


## Custom Backend

A custom backend has been written to support AIC. See the codebase here: 

See core/backends/aic.py

