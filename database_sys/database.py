from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings.config import DATABASE

engine_db = DATABASE["ENGINE"]
name_db = DATABASE["NAME"]
user_db = DATABASE["USERNAME"]
pw_db = DATABASE["PASSWORD"]
host_db = DATABASE["HOST"]
port_db = DATABASE["PORT"]

# DATABASE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = f"{engine_db}://{user_db}:{pw_db}@{host_db}:{port_db}/{name_db}"
# DATABASE_URL = f"postgresql://postgres:carmello96@localhost:5432/formation_db"

engine = create_engine(
    DATABASE_URL # , connect_args={"check_same_thread": False} # .is needed only for SQLite. It's not needed for other databases.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()