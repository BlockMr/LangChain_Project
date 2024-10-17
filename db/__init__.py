from db_methods import add_all_armor, add_all_spell, add_all_gear, add_all_weapon
from db_models import Base, engine

Base.metadata.create_all(bind=engine)
add_all_spell()
add_all_weapon()
add_all_gear()
add_all_armor()
