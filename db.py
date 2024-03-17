from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

# todo add envs here 
URL_DB='postgresql://postgres:sin100=100@127.0.0.1:5432/quizes_fa'

engine = create_engine(URL_DB);

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()