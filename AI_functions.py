# Name: Tioluwani Ajani
# AndrewID: tajani
# Section: C0
 
# AI operates on a MiniMax Algorithm 

import math
from functions_and_classes import *
from game_objects import *

# function determines heuteristic values of every move possible
# and returns a dictionary, as well as a matching move list

def AI_moves_heutValues(p1, p2, steps):
    # create array of moves from properties of p2 object
    AI_moves = []
    AI_moves.extend(p2.weapons)
    AI_moves.extend(p2.spells)
    AI_moves.extend(p2.items)
    # create dictionary to populate with moves and values
    AI_heutVal = dict()
    
    # loop through all moves and calculate value based on move type
    for move in range(len(AI_moves)):
        # Weapon: Damage * Accuracy
        if isinstance(AI_moves[move], Weapon):
            AI_heutVal[move] = (AI_moves[move].attack *
                (AI_moves[move].accuracy/10))
        # Offence Spell: Damage * (1 - XPCost/totalXP)
        elif isinstance(AI_moves[move], OSpell):
            AI_heutVal[move] = (AI_moves[move].damage *
                (1-(AI_moves[move].xpCost/p2.maxXP)))
        # Defence Spell: RecoveryAmount * (1 - XPCost/totalXP)
        elif isinstance(AI_moves[move], DSpell):
            AI_heutVal[move] = (abs(AI_moves[move].damage) *
                (1-(AI_moves[move].xpCost/p2.maxXP)))
        # Item
        elif isinstance(AI_moves[move], Item):
            # PoisonDamagePerRound * NumberOfRounds
            if AI_moves[move].name == "Antidote":
                AI_heutVal[move] = poisonCurse.weight*steps
            # HPRecovered * (1/(1 - PotionsInInventory))
            if AI_moves[move].name == "Potion":
                AI_heutVal[move] = (AI_moves[move].weight *
                    (1 - 1/AI_moves[move].stock))
            # XPRecovered * (1/(1 - ElixirsInInventory))
            if AI_moves[move].name == "Elixir":
                AI_heutVal[move] = (AI_moves[move].weight * 
                (1 - 1/AI_moves[move].stock))
        # Curse: CurseDamagePerRound * NumberOfRounds * (1 - XPCost/totalXP)
        elif isinstance(AI_moves[move], Curse):
            AI_heutVal[move] = (AI_moves[move].weight*steps * 
            (1 - AI_moves[move].xpCost/p2.maxXP))
        # Chant: 0.7*(P1LastWeaponStrength)
        elif isinstance(AI_moves[move], Chant):
            AI_heutVal[move] = p1.weapons[-1].attack*(0.7)
    return AI_heutVal, AI_moves

# function returns the best possible gain the AI can attain in this round using
# minimax algorithm
# (based on pseudocode from https://en.wikipedia.org/wiki/Minimax)

# depth: steps the AI will look ahead 
def AI_miniMax(bestDamage, depth, isMaxPlayer, AI_heutValue, p1, p2, AI_moves):
    if depth == 0:
        return bestDamage
    # maximize damage done
    if isMaxPlayer:
        # default option (not doing anything) is infinitely harmful hence -inf
        damage = -math.inf
        # loop through every possible move
        for move in AI_heutValue:
            # ignore illegal moves
            if AI_isLegalMove(p1, p2, AI_moves, move) == False:
                continue
            nextNodeDmg = AI_miniMax(AI_heutValue[move], depth - 1, 
                False, AI_heutValue, p1, p2, AI_moves)
            if nextNodeDmg > damage and AI_isLegalMove(p1, p2, AI_moves, move):
                damage = nextNodeDmg
        return damage
    # minimize damage taken
    else:
        damage = math.inf
        for move in AI_heutValue:
            if AI_isLegalMove(p1, p2, AI_moves, move) == False:
                continue
            nextNodeDmg = AI_miniMax(AI_heutValue[move], depth - 1,
                True, AI_heutValue, p1, p2, AI_moves)
            if nextNodeDmg < damage and AI_isLegalMove(p1, p2, AI_moves, move):
                damage = nextNodeDmg
        return damage

#determines if a move is legal
def AI_isLegalMove(p1, p2, AI_moves, index):
    # weapons always valid
    if isinstance(AI_moves[index], Weapon): return True
    # determine if there's sufficient XP for offense spell
    elif isinstance(AI_moves[index], OSpell):
        if p2.xp < AI_moves[index].xpCost: return False
        else: return True
    # determine if there's sufficient XP for defence spell and HP isn't full
    elif isinstance(AI_moves[index], DSpell):
        if p2.xp < AI_moves[index].xpCost: return False
        elif p2.hp == p2.maxHP: return False
        else: return True
    # determine if there's sufficient XP and opponent isn't already cursed
    elif isinstance(AI_moves[index], Curse):
        if AI_moves[index].stat in p1.status: return False
        elif p2.xp < AI_moves[index].xpCost: return False
        else: return True
    # determine if there's sufficient XP and Defence isn't maxed out
    elif isinstance(AI_moves[index], Chant):
        if p2.xp < AI_moves[index].xpCost: return False
        elif p2.defence + AI_moves[index].modVal >= 0.7: return False
        else: return True
    elif isinstance(AI_moves[index], Item):
        # determine if item is in inventory
        if AI_moves[index].count <= 0:return False
        else:
            # if not Potion or Elixir, ensure stat effect is acually present
            if AI_moves[index].stat != "HP" and AI_moves[index].stat != "XP":
                if AI_moves[index].stat in p2.status: return True
                else: return False
            else:
                #ensure HP isn't maxxed
                if AI_moves[index].stat == "HP":
                    if p2.hp == p2.maxHP: return False
                    else: return True
                #ensure XP isn't maxxed
                elif AI_moves[index].stat == "XP":
                    if p2.xp == p2.maxXP: return False
                    else: return True     

# this function takes the best possible damage according to MiniMax
# and coverts to an index in the move list

def AI_damageToIndex(AI_bestDamage, AI_heutValue):
    for move in AI_heutValue:
        if AI_heutValue[move] == AI_bestDamage:
            bestMove = move
    return bestMove

# this function performs the move corresponding to the appropriate index
def AI_indexToMove(p1, p2, AI_moves, index):
    if isinstance(AI_moves[index], Weapon):
        return p2.useWeapon(p1, AI_moves[index]), AI_moves[index].name
    elif isinstance(AI_moves[index], OSpell):
        return p2.useMagic(p2, p1, AI_moves[index]), AI_moves[index].name
    elif isinstance(AI_moves[index], DSpell):
        return p2.useMagic(p2, p1, AI_moves[index]), AI_moves[index].name
    elif isinstance(AI_moves[index], Curse):
        return p2.useMagic(p2, p1, AI_moves[index]), AI_moves[index].name
    elif isinstance(AI_moves[index], Chant):
        return p2.useMagic(p2, p1, AI_moves[index]), AI_moves[index].name
    elif isinstance(AI_moves[index], Item):
        return p2.useItem(p2, AI_moves[index]), AI_moves[index].name 