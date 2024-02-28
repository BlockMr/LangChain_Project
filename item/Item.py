from langchain_openai import ChatOpenAI


class Item:
    def __init__(self, name, price, weight, description: str = None):
        self.name = name
        self.price = price
        self.weight = weight
        self.description = description

    def __str__(self):
        attributes = [f"{name}={value}" for name, value in vars(self).items() if not name.startswith('__')]
        return f"{self.__class__.__name__}({', '.join(attributes)})"


all_gear = {
  "Backpack": ["2 gp", "5 lb.", "A backpack can hold up to 30 pounds of gear."],
  "Ball Bearings (bag of 1,000)": ["1 gp", "2 lb.", "As an action, you can spill these tiny metal balls from their"
                                                    " pouch to cover a level, square area that is 10 feet on a side."],
  "Barrel": ["2 gp", "70 lb.", "A barrel can hold 40 gallons of liquid or 4 cubic feet of solid material."],
  "Basket": ["4 sp", "2 lb.", "A basket can hold up to 40 pounds of gear."],
  "Bedroll": ["1 gp", "7 lb.", "A bedroll is a blanket and a simple mattress, useful for sleeping outdoors."],
  "Bell": ["1 gp", "", "A small bell, typically made of brass, that can be rung to produce a sound."],
  "Blanket": ["5 sp", "3 lb.", "A blanket is a thick piece of cloth used for warmth or as bedding."],
  "Block and Tackle": ["1 gp", "5 lb.", "A block and tackle is a pulley system used to lift heavy objects."],
  "Book": ["25 gp", "5 lb.", "A book is a written or printed work consisting of pages glued or sewn together along"
                             " one side and bound in covers."],
  "Bottle, Glass": ["2 gp", "2 lb.", "A glass bottle with a cork stopper, typically used for holding liquids."],
  "Bucket": ["5 cp", "2 lb.", "A bucket can hold up to 3 gallons of liquid."],
  "Caltrops (bag of 20)": ["1 gp", "2 lb.", "As an action, you can spread a bag of caltrops to cover a square area that"
                                            " is 5 feet on a side."],
  "Candle": ["1 cp", "", "A candle provides dim light in a 5-foot radius."],
  "Case, Crossbow Bolt": ["1 gp", "1 lb.", "A case can hold up to 20 bolts for a crossbow."],
  "Case, Map or Scroll": ["1 gp", "1 lb.", "A case can hold up to 10 rolled-up maps or scrolls."],
  "Chain (10 feet)": ["5 gp", "10 lb.", "A chain has a length of 10 feet and can be used for various purposes."],
  "Chalk (1 piece)": ["1 cp", "", "A piece of chalk that can be used to write on surfaces."],
  "Chest": ["5 gp", "25 lb.", "A chest is a large box typically used for storing valuables."],
  "Climber's Kit": ["25 gp", "12 lb.", "A climber's kit includes special pitons, boot tips, gloves, and a harness."],
  "Clothes, Costume": ["5 gp", "4 lb.", "A costume is a set of clothing and accessories designed to represent a"
                                        " particular character or theme."],
  "Clothes, Fine": ["15 gp", "6 lb.", "Fine clothes are elegant and stylish garments made from quality materials."],
  "Clothes, Traveler's": ["2 gp", "4 lb.", "Traveler's clothes are simple garments suitable for long journeys."],
  "Component Pouch": ["25 gp", "2 lb.", "A component pouch is a small, watertight leather belt pouch that contains the"
                                        " materials you need to cast spells."],
  "Crowbar": ["2 gp", "5 lb.", "A crowbar is a metal bar with a flattened end, often used for prying things open."],
  "Fishing Tackle": ["1 gp", "4 lb.", "Fishing tackle includes a rod, reel, line, hooks, and bait for catching fish."],
  "Flask or Tankard": ["2 cp", "1 lb.", "A metal container for holding liquids."],
  "Flute": ["2 gp", "1 lb.", "A musical instrument that produces sound by blowing air through a series of holes."],
  "Grappling Hook": ["2 gp", "4 lb.", "A grappling hook is a metal hook with multiple prongs, attached to a rope."],
  "Hammer": ["1 gp", "3 lb.", "A hammer is a simple tool with a heavy head, used for driving nails or breaking things."],
  "Healer's Kit": ["5 gp", "3 lb.", "A healer's kit includes bandages, salves, and other supplies used"
                                    " for treating wounds."],
  "Holy Water (flask)": ["25 gp", "1 lb.", "Holy water is water that has been blessed by a cleric or other"
                                           " religious figure."],
  "Hourglass": ["25 gp", "1 lb.", "An hourglass is a device used to measure time, consisting of two glass bulbs"
                                  " connected by a narrow neck."],
  "Hunting Trap": ["5 gp", "25 lb.", "A hunting trap is a mechanical device used to catch animals."],
  "Ink (1 ounce bottle)": ["10 gp", "", "A bottle of ink used for writing or drawing."],
  "Ink Pen": ["2 cp", "", "A simple pen used for writing."],
  "Jug or Pitcher": ["2 cp", "4 lb.", "A container for holding liquids."],
  "Ladder (10-foot)": ["1 sp", "25 lb.", "A ladder has a length of 10 feet and can be used for climbing."],
  "Lamp": ["5 sp", "1 lb.", "A lamp provides bright light in a 15-foot radius."],
  "Lantern, Bullseye": ["10 gp", "2 lb.", "A bullseye lantern provides a narrow beam of light."],
  "Lantern, Hooded": ["5 gp", "2 lb.", "A hooded lantern provides a bright light in a 30-foot radius."],
  "Lock": ["10 gp", "1 lb.", "A lock is a mechanical device used to secure doors, chests, and other objects."],
  "Magnifying Glass": ["100 gp", "", "A magnifying glass is a handheld lens used to make objects appear larger."],
  "Manacles": ["2 gp", "6 lb.", "A pair of manacles can be used to restrain a prisoner."],
  "Mess Kit": ["2 sp", "1 lb.", "A mess kit includes a plate, cup, utensils, and a cooking pot."],
  "Mirror, Steel": ["5 gp", "1/2 lb.", "A steel mirror provides a clear reflection."],
  "Oil (flask)": ["1 sp", "1 lb.", "A flask of oil that can be used to create a slick surface or fuel a lantern."],
  "Paper (one sheet)": ["2 sp", "", "A single sheet of paper for writing or drawing."],
  "Parchment (one sheet)": ["1 gp", "", "A single sheet of parchment made from animal skin."],
  "Perfume (vial)": ["5 gp", "", "A small vial of scented oil used for personal grooming."],
  "Pick, Miner's": ["2 gp", "10 lb.", "A miner's pick is a sturdy tool with a sharp, pointed end,"
                                      " used for breaking rocks."],
  "Piton": ["5 cp", "1/4 lb.", "A metal spike with an eye at one end, used for securing ropes and climbing gear."],
  "Poison, Basic (vial)": ["100 gp", "", "A vial of basic poison that can be applied to a weapon or food."],
  "Pole (10-foot)": ["5 cp", "7 lb.", "A pole has a length of 10 feet and can be used for various purposes."],
  "Pot, Iron": ["2 gp", "10 lb.", "An iron pot used for cooking food."],
  "Potion of Healing": ["50 gp", "1/2 lb.", "A potion that restores hit points when consumed."],
  "Pouch": ["5 sp", "1 lb.", "A pouch can hold up to 1/5 cubic foot or 6 pounds of gear."],
  "Quiver": ["1 gp", "1 lb.", "A quiver can hold up to 20 arrows or bolts."],
  "Ram, Portable": ["4 gp", "35 lb.", "A portable ram is a sturdy pole with a metal head,"
                                      " used for breaking down doors."],
  "Rations (1 day)": ["5 sp", "2 lb.", "A day's worth of rations for one person."],
  "Robes": ["1 gp", "4 lb.", "A simple garment worn for ceremonial or formal occasions."],
  "Rope, Hempen (50 feet)": ["1 gp", "10 lb.", "A length of durable hemp rope that is 50 feet long."],
  "Rope, Silk (50 feet)": ["10 gp", "5 lb.", "A length of resilient silk rope that is 50 feet long."],
  "Sack": ["1 cp", "1/2 lb.", "A sack can hold up to 1 cubic foot or 30 pounds of gear."],
  "Scale, Merchant's": ["5 gp", "3 lb.", "A scale used for weighing goods and determining their value."],
  "Sealing Wax": ["5 sp", "", "A stick of wax used to seal letters or documents."],
  "Shovel": ["2 gp", "5 lb.", "A shovel is a tool with a broad, flat blade, used for digging."],
  "Signal Whistle": ["5 cp", "", "A small whistle used to produce a loud, piercing sound."],
  "Signet Ring": ["5 gp", "", "A ring bearing a unique symbol or design used to mark documents or personal property."],
  "Soap": ["2 cp", "", "A bar of soap used for personal hygiene."],
  "Spellbook": ["50 gp", "3 lb.", "A spellbook is a leather-bound book used by wizards to record"
                                  " spells and magical research."],
  "Spikes, Iron (10)": ["1 gp", "5 lb.", "A set of iron spikes that can be used to secure ropes or create obstacles."],
  "Spyglass": ["1,000 gp", "1 lb.", "A spyglass is a handheld telescope used for viewing distant objects."],
  "Tent, Two-Person": ["2 gp", "20 lb.", "A simple tent designed to accommodate two people."],
  "Tinderbox": ["5 sp", "1 lb.", "A tinderbox contains flint, steel, and tinder for starting fires."],
  "Torch": ["1 cp", "1 lb.", "A torch provides bright light in a 20-foot radius."],
  "Vial": ["1 gp", "", "A small glass container used for holding liquids or powders."],
  "Waterskin": ["2 sp", "5 lb.", "A waterskin can hold up to 4 pints of liquid."],
  "Whetstone": ["1 cp", "1 lb.", "A whetstone is a rough stone used for sharpening blades."],
  "Wooden Staff": ["5 cp", "4 lb.", "A simple wooden staff that can be used as a weapon or walking aid."],
  "Yew Wand": ["10 gp", "", "A wand made from yew wood, used by spellcasters to channel magical energies."]
}
