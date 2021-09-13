from random import random, randint

def generate():
    rarity = 100
    #SPECIAL CASES:
    if random() > 0.995:
        minecraft = True
    else:
        minecraft = False

    #Set probablity scores
    probs={
        'model' :        (0.995, 0.85, 0.5, 0),
        'snake' :        (0.98, 0.92, 0.75, 0.5, 0),
        'speed' :        (0.99, 0.6, 0),
        'transparency' : (0, 0),
        'color' :        (0.995, 0.98, 0.97, 0.95, 0.92, 0.88, 0.3, 0),
        'spin' :         (0.99, 0.9, 0),
        'texture' :      (0.99, 0.98, 0.95, 0.91, 0),
        'background' :   (0.99, 0.6, 0.3, 0),
        'mirror' :       (0.3, 0),
        'wireframe' :    (0.8, 0.3, 0),
        'sticker' :      (0.9999,0.999,0.995, 0.95, 0)
    }


    #MODEL SELECTION
    modelSeed = random()
    if minecraft:
        sizeNormalizer = 5
        modelType = 'box.egg'
        scaleMod = (1,1,1)
    else:
        if modelSeed > probs['model'][0]:
            sizeNormalizer = 8
            scaleMod = (1,1,1)
            modelType = 'monkey.egg'
        elif modelSeed > probs['model'][1]:
            sizeNormalizer = 2
            scaleMod = (3,0.5,0.5)
            modelType = 'Icosahedron.egg'
        elif  modelSeed > probs['model'][2]:
            sizeNormalizer = 2
            scaleMod = (1,1,1)
            modelType = 'Icosahedron.egg'
        else:
            sizeNormalizer = 4.5
            scaleMod = (1,1,1)
            modelType = 'box.egg'

    #NUMBER OF MEGARMS, numNODES, SIZES
    snakeSeed = random()
    if snakeSeed > probs['snake'][0]:
        numSnakes=5
        sizeMod = 0.6
        numNodes = randint(300,350)
    elif snakeSeed > probs['snake'][1]:
        numSnakes=4
        sizeMod = 0.75
        numNodes = randint(200,300)
    elif snakeSeed > probs['snake'][2]:
        numSnakes=3
        sizeMod = 1
        numNodes = randint(125,200)
    elif snakeSeed > probs['snake'][3]:
        sizeMod = 1.1
        numNodes = randint(50,75)
        numSnakes=2
    else:
        sizeMod = 1.2
        numNodes = randint(100,150)
        numSnakes=1

    modelScale = (sizeMod * sizeNormalizer * scaleMod[0], sizeMod * sizeNormalizer * scaleMod[1], sizeMod * sizeNormalizer * scaleMod[2])

    #JOINT SPEED RANGE
    speedSeed = random()
    if speedSeed > probs['speed'][0]: #SPARKLES
        jointSpeedRange = (10,20)
        modelSpin = 0
    elif speedSeed > probs['speed'][1]:
        jointSpeedRange = (3,6)
        modelSpin = 2
    else:
        jointSpeedRange = (1.5,3)
        modelSpin = 3.5
    lengthRange = (0,20)

    #BASE SPEED RANGE
    if speedSeed > probs['speed'][0]: #SPARKLES
        baseSpeedRange = (0,1)
        modelSpin = 0
    elif speedSeed > probs['speed'][1]:
        baseSpeedRange = (3,6)
        modelSpin = 2
    else:
        baseSpeedRange = (1.5,3)
        modelSpin = 3.5
    lengthRange = (0,20)


    #COLORS
    colorSeed = random()
    colors=[]
    if colorSeed > probs['color'][0]: #DARK RAINBOW
        colors.append((0.45,0,0.1))
        colors.append((0.45,0.4,0.1))
        colors.append((0.475,0.45,0.1))
        colors.append((0.1,0.475,0.3))
        colors.append((0.15,0.1,0.50))
        colors.append((.30,.1,0.5))
        colors.append((0.45,0,0.1))
        colors.append((0.45,0.4,0.1))
        colors.append((0.475,0.45,0.1))
        colors.append((0.1,0.475,0.3))
        colors.append((0.15,0.1,0.50))
        colors.append((.30,.1,0.5))
        colors.append((0.45,0,0.1))
        colors.append((0.45,0.4,0.1))
        colors.append((0.475,0.45,0.1))
        colors.append((0.1,0.475,0.3))
        colors.append((0.15,0.1,0.50))
        colors.append((.30,.1,0.5))
    elif colorSeed > probs['color'][1]: #zebra
        colors.append((random(),random(),random()))
        colors.append((random(),random(),random()))
        colors.append((random(),random(),random()))
        colors.append((random(),random(),random()))
        colors.append((random(),random(),random()))
        colors.append((random(),random(),random()))
    elif colorSeed > probs['color'][2]: #8 randoms
        colors.append((0,0,0))
        colors.append((1,1,1))
        colors.append((0,0,0))
        colors.append((1,1,1))
        colors.append((0,0,0))
        colors.append((1,1,1))
    elif colorSeed > probs['color'][3]: #RAINBOW
        colors.append((0.9,0,0))
        colors.append((0.9,0.4,0))
        colors.append((0.95,0.9,0.05))
        colors.append((0.2,0.95,0.2))
        colors.append((0.2,0.2,0.95))
        colors.append((.55,.2,1))
        colors.append((0.9,0,0))
        colors.append((0.9,0.4,0))
        colors.append((0.95,0.9,0.05))
        colors.append((0.2,0.95,0.2))
        colors.append((0.2,0.2,0.95))
        colors.append((.55,.2,1))
        colors.append((0.9,0,0))
        colors.append((0.9,0.4,0))
        colors.append((0.95,0.9,0.05))
        colors.append((0.2,0.95,0.2))
        colors.append((0.2,0.2,0.95))
        colors.append((.55,.2,1))
    elif colorSeed > probs['color'][4]: #RGB flash
        colors.append((0.1,0.2,0.35))
        colors.append((0.95,0.91,0.89))
        colors.append((1,0.4,0.25))
        colors.append((1,0.82,0.2))
        colors.append((0.1,0.2,0.35))
        colors.append((0.95,0.91,0.89))
        colors.append((1,0.4,0.25))
        colors.append((1,0.82,0.2))
        colors.append((0.1,0.2,0.35))
        colors.append((0.95,0.91,0.89))
        colors.append((1,0.4,0.25))
        colors.append((1,0.82,0.2))
    elif colorSeed > probs['color'][5]:
        colors.append((.55,.2,1))
        colors.append((0.9,0.4,0))
        colors.append((.55,.2,1))
        colors.append((0.9,0.4,0))
        colors.append((.55,.2,1))
        colors.append((0.9,0.4,0))
        colors.append((.55,.2,1))
        colors.append((0.9,0.4,0))
    elif colorSeed > probs['color'][6]:
        colors.append((random(),random(),random()))
        colors.append((random(),random(),random()))
        colors.append((random(),random(),random()))
    else:
        colors.append((random(),random(),random()))
        colors.append((random(),random(),random()))

    if len(colors) > 1:
        if random() > probs['transparency'][0]:
            transparency = True
        else:
            transparency = False
    else:
        transparency = True

    #CAMERA SPINNING
    spinSeed = random()
    if spinSeed > probs['spin'][0]:
        spinSpeed = randint(-15,15)
    elif spinSeed > probs['spin'][1]:
        spinSpeed = randint(-2,2)
    else:
        spinSpeed = randint(-1,1)
        #none, zebra, multi
    if random() > 0.5:
        spinSpeed*-1

    #TEXTURES
    texSeed = random()
    backgroundImage = None
    if minecraft:
        texture = '0.png'  #MINECRAFT GRASS
        colors=((1,1,1),(1,1,1))
        backgroundColor = (0.380, 0.882, 0.960)
    elif texSeed > probs['texture'][0]:
        texture = 'rainbow.png'  #icy (probably temp)
        colors=((1,1,1),(1,1,1))
        backgroundColor = (1,1,1)
    elif texSeed > probs['texture'][1]:
        texture = '1.png'  #icy (probably temp)
        colors=((1,1,1),(1,1,1))
        backgroundColor = (0.2, 0.4, 0.9)
    elif texSeed > probs['texture'][2]:
        texture = '2.png' #shitty temp
        colors=((0.2,0.05,0),(0.8,0.95,1))
        backgroundColor = 'opposite'
    elif texSeed > probs['texture'][3]:
        colors=((1,1,1),(1,1,1))
        texture = None
        backgroundColor = (0,0,0)
        backgroundImage = 'tv.jpg'
    else:
        backgroundSeed = random()
        if backgroundSeed > probs['background'][0]:
            backgroundColor = (0.2,0,0.2)
        elif backgroundSeed > probs['background'][1]:
            backgroundColor = 'opposite'
        elif backgroundSeed > probs['background'][2]:
            backgroundColor = (0,0.2,0.2)
        else:
            backgroundColor = (0,0,0)
        texture = None

    if random() > probs['mirror'][0]: #I WANT DOUBLE MIRRORS
        mirror = True #7
    else:
        mirror = False

    drawSnakes = True

    if numSnakes > 2:
        wireframeSeed = random()
        if wireframeSeed > probs['wireframe'][0] and mirror == False:
            drawWireframe = True
        elif wireframeSeed > probs['wireframe'][1] and mirror == False:
            drawWireframe = True
            drawSnakes = False
        else:
            drawWireframe = False
    else:
        drawSnakes = True
        drawWireframe = False

    #STICKERGEN
    stickerSeed = random()
    if stickerSeed > probs['sticker'][0]:
        stickers = 4
    elif stickerSeed > probs['sticker'][1]:
        stickers = 3
    elif stickerSeed > probs['sticker'][2]:
        stickers = 2
    elif stickerSeed > probs['sticker'][3]:
        stickers = 1
    else:
        stickers = 0
    #color type
    #gradients
    #shrinking
    #specialCases (zebra, rainbow, cotton_candy, leapord), PURE FIRE
    prop={
        'num_snakes' : numSnakes,
        'base_speed_range' : baseSpeedRange,
        'joint_speed_range' : jointSpeedRange,
        'model_scale' : modelScale,
        'num_snake_heads' : numNodes,
        'num_wireframes' : 85,
        'model_type' : modelType,
        'colors' : colors,
        'background_color' : backgroundColor,
        'background_image' : backgroundImage,
        'transparency' : transparency,
        'mirror' : mirror,
        'texture' : texture,
        'camera_spin' : spinSpeed,
        'draw_wireframe' : drawWireframe,
        'draw_snakes' : drawSnakes,
        'num_stickers' : stickers,
        'model_spin' : modelSpin
    }
    return prop
