from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, create_engine

metadata = MetaData()
engine = create_engine("postgresql://app_user:changeme@127.0.0.1:5432/app_db")

metadata.reflect(engine, only=['order'])
Base = automap_base(metadata=metadata)

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
Order = Base.classes.order
