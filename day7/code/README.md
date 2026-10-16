# MySQL

## windows

- https://dev.mysql.com/downloads/installer/

## Linux - ubuntu

```bash
# installation
> sudo apt-get update
> sudo apt-get install mysql-server

# first time startup
> sudo mysql
```

## open mysql prompt

- open command prompt
- fire command
  - mysql -u root -p
  - enter password

## create the schema

```bash
# initialize the schema
> mysql -u root -p < schema.sql
```

## for python mysql connection

```bash
> pip install mysql-connector-python
```
