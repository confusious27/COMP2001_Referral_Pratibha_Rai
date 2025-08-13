# handles configuration (helps with OWASP; so anything sensitive is not hardcoded in)
import os
import urllib.parse
import pyodbc

import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve() # finds path of folder
connex_app = connexion.App(__name__, specification_dir=basedir) # creates connexion app
app = connex_app.app

class Config:
    DB_DRIVER = os.getenv("DB_DRIVER")
    DB_SERVER = os.getenv("DB_SERVER")
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    AUTH_API = os.getenv("AUTH_API")

    # build DB connection
    @classmethod
    def db_uri(cls):
        conn_str = (
            f"DRIVER={{{cls.DB_DRIVER}}};"
            f"SERVER={cls.DB_SERVER};"
            f"DATABASE={cls.DB_DATABASE};"
            f"UID={cls.DB_USERNAME};"
            f"PWD={cls.DB_PASSWORD};"
            "Encrypt=Yes;TrustServerCertificate=Yes;"
        )
        return "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(conn_str)

    # for the raw pyodbc connection
    @classmethod
    def pyodbc_conn_str(cls):
        return (
            f"DRIVER={{{cls.DB_DRIVER}}};"
            f"SERVER={cls.DB_SERVER};"
            f"DATABASE={cls.DB_DATABASE};"
            f"UID={cls.DB_USERNAME};"
            f"PWD={cls.DB_PASSWORD};"
            "Encrypt=Yes;TrustServerCertificate=Yes;"
        )

# calls on the procedures in sql
def call_proc(proc_name, params=()):
    conn_str = Config.pyodbc_conn_str()
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            if params:
                placeholders = ', '.join(['?'] * len(params))
                sql = f"EXEC {proc_name} {placeholders}"
                cursor.execute(sql, params)
            else:
                sql = f"EXEC {proc_name}"
                cursor.execute(sql)

            if cursor.description:  # SELECT
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                conn.commit()
                return {"message": "Procedure executed!"}
    except Exception as e:
        # Re-raise or return an error structure (can return a 4xx/5xx status code)
        raise

# same but with sql (this helps with read-only trail table)
def call_sql(query, params=()):
    conn_str = Config.pyodbc_conn_str()
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if cursor.description:
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                conn.commit()
                return {"message": "Query executed!"}
    except Exception:
        raise


app.config['SQLALCHEMY_DATABASE_URI'] = Config.db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)