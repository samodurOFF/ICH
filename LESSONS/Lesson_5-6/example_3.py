import time

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from dotenv import load_dotenv
import os

from sqlalchemy.orm.session import sessionmaker

load_dotenv()
db_url = os.getenv("CONNECTION_TO_MYSQL")
engine = create_engine(db_url + '/sakila')

metadata = MetaData()
metadata.reflect(bind=engine)
Base = automap_base(metadata=metadata)
Base.prepare()

# Можно посмотреть информацию о таблицах в указанной базе данных
# print(metadata.tables)

# Теперь можно использовать классы, автоматически созданные из таблиц
Address = Base.classes.address
City = Base.classes.city
Session = sessionmaker(bind=engine)

with Session() as session:
    city = session.query(City).first()
    print(city.address)
    # address.phone = '123'
    # session.commit()

# time.sleep(10)
# session.add(address)
# address.phone = ''
# session.commit()  # новое подключение к базе данных
# session.close()
