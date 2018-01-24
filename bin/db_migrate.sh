#!/usr/bin/env bash

msg=$1
path=$2

if [ -z "$msg" ]; then
    echo "lack revision msg. Exiting..."
    exit 1
fi

if [ -z "$path" ]; then
    path=~/xraspberry.db
fi

alembic -c misc/db-migrations/alembic.ini -x dburl=$path revision -m "$msg"
