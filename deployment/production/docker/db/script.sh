#!/usr/bin/env bash
while ! pg_isready
do
    echo "$(date) - waiting for database to start"
    sleep 10
done
