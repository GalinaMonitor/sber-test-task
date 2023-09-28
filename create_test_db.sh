#!/bin/bash

psql -U admin admin_db -c "CREATE DATABASE test_db OWNER admin"