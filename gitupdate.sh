#!/bin/bash

cd /config

git add .
git commit -m "$1"
git push origin master

