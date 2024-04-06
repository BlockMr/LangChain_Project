from item.all_item import all_armor, all_gear, all_weapon
from db.db_models import Gears, Armors, Weapons, session, text


def add_gear(id, name, price, weight, description):
    gear = Gears(gear_id=id, name=name, price=price, weight=weight, description=description)
    session.add(gear)
    session.commit()
    session.close()


def add_all_gear():
    all_name = list(all_gear.keys())
    for id in range(len(all_name)):
        add_gear(
            id=id,
            name=all_name[id],
            price=all_gear[all_name[id]][0],
            weight=all_gear[all_name[id]][1],
            description=all_gear[all_name[id]][2]
        )


def add_armor(id, name, price, weight, armor_class, armor_type, strength, stealth, description):
    armor = Armors(
        armor_id=id,
        name=name,
        price=price,
        weight=weight,
        armor_class=armor_class,
        armor_type=armor_type,
        strength=strength,
        stealth=stealth,
        description=description
    )
    session.add(armor)
    session.commit()
    session.close()


def add_all_armor():
    all_name = list(all_armor.keys())
    for id in range(len(all_name)):
        add_armor(
            id=id,
            name=all_name[id],
            price=all_armor[all_name[id]][0],
            weight=all_armor[all_name[id]][1],
            armor_class=all_armor[all_name[id]][2],
            armor_type=all_armor[all_name[id]][3],
            strength=all_armor[all_name[id]][4],
            stealth=all_armor[all_name[id]][5],
            description=all_armor[all_name[id]][6]
        )


def add_weapon(id, name, price, weight, damage_type, damage, properties, description):
    weapon = Weapons(
        weapon_id=id,
        name=name,
        price=price,
        weight=weight,
        damage=damage,
        damage_type=damage_type,
        properties=properties,
        description=description
    )
    session.add(weapon)
    session.commit()
    session.close()


def add_all_weapon():
    all_name = list(all_weapon.keys())
    for id in range(len(all_name)):
        add_weapon(
            id=id,
            name=all_name[id],
            price=all_weapon[all_name[id]][0],
            weight=all_weapon[all_name[id]][1],
            damage=all_weapon[all_name[id]][2],
            damage_type=all_weapon[all_name[id]][3],
            properties=all_weapon[all_name[id]][4],
            description=all_weapon[all_name[id]][5]
        )


def get_all_weapons_name():
    with session as db:
        res = db.execute(text('SELECT name FROM weapons'))
    all_name = []
    for name in res:
        all_name.append(name[0])
    return all_name


def get_all_armors_name():
    with session as db:
        res = db.execute(text('SELECT name FROM armors'))
    all_name = []
    for name in res:
        all_name.append(name[0])
    return all_name


def get_all_gears_name():
    with session as db:
        res = db.execute(text('SELECT name FROM gears'))
    all_name = []
    for name in res:
        all_name.append(name[0])
    return all_name


def get_weapon(name):
    with session as db:
        res = db.execute(text('SELECT * FROM weapons WHERE name = :weapon_name'), {'weapon_name': name})
    all_inf = res.all()[0]
    return all_inf


def get_gear(name):
    with session as db:
        res = db.execute(text('SELECT * FROM gears WHERE name = :gear_name'), {'gear_name': name})
    all_inf = res.all()[0]
    return all_inf


def get_armor(name):
    with session as db:
        res = db.execute(text('SELECT * FROM armors where name = :armor_name'), {'armor_name': name})
    all_inf = res.all()[0]
    return all_inf
