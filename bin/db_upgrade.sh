#!/usr/bin/env bash

path=$1

if [ -z "$path" ]; then
    path=~/xraspberry.db
fi

alembic -c misc/db-migrations/alembic.ini -x dburl=$path upgrade head