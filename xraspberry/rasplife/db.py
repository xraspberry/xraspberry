# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from xraspberry import config

dsn_url = URL(drivername='postgresql',
              host=config.get_config("rasplife.postgresql.host"),
              port=config.get_config("rasplife.postgresql.port"),
              username=config.get_config("rasplife.postgresql.user"),
              password=config.get_config("rasplife.postgresql.password"),
              database=config.get_config("rasplife.postgresql.db_name"))

engine = create_engine(dsn_url, echo=config.get_config("rasplife.sqlalchemy.echo", False))
DBSession = sessionmaker(engine)  # pylint: disable=invalid-name
db_session = DBSession()

BaseModel = declarative_base()  # pylint: disable=invalid-name
