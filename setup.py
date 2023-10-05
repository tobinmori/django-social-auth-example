#!/usr/bin/env python
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from collections import OrderedDict
from pkg_resources import resource_filename
from setuptools.command.install import install as _install
import shutil
import socket


class PyTest(TestCommand):
    user_options = [
        ('args=', None, "Pytest arguments to pass to py.test."),
        ('settings=', None, "Settings to use.")
    ]

    def initialize_options(self):
        self.args = 'hector/ --nomigrations -v --junit-xml=test-results/test_results.xml'
        self.settings = 'hector.settings.test'

    def finalize_options(self):
        self.test_suite = True
        self.test_args = []
        self.args = self.args.split()
        self.settings = "--ds={}".format(self.settings)
        self.args.append(self.settings)

    def run_tests(self):
        import pytest
        print(80 * '=')
        print('Running equivalent of: py.test {}'.format(' '.join(self.args)))
        print(80 * '=')
        errno = pytest.main(self.args)
        sys.exit(errno)

dependencies = (
'asgiref==3.3.4',
'certifi==2020.12.5',
'cffi==1.14.5',
'chardet==4.0.0',
'cryptography==3.4.7',
'defusedxml==0.7.1',
'Django==3.2',
'ecdsa==0.14.1',
'idna==2.10',
'oauthlib==3.1.0',
'pyasn1==0.4.8',
'pycparser==2.20',
'PyJWT==2.0.1',
'python-jose==3.2.0',
'python3-openid==3.2.0',
'pytz==2021.1',
'requests==2.25.1',
'requests-oauthlib==1.3.0',
'rsa==4.7.2',
'six==1.15.0',
'social-auth-app-django==4.0.0',
'social-auth-core==4.1.0',
'sqlparse==0.4.1',
'urllib3==1.26.4',
)

hostname = socket.gethostname()

files_to_copy_map = OrderedDict()
files_to_copy_map['qa-app'] = {
    'django.wsgi': '/home/pbsaccount/deployed/django.wsgi',
    'newrelic.ini': '/home/pbsaccount/newrelic.ini',
}
files_to_copy_map['staging-app'] = {
    'django.wsgi': '/home/pbsaccount/deployed/django.wsgi',
    'newrelic.ini': '/home/pbsaccount/newrelic.ini',
}
files_to_copy_map['prod-app'] = {
    'django.wsgi': '/home/pbsaccount/deployed/django.wsgi',
    'newrelic.ini': '/home/pbsaccount/newrelic.ini',
}

files_to_copy = {}

for map_key in files_to_copy_map.keys():
    if map_key in hostname:
        files_to_copy = files_to_copy_map[map_key]


class Install(_install):
    def run(self):
        _install.run(self)
        self.copy_files(files_to_copy)

    def copy_files(self, files_to_copy):
        for file_to_copy, destination in files_to_copy.items():
            source = resource_filename('required', file_to_copy)
            print('Copying %s to %s' % (file_to_copy, destination))
            try:
                shutil.copy2(source, destination)
            except OSError as e:
                print('ERROR: Can not copy file {} because {}.'.format(
                    file_to_copy, e))


setup(
    name='social_app',
    version='1.0.0',
    description='Demo Django Social Auth',
    author='Tobin Mori',
    author_email='ttmori@email.org',
    url='http://localhost:8000/',
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
    setup_requires=[],
    #cmdclass={'test': PyTest, 'install': Install},
    extras_require={
    #    'doc': ['Sphinx==1.2b1', 'sphinxcontrib-httpdomain==1.5.0']},
    },
    tests_require=[
    #    'soupsieve==1.9.5', 'pytest-django==3.4.8', 'selenium', 'mock==1.0.1',
    #    'xvfbwrapper==0.2.9', 'pytest==4.6.4', 'beautifulsoup4==4.8.1',
    #    'responses==0.7.0'
    ],
    zip_safe=False,
)