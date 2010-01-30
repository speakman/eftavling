#!/bin/sh

python manage.py sqlall --settings=eftavling.local_settings $(python -c'from settings import INSTALLED_APPS; print " ".join(map(lambda x: x.split(".")[-1], INSTALLED_APPS))')
