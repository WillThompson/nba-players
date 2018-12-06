# Contains the functionality to access the postgres db for the NBA players.

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import db_configuration

### Define the postgres db connection information. I have 
# DB_CONFIG_DICT = {
#         'user': <USERNAME>,
#         'password': <PASSWORD>,
#         'host': <HOST>,
#         'port': <PORT, usually 5432>,
#         'database' : nba_players
# }

DB_CONFIG_DICT = db_configuration.DB_CONFIG_DICT

###

DB_CONN_FORMAT = "postgresql://{user}:{password}@{host}:{port}/{database}"
DB_CONN_URI_DEFAULT = (DB_CONN_FORMAT.format(**DB_CONFIG_DICT))

# Create a function for a quick connection to the database
def db_connect():
    return create_engine(DB_CONN_URI_DEFAULT)