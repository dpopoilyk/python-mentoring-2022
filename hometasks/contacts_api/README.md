Environment variables:

    DATABASE_URL - <username>:<password>@<host>:<port>/<database_name>


To create database tables use initialize_db_tables.py script with `DATABASE_URL` env variable

To start an application fill environment variables and run: `uvicorn hometasks.contacts_api.main:app`
