#!/bin/sh
psql -U postgres -c 'DROP DATABASE IF EXISTS umbrellasharing'
psql -U postgres -c 'CREATE DATABASE umbrellasharing WITH TEMPLATE template0'
psql -U postgres -d 'umbrellasharing' -f USchema.sql
psql -U postgres -d 'umbrellasharing' -f UUsers.sql
psql -U postgres -d 'umbrellasharing' -f UStations.sql
psql -U postgres -d 'umbrellasharing' -f UUmbrellas.sql
psql -U postgres -d 'umbrellasharing' -f ULoans.sql
psql -U postgres -d 'umbrellasharing' -f UReports.sql