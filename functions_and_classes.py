#Name: Tioluwani Ajani
#AndrewID: tajani
#Section: C0
 
import random

# Fighter object. Two opposing objects in every fight. P1 vs. P2
class Fighter(object):
    def __init__(self, name, hp, maxHP, xp, maxXP, defence, status):
        self.name = name
        self.hp = hp
        self.maxHP = maxHP
        self.xp = xp
        self.maxXP = maxXP
        self.defence = defence
        self.startDefence = defence
        self.status = status
        self.weapons = []
        self.spells = []
        self.items = []

    # returns fighter to original state
    def reset(self):
        self.hp = self.maxHP
        self.xp = self.maxXP
        self.defence = self.startDefence
        self.status = []
        for item in self.items:
            item.count = item.stock

    # Fighter Methods:
    # returns outcome of using a given weapon
    def useWeapon(self, target, weapon):
        result = ""
        if not attackHit(weapon.accuracy):
            result += f"{self.name} missed!"
            return result, True
        else:
            result += f"{self.name} hit!\n"
            if isCrit():
                crit = True
                result += f"Critical Damage!\n"
            else:
                crit = False
            # damage calculation
            damage = round(weapon.attack * (1 - target.defence), 2)
            # vary within range of damage - 5 to damage
            damage = random.randint(int(damage - 5), int(damage))
            # double if critical hit
            if crit == True: damage *= 2
            target.hp -= damage
            result += f"{self.name} dealt {damage} damage!"
            return result, True

    # returns outcome of using a given attack spell
    def offenceSpell(self, target, spell):
        result = ""
        # fails if insufficient XP
        if spell.xpCost > self.xp:
            result += f"The spell failed!\n{self.name} doesn't have enough XP!"
            return result, False
        else:
            # damage calculation
            damage = spell.damage
            damage = random.randint(damage - 15, damage + 15)
            target.hp -= damage
            self.xp -= spell.xpCost
            result += f"{self.name} dealt {damage} damage" 
            result += f" and spent {spell.xpCost}XP!"
            return result, True

    #returns outcome of using a given defence spell
    def defenceSpell(self, target, spell):
        result = ""
        # fails if insufficient XP
        if spell.xpCost > self.xp:
            result += f"The spell failed!\n{self.name} doesn't have enough XP!"
            return result, False
        else:
            recovered = spell.damage
            if target.hp < 500:
                target.hp -= spell.damage
                if target.hp > 500: 
                    recovered = -spell.damage - abs(target.hp - 500)
                    target.hp = 500
                self.xp -= spell.xpCost
                result += f"{self.name} recovered {abs(recovered)}HP" 
                result += f" and spent {spell.xpCost}XP!"
                return result, True
            else:
                result += f"The spell had no effect!"
                return result, False
    
    # returns outcome of using a given chant
    def useChant(self, target, chant):
        result = ""
        if chant.xpCost > self.xp:
            result += f"The chant couldn't be completed!\n"
            result += f"{self.name} doesn't have enough XP!"
            return result, False
        else:
            if target.defence >= 0.7:
                result += f"The chant's effect is already maxed!"
                return result, False
            else:
                target.defence = round(target.defence + chant.modVal, 2)
                self.xp -= chant.xpCost
                result += f"{target.name}'s {chant.stat} rose!"
                return result, True

    # returns outcome of using a curse
    def placeCurse(self, target, curse):
        result = ""
        if curse.xpCost > self.xp:
            result += f"The curse failed!\n"
            result += f" {self.name} doesn't have enough XP!"
            return result, False
        else:
            if curse.stat in target.status:
                result += f"{target.name} is already {curse.stat}!"
                return result, False
            else:
                self.xp -= curse.xpCost
                target.status.append("poisoned")
                result += f"{target.name} was {curse.stat}!"
                return result, True

    # helper function for using any form of magic
    def useMagic(self, player, target, magic):
        if isinstance(magic, OSpell):
            return(player.offenceSpell(target, magic))
        elif isinstance(magic, DSpell):
            return(player.defenceSpell(player, magic))
        elif isinstance(magic, Curse):
            return(player.placeCurse(target, magic))
        elif isinstance(magic, Chant):
            return(player.useChant(player, magic))
 
    # returns outcome of using an item
    def useItem(self, target, item):
        result = ""
        if item.count <= 0:
            result += f"{self.name} doesn't have any {item.name}s!"
            return result, False
        else:
            if item.stat != "HP" and item.stat != "XP":
                if item.stat in target.status:
                    target.status.remove(item.stat)
                    item.count -= 1
                    result += f"{target.name} is no longer {item.stat}"
                    return result, True
                else:
                    result += f"The {item.name} had no effect!"
                    return result, False
            else:
                if item.stat == "HP":
                    if target.hp == target.maxHP:
                        result += f"{target.name}'s HP is already full!"
                        return result, False
                    elif target.hp + item.weight >= target.maxHP:
                        preHP = target.hp
                        target.hp = target.maxHP
                        recovered = target.maxHP - preHP
                        item.count -= 1
                        result += f"{target.name} recovered {recovered}HP!"
                        return result, True
                    else:
                        target.hp += item.weight
                        item.count -= 1
                        result += f"{target.name} recovered {item.weight}HP!"
                        return result, True
                elif item.stat == "XP":
                    if target.xp == target.maxXP:
                        result += f"{target.name}'s XP is already full!"
                        return result, False
                    elif target.xp + item.weight >= target.maxXP:
                        preXP = target.xp
                        target.xp = target.maxXP
                        recovered = target.maxXP - preXP
                        item.count -= 1
                        result += f"{target.name} recovered {recovered}XP!"
                        return result, True
                    else:
                        target.xp += item.weight
                        item.count -= 1
                        result += f"{target.name} recovered {item.weight}XP!"
                        return result, True
    
class Weapon(object):
    def __init__(self, name, attack, accuracy):
        self.name = name
        self.attack = attack
        self.accuracy = accuracy

class OSpell(object):
    def __init__(self, name, damage, xpCost):
        self.name = name
        self.damage = damage
        self.xpCost = xpCost

class DSpell(object):
    def __init__(self, name, damage, xpCost):
        self.name = name
        self.damage = damage
        self.xpCost = xpCost

class Chant(object):
    def __init__(self, name, stat, modVal, xpCost):
        self.name = name
        self.stat = stat
        self.modVal = modVal
        self.xpCost = xpCost

class Curse(object):
    def __init__(self, name, stat, weight, xpCost):
        self.name = name
        self.stat = stat
        self.weight = weight
        self.xpCost = xpCost

class Item(object):
    def __init__(self, name, stat, weight, count):
        self.name = name
        self.count = count
        self.stock = self.count
        self.stat = stat
        self.weight = weight

# determines if an attack hits
def attackHit(accuracy):
    chance = random.randint(0,10)
    if chance < accuracy: return True
    else: return False

# determines if an attack does critical damage
def isCrit():
    chance = random.randint(0,6)
    if chance == 0: return True
    else: return False

# checks if a player has lost
def isDefeated(player):
    if player.hp <= 0:
        return True
    else: return False