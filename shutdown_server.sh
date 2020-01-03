#!/usr/bin/env bash
ps -ef | grep java | grep Tika | grep -v grep | awk '{print $2}' | xargs kill
echo 'Tika Rest Server successfully stopped.'
ps -ef | grep python  | grep runserver | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep python  | grep runserver | grep -v grep | awk '{print $2}' | xargs kill
echo 'Django Runserver successfully stopped.'
ps -ef | grep python  | grep scrapyd | grep -v grep | awk '{print $2}' | xargs kill
echo 'Scrapyd successfully stopped.'

