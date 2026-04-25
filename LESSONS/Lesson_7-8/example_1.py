from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from dotenv import load_dotenv
import os

from sqlalchemy.orm.session import sessionmaker

load_dotenv()
db_url = os.getenv("CONNECTION_TO_MYSQL")
engine = create_engine(db_url + '/northwind')

metadata = MetaData()
metadata.reflect(bind=engine)
Base = automap_base(metadata=metadata)
Base.prepare()
