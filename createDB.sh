#!/bin/sh
psql -U postgres -c 'DROP DATABASE IF EXISTS umbrella'
psql -U postgres -c 'CREATE DATABASE umbrella WITH TEMPLATE template0'
psql -U postgres -d 'umbrella' -f USchema.sql
psql -U postgres -d 'umbrella' -f UUsers.sql
psql -U postgres -d 'umbrella' -f UStations.sql
psql -U postgres -d 'umbrella' -f UUmbrellas.sql
psql -U postgres -d 'umbrella' -f ULoans.sql
psql -U postgres -d 'umbrella' -f UReports.sql