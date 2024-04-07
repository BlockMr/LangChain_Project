from db.db_models import Characters, Skills, Spells, Char_spells, AbilityStats, Gears, Char_items, Armors, Char_armors
from db.db_models import Weapons, Char_weapons, engine


Char_weapons.__table__.drop(engine)
Weapons.__table__.drop(engine)
Char_armors.__table__.drop(engine)
Armors.__table__.drop(engine)
Char_items.__table__.drop(engine)
Gears.__table__.drop(engine)
AbilityStats.__table__.drop(engine)
Char_spells.__table__.drop(engine)
Spells.__table__.drop(engine)
Skills.__table__.drop(engine)
Characters.__table__.drop(engine)
