#!/usr/bin/env bash

path=$1

if [ -z "$path" ]; then
    path=~/xraspberry.db
fi

if [ -f "$path" ]; then
   echo "$path already exists! Removing"
   rm -f $path
fi

touch $path
echo "create db $path"

BIN_DIR=$(dirname $0)

echo "db upgrading"
sh $BIN_DIR/db_upgrade.sh