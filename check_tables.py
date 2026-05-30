from sqlalchemy import inspect
from app.db.database import engine

inspector = inspect(engine)

print("Tables found:")
print(inspector.get_table_names())