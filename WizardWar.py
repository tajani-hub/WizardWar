#Name: Tioluwani Ajani
#Andrew ID: tajani
#Section C0

# Disclaimer: All sprites and images were sourced from the following websites:
# https://www.feplanet.net
# https://opengameart.org/content/pixel-art-adventurer-sprites
# https://seekpng.com 

from cmu_112_graphics import *
from functions_and_classes import *
from game_objects import *
from AI_functions import *

# Calls on all AI functions to determine next move
def AI_Play(p1, p2, depth):
    AI_heutValue, AI_moves = AI_moves_heutValues(p1, p2, depth)
    AI_bestDamage = AI_miniMax(0, depth, True, AI_heutValue, p1, p2, AI_moves)
    index = AI_damageToIndex(AI_bestDamage, AI_heutValue)
    result, move = AI_indexToMove(p1, p2, AI_moves, index)
    return f"{p2.name} used the {move}!", result[0]

#  Returns text for move options
def displayMoves(player, target):
    text = ""
    
    text = f"What will {player.name} do?\n 1: Use a weapon \n 2: Use magic"
    text += f"\n 3: Use an item \n 4: Concede"
    return text

# Returns text for move types
def displayMoveTypes(player, target, move): 
    if move == "1":
        text = f"Which weapon will {player.name} use?\n"
        weaponsList = player.weapons
        for i in range(len(player.weapons)):
            text += f"{i + 1}: {weaponsList[i].name}\n"            
    elif move == "2":
        text = f"Which spell will {player.name} use?\n"
        spellList = player.spells
        for i in range(len(player.spells)):
            text += f"{i + 1}: {spellList[i].name}\n"    
    elif move == "3":
        text = f"Which item will {player.name} use?\n"
        itemList = player.items
        for i in range(len(player.items)):
            text += f"{i + 1}: {itemList[i].name}\n"
    elif move == "4":
        text = f"{player.name} fled like a coward!"
        player.hp = 0    
    else: 
        text = "That's not an option!"
    return text

# Returns text for move result
def displayResult(player, target, moveCategory, move):
    if moveCategory == "1":
        try:
            weaponsList = player.weapons
            weaponChoice = int(move)
            if weaponChoice > len(weaponsList): return "Not an option!"
            text = (player.useWeapon(target, weaponsList[weaponChoice-1])[0])
        except ValueError:
            text = "You failed to execute a move!"
    elif moveCategory == "2":
        try:
            spellList = player.spells
            spellChoice = int(move)
            if spellChoice > len(spellList): return "Not an option!"
            text=(player.useMagic(player,target,spellList[spellChoice-1])[0])
        except ValueError:
            text = "You failed to execute a move!"
    elif moveCategory == "3":
        try:
            itemList = player.items
            itemChoice = int(move)
            if itemChoice > len(itemList): return "Not an option!"
            text = (player.useItem(player, itemList[itemChoice - 1])[0])
        except ValueError:
            text = "You failed to execute a move!"
    elif moveCategory == "4":
        text = f"{player.name} from battle!"
        player.hp = 0  
    else: return "You failed to execute a move!"
    return text

# adjusted data file functions
def doStatusDamage(player):
    text = f"{player.name} is poisoned!\n"
    text += f"{player.name} took {poisonCurse.weight} damage!"
    player.hp -= poisonCurse.weight
    return text

# Graphics handling portion with Tkinter and CMU 15-112 graphics
# Battle Mode

def keyPressed(app, event):
    if app.mode == "setUpMode":
        if event.key == "Left" or event.key == "Down":
            if app.diffSelection - 1 >= 1:
                app.diffSelection -= 1
        if event.key == "Right" or event.key == "Up":
            if app.diffSelection + 1 <= 5:
                app.diffSelection += 1

        # enemy sprite and display text set up, based on CMU 15-112 course notes
        # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
        if app.diffSelection == 1:
            app.diffText = veryEasyText
            app.enemy = veryEasy
            app.enemySpritePath = "sprites/veryEasy.png"
            app.enemyLoopLength = 5
            app.enemy_x0, app.enemy_x1 = 0, 28
            app.enemy_y0, app.enemy_y1 = 0, 25
            app.enemy_m = 28
        elif app.diffSelection == 2:
            app.diffText = easyText
            app.enemy = easy
            app.enemySpritePath = "sprites/easy.png"
            app.enemyLoopLength = 10
            app.enemy_x0, app.enemy_x1 = 0, 37
            app.enemy_y0, app.enemy_y1 = 0, 25
            app.enemy_m = 32
        elif app.diffSelection == 3:
            app.diffText = normalText
            app.enemy = normal
            app.enemySpritePath = "sprites/normal.gif"
            app.enemyLoopLength = 5
            app.enemy_x0, app.enemy_x1 = 1, 41
            app.enemy_y0, app.enemy_y1 = 0, 80
            app.enemy_m = 56
        elif app.diffSelection == 4:
            app.diffText = hardText
            app.enemy = hard
            app.enemySpritePath = "sprites/hard.gif"
            app.enemyLoopLength = 6
            app.enemy_x0, app.enemy_x1 = 3, 75
            app.enemy_y0, app.enemy_y1 = 0, 41
            app.enemy_m = 84
        elif app.diffSelection == 5:
            app.diffText = veryHardText
            app.enemy = veryHard
            app.enemySpritePath = "sprites/veryHard.gif"
            app.enemyLoopLength = 5
            app.enemy_x0, app.enemy_x1 = 0, 60
            app.enemy_y0, app.enemy_y1 = 0, 72
            app.enemy_m = 76

        enemySpriteStrip = app.loadImage(app.enemySpritePath)
        app.enemySprites = []
        for i in range(app.enemyLoopLength):
            app.enemySprite = enemySpriteStrip.crop(
                (app.enemy_x0 + i * app.enemy_m, app.enemy_y0,
                    app.enemy_x1 + i * app.enemy_m, app.enemy_y1)
            )
            app.enemySprites.append(app.enemySprite)
        app.enemySpriteCounter = 0

        if event.key == "Enter":
            app.mode = "battleMode"

    elif app.mode == "battleMode":
        if isDefeated(p1) or isDefeated(app.enemy):
            if event.key == "r":
                p1.reset()
                app.enemy.reset() 
                appStarted(app)

        # "falls through" stages of move making by toggling bools      
        else:
            if app.getMove:
                app.move = event.key
                app.getMove = False
                app.getMoveType = True
            elif app.getMoveType:
                app.moveType = event.key
                app.getMoveType = False
                app.showResult = True
            elif app.showResult:
                app.showResult = False
                app.showStatusDamage = True
            elif app.showStatusDamage:
                app.showStatusDamage = False
                app.showAIMove = True
            elif app.showAIMove:
                app.showAIMove = False
                app.showAIResult = True
            elif app.showAIResult:
                app.showAIResult = False
                app.showAIStatusDamage = True
            elif app.showAIStatusDamage:
                app.showAIStatusDamage = False
                app.getMove = True
            
            # displays appropriate texts
            if app.getMove:
                app.text = displayMoves(p1, app.enemy)
            if app.getMoveType:
                app.text = displayMoveTypes(p1, app.enemy, app.move)
            if app.showResult:
                app.text = displayResult(p1, app.enemy, app.move, app.moveType)
            if app.showStatusDamage:
                if "poisoned" in p1.status: app.text = doStatusDamage(p1)
            if app.showAIMove:
                app.AIMove, app.AIResult = AI_Play(p1, app.enemy, app.AI_depth)
                app.text = app.AIMove
            if app.showAIResult: 
                app.text = app.AIResult
            if app.showAIStatusDamage:
                if "poisoned" in app.enemy.status:
                    app.text = doStatusDamage(app.enemy)

def timerFired(app):
    # health bar colors
    if p1.hp > p1.maxHP*(2/3): app.p1HealthColor = "green"
    elif p1.maxHP*(1/3) < p1.hp <= p1.maxHP*(2/3): app.p1HealthColor = "orange"
    elif p1.hp < p1.maxHP*(1/3): app.p1HealthColor = "red"

    if app.enemy.hp > app.enemy.maxHP*(2/3): app.p2HealthColor = "green"
    elif app.enemy.maxHP*(1/3) < app.enemy.hp <= app.enemy.maxHP*(2/3): 
        app.p2HealthColor = "orange"
    elif app.enemy.hp < app.enemy.maxHP*(1/3): app.p2HealthColor = "red"
    
    if app.mode == "battleMode":
        app.playerSpriteCounter = ((1 + app.playerSpriteCounter) %
            len(app.playerSprites))
        app.enemySpriteCounter = ((1 + app.enemySpriteCounter) %
            len(app.enemySprites))

# functions that follow draw indinvidual screen components
def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "grey")

def drawEnemyStatBox(app, canvas):
    canvas.create_rectangle(0,0, 750, 150,
        outline = "black")
    canvas.create_text(140, 45,
        text = "Enemy HP:", font = "Modern 20 bold", fill="white", anchor="e")
    #Full HPBar
    canvas.create_rectangle(150, 30,
        600, 60, fill = "white")
    #Depleted HPBar
    if app.enemy.hp >= 0:
        canvas.create_rectangle(150, 30,150+450*(app.enemy.hp/app.enemy.maxHP), 
            60, fill = app.p2HealthColor)
    canvas.create_text(140, 90,
        text = "Enemy XP:", font = "Modern 20 bold", fill="white", anchor="e")
    #Full XPBar
    canvas.create_rectangle(150, 75,
        600, 105, fill = "white")
    #Depleted XPBar
    if app.enemy.xp >= 0:
        canvas.create_rectangle(150, 75,
            150 + (450)*(app.enemy.xp/app.enemy.maxXP), 
            105, fill = "purple")

def drawPlayerStatBox(app, canvas):
    canvas.create_rectangle(0, 450, 500, 600,outline = "black")
    canvas.create_text(50, 500,
        text = "HP:", font = "Modern 20 bold", fill = "white", anchor = "e")
    #FullHPBar
    canvas.create_rectangle(70, 490,
        470, 510, fill = "white")
    #DepletedHPBar
    if p1.hp >= 0:
        canvas.create_rectangle(70, 490,
            70 + (400)*(p1.hp/p1.maxHP), 510, fill = app.p1HealthColor)

    canvas.create_text(270, 500, font = "Modern 16 bold", fill = "black",
        text = f"{p1.hp}/{p1.maxHP}")

    canvas.create_text(50, 550,
        text = "XP:", font = "Modern 20 bold", fill = "white", anchor = "e")
    #FullXPBar
    canvas.create_rectangle(70, 540,
        470, 560, fill = "white")
    #DepletedXPBar
    if p1.xp >= 0:
        canvas.create_rectangle(70, 540,
            70 + (400)*(p1.xp/p1.maxXP), 560, fill = "purple")
    canvas.create_text(270, 550, font = "Modern 16 bold", fill = "black",
        text = f"{p1.xp}/{p1.maxXP}")

def drawPlayerInventory(app, canvas):
    canvas.create_rectangle(500, 450, 750, 600)
    for i in range(len(p1.items)):
        canvas.create_text(550, 500 + i*(30),
            text = f"{p1.items[i].name}s: {p1.items[i].count}",
            anchor = "w", font = "Modern 15 bold", fill = "white")

def displayInFightBox(app, canvas):
    canvas.create_text(30, 175, text = app.text, fill = "White",
        font = "Modern 30 bold", anchor = "nw")

def drawFightBox(app, canvas):
    canvas.create_rectangle(0, 150, 900, 450)
    displayInFightBox(app, canvas)

def drawWinLossScreen(app, canvas):
    if isDefeated(p1):
        # canvas.create_rectangle(0, 150, 750, 450, fill = "grey")
        canvas.create_text(450, 300, text = "YOU DIED.",
            font = "Modern 40 bold", fill = "maroon")
        canvas.create_text(20, 400, text = "Press r to begin a new battle!",
            fill = "white", font = "Modern 20 bold", anchor = "nw")
        canvas.create_rectangle(750, 0, 900, 150, fill = "grey")
        canvas.create_image(825, 75, image=ImageTk.PhotoImage(app.winnerImage))
        canvas.create_rectangle(750, 450, 900, 600, fill = "grey")
        canvas.create_image(825, 525, image=ImageTk.PhotoImage(app.loserImage))
        
    if isDefeated(app.enemy):
        # canvas.create_rectangle(0, 150, 750, 450, fill = "grey")
        canvas.create_text(450, 300, text = "VICTORY!",
            font = "Modern 40 bold", fill = "gold")
        canvas.create_text(20, 400, text = "Press r to begin a new battle!",
            fill = "white", font = "Modern 20 bold", anchor = "nw")
        canvas.create_rectangle(750, 0, 900, 150, fill = "grey")
        canvas.create_image(825, 75, image=ImageTk.PhotoImage(app.loserImage))
        canvas.create_rectangle(750, 450, 900, 600, fill = "grey")
        canvas.create_image(825, 525, image=ImageTk.PhotoImage(app.winnerImage))

def drawEnemyContainer(app, canvas):
    canvas.create_rectangle(750, 0, 900, 150)
    sprite = app.enemySprites[app.enemySpriteCounter]
    sprite = sprite.resize((100, 100))
    canvas.create_image(825, 75, image = ImageTk.PhotoImage(sprite))

def drawPlayerContainer(app, canvas):
    canvas.create_rectangle(750, 450, 900, 600)
    sprite = app.playerSprites[app.playerSpriteCounter]
    sprite = sprite.resize((100, 100))
    canvas.create_image(825, 525, image = ImageTk.PhotoImage(sprite))

def battleMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawEnemyStatBox(app, canvas)
    drawPlayerStatBox(app, canvas)
    drawPlayerInventory(app, canvas)
    drawEnemyContainer(app, canvas)
    drawPlayerContainer(app, canvas)
    drawFightBox(app, canvas)
    drawWinLossScreen(app, canvas)

def drawTopBox(app, canvas):
    canvas.create_rectangle(0, 0, 900, 100, fill = "grey")
    canvas.create_text(450, 50, text = "Welcome to Wizard War!\
        Choose an opponent!",
        font = "Modern 26 bold", fill = "white")

def drawDifficultyText(app, canvas):
    canvas.create_text(200, 200, text = app.diffText,
        font = "Modern 32 bold", fill = "white", anchor = "nw")

def drawInstructions(app, canvas):
    instructions = "Use the Left/Right/Down/Up keys to choose a difficulty."
    instructions += "\nPress Enter to begin."
    canvas.create_rectangle(0, 500, 900, 600, fill = "grey")
    canvas.create_text(20, 520, font = "Modern 18 bold", fill = "white",
        anchor = "nw", text = instructions)

def drawLeftAndRightArrows(app, canvas):
    if app.diffSelection != 1:
        canvas.create_polygon(70, 250, 40, 300, 70, 350, fill = "white",
            outline = "white") 
    if app.diffSelection != 5:
        canvas.create_polygon(830, 250, 860, 300, 830, 350, fill = "white",
            outline = "white")   

def setUpMode_redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawTopBox(app, canvas)
    drawDifficultyText(app, canvas)
    drawInstructions(app, canvas)
    drawLeftAndRightArrows(app, canvas)

# Main App
def appStarted(app):
    app.mode = "setUpMode"
    setUpModeInit(app)
    battleModeInit(app)

def setUpModeInit(app):
    app.diffSelection = 1
    app.diffText = veryEasyText
    app.enemy = veryEasy

def battleModeInit(app):
    app.move = -1
    app.moveType = -1
    app.text = f"What will {p1.name} do?\n 1: Use a weapon \n 2: Use magic"
    app.text += f"\n 3: Use an item \n 4: Concede"
    app.getMove = True
    app.getMoveType = False
    app.showResult = False
    app.showStatusDamage = False
    app.showAIResult = False
    app.showAIMove = False
    app.showAIStatusDamage = False
    app.AIMove = ""
    app.AIResult = "" 
    app.p1HealthColor = "green"
    app.p2HealthColor = "green" 
    app.AI_depth = app.diffSelection

    #player sprite set up (based on cmu 15-112 course notes 
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

    app.playerSpritePath = "sprites/you.png"
    playerSpriteStrip = app.loadImage(app.playerSpritePath)
    app.playerSprites = []
    for i in range(7):
        app.playerSprite = playerSpriteStrip.crop((7+50*i, 0, 50+50*i, 37))
        app.playerSprites.append(app.playerSprite)
    app.playerSpriteCounter = 0

    app.winImagePath = "sprites/trophy.png"
    app.loserImagePath = "sprites/skull.png"

    app.winnerImage = app.loadImage(app.winImagePath)
    app.winnerImage = app.winnerImage.resize((100, 100))
    app.loserImage = app.loadImage(app.loserImagePath)
    app.loserImage = app.loserImage.resize((100, 100))

def redrawAll(app, canvas):
    if app.mode == "battleMode":
        battleMode_redrawAll(app, canvas)
    if app.mode == "setUpMode":
        setUpMode_redrawAll(app, canvas)

runApp(width=900, height=600, x=350, y=100)