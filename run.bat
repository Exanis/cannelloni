@echo off

CALL env\Scripts\activate
CALL python manage.py workflow %1 %2 %3
CALL env\Scripts\deactivate
