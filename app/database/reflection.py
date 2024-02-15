"""Database Module to access pre-existing tables.
We're going to use the automap extension to automatically reflect database tables to SQLAlchemy 
models. However automap uses 'inspect' on the engine, and this isn't supported on async engines; 
we can work around this by doing the automapping using a synchronous engine. Once the models have 
been mapped they can be used by the async engine.
"""
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
import app.core.settings as settings


metadata = MetaData()
engine = create_engine(settings.db_url)

metadata.reflect(engine)
Base = automap_base(metadata=metadata)

# reflect the tables
Base.prepare(autoload_with=engine)

# mapped classes are now created with names by default
# matching that of the table name.
Order = Base.classes.order
User = Base.classes.customer
Item = Base.classes.orderProduct
