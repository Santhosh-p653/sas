# PostgreSQL Setup Guide (Termux/Linux)

## Step 1: Update Packages
```bash
pkg update && pkg upgrade -y
pkg install postgresql -y
initdb $PREFIX/var/lib/postgresql
pg_ctl -D $PREFIX/var/lib/postgresql start
pg_ctl -D $PREFIX/var/lib/postgresql stop
psql -U $(whoami) -d $(whoami)
TO EXIT SHELL LATER:\q
