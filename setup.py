# setup.py

from setuptools import setup, find_packages

setup(
    name='chat_app',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SocketIO',
        'redis',
        'cryptography',
        'authlib',
        'eventlet',
    ],
    entry_points={
        'console_scripts': [
            'chat_app=main:main',
        ],
    },
    author='Your Name',
    author_email='youremail@example.com',
    description='A secure, real-time chat application with E2EE',
    url='https://github.com/yourusername/chat_app',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)