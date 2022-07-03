#Name: Tioluwani Ajani
#AndrewID: tajani
#Section: C0

from functions_and_classes import *
# All objects (fighters, weapons, magic and items) are declared here
 
# dificulty texts
veryEasyText = "Very Easy:\nVictory guaranteed.\n"
veryEasyText += "Radagast doesn't even know magic.\nGo easy on him."
easyText = "Easy:\nStill fairly simple.\nBeginners start here.\n"
easyText += "Pollando shall serve as your\npunching bag"
normalText = "Normal:\nChoose this difficulty\nfor a balanced experience.\n"
normalText += "Gwydion shall be your opponent."
hardText = "Hard:\nNow it gets interesting\nBe careful!"
hardText += "\nYou shall face Avogorim.\n"
veryHardText = "Impossible:\nYou will lose.\nThe Reaper conquers all.\n"

# Weapons
rustySword = Weapon("Rusty Sword", 45, 8)
bluntAxe = Weapon("Blunt Axe", 60, 8)
longBow = Weapon("Long Bow", 85, 7)
bludgeon = Weapon("Bludgeon", 85, 8)
warHammer = Weapon("War Hammer", 80, 8)
club = Weapon("War Club", 80, 6)
axe = Weapon("Gilded Axe", 70, 7)
warScythe = Weapon("War Scythe", 70, 7)
arbalest = Weapon("Crossbow", 50, 9)
morningStar = Weapon("Morning Star", 70, 10)
glaive = Weapon("Glaive", 50, 10)
flamingLongSword = Weapon("Flaming Long Sword", 140, 3)

# Spells
fireSpell = OSpell("Fiery Bolt", 110, 150)
magmaRay = OSpell("Magma Ray", 100, 140)
healingSpell = DSpell("Divine Recovery", -90, 175)
raiseShield = Chant("Orb of Protection", "defence", 0.12, 100)
poisonCurse = Curse("Curse of Venom", "poisoned", 40, 130)
thunderBolt = OSpell("Arcane Thunderbolt", 90, 105)
nauseaCurse = Curse("Surge of Nausea", "poisoned", 40, 120)

# Items
p1antidote = Item("Antidote", "poisoned", None, 1)
p1potion = Item("Potion", "HP", 110, 2)
p1elixir = Item("Elixir", "XP", 100, 2)

normalPotion = Item("Potion", "HP", 90, 2)
normalElixir = Item("Elixir", "XP", 95, 2)

hardAntidote = Item("Antidote", "poisoned", None, 1)
hardPotion = Item("Potion", "HP", 90, 2)
hardElixir = Item("Elixir", "XP", 95, 2)

veryHardAntidote = Item("Antidote", "poisoned", None, 3)
veryHardPotion = Item("Potion", "HP", 100, 2)
veryHardElixir = Item("Elixir", "XP", 110, 2)

# Fighters
# You are p1
p1 = Fighter("Player 1", 500, 500, 500, 500, 0.2, [])
p1.weapons = [warScythe, arbalest, flamingLongSword]
p1.spells = [fireSpell, healingSpell, raiseShield, poisonCurse]
p1.items = [p1antidote, p1potion, p1elixir]

# Very Easy AI
veryEasy = Fighter("Radagast", 400, 400, 100, 100, 0.1, [])
veryEasy.weapons = [rustySword, bluntAxe]
veryEasy.spells = []
veryEasy.items = []

# Easy AI
easy = Fighter("Pallando", 400, 400, 500, 500, 0.15, [])
easy.weapons = [bluntAxe, longBow]
easy.spells = [thunderBolt]
easy.items = []

# Normal AI
normal = Fighter("Gwydion", 550, 550, 500, 500, 0.2, [])
normal.weapons = [warHammer, bludgeon]
normal.spells = [thunderBolt, nauseaCurse]
normal.items =[normalPotion, normalElixir]

# Hard AI
hard = Fighter("Avogorim", 600, 600, 500, 500, 0.2, [])
hard.weapons = [axe, club]
hard.spells = [magmaRay]
hard.items = [hardPotion, hardElixir, hardAntidote]

# Very Hard AI
veryHard = Fighter("The Reaper",600, 600, 500, 500, 0.2, [])
veryHard.weapons = [morningStar, glaive]
veryHard.spells = [poisonCurse, fireSpell, healingSpell]
veryHard.items = [veryHardAntidote, veryHardPotion, veryHardElixir]