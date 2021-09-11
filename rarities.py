from random import random, randint

def generate():
    rarity = 100
    if random() > 0.995:
        minecraft = True
    else:
        minecraft = False

    #Set probablity scores
    probs={
        'model' :        (0.99, 0.4, 0),
        'snake' :        (0.98, 0.92, 0.75, 0.5, 0),
        'speed' :        (0.85, 0.6, 0),
        'transparency' : (0.2, 0),
        'color' :        (0.99, 0.96, 0.92, 0.88, 0.6, 0),
        'spin' :         (0.99, 0.9, 0.7, 0),
        'texture' :      (0.99, 0.98, 0.95, 0),
        'background' :   (0.6, 0.1, 0),
        'mirror' :       (0.5, 0),
        'wireframe' :    (0.97, 0.7, 0)
    }


    #MODEL SELECTION
    modelSeed = random()
    if minecraft:
        sizeNormalizer = 5
        modelType = 'box.egg'
    else:
        if modelSeed > probs['model'][0]:
            sizeNormalizer = 8
            modelType = 'monkey.egg'
        elif modelSeed > probs['model'][1]:
            sizeNormalizer = 2
            modelType = 'Icosahedron.egg'
        else:
            sizeNormalizer = 5
            modelType = 'box.egg'

    #NUMBER OF MEGARMS, numNODES, SIZES
    snakeSeed = random()
    if snakeSeed > probs['snake'][0]:
        numSnakes=5
        modelSize = sizeNormalizer*0.5
        numNodes = randint(400,500)
    elif snakeSeed > probs['snake'][1]:
        numSnakes=4
        modelSize = sizeNormalizer*0.85
        numNodes = randint(300,400)
    elif snakeSeed > probs['snake'][2]:
        numSnakes=3
        modelSize = sizeNormalizer*1
        numNodes = randint(200,300)
    elif snakeSeed > probs['snake'][3]:
        modelSize = sizeNormalizer*1.3
        numNodes = randint(100,200)
        numSnakes=2
    else:
        modelSize = sizeNormalizer*1.7
        numNodes = randint(50,100)
        numSnakes=1

    speedSeed = random()
    if speedSeed > probs['speed'][0]: #SPARKLES
        speedRange = (-75,75)
    elif speedSeed > probs['speed'][1]:
        speedRange = (-15,15)
    else:
        speedRange = (-5,5)
    lengthRange = (0,20)


    if numNodes > 1:
        if random() > probs['transparency'][0]:
            transparency = True
        else:
            transparency = False
    else:
        transparency = True




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
    elif colorSeed > probs['color'][1]: #RAINBOW
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
    elif colorSeed > probs['color'][2]: #RGB flash
        colors.append((0.1,0.1,0.5))
        colors.append((0.9,0.9,1))
        colors.append((0.1,0.5,0.1))
        colors.append((0.9,1,0.9))
        colors.append((0.5,0.1,0.1))
        colors.append((1,0.9,0.9))
        colors.append((0.1,0.1,0.5))
        colors.append((0.9,0.9,1))
        colors.append((0.1,0.5,0.1))
        colors.append((0.9,1,0.9))
        colors.append((0.5,0.1,0.1))
        colors.append((1,0.9,0.9))
    elif colorSeed > probs['color'][3]:
        colors.append((.55,.2,1))
        colors.append((0.9,0.4,0))
        colors.append((.55,.2,1))
        colors.append((0.9,0.4,0))
        colors.append((.55,.2,1))
        colors.append((0.9,0.4,0))
        colors.append((.55,.2,1))
        colors.append((0.9,0.4,0))
    elif colorSeed > probs['color'][4]:
        colors.append((random(),random(),random()))
        colors.append((random(),random(),random()))
    else:
        colors.append((random(),random(),random()))

    #SPINNING
    spinSeed = random()
    if spinSeed > probs['spin'][0]:
        spinSpeed = 1000
    elif spinSeed > probs['spin'][1]:
        spinSpeed = 200
    elif spinSeed > probs['spin'][2]:
        spinSpeed = 45
    else:
        spinSpeed = 20
        #none, zebra, multi

    #TEXTURES
    texSeed = random()
    if minecraft:
        texture = '0.png'  #MINECRAFT GRASS
        colors=(((1,1,1),(1,1,1)))
        backgroundColor = (0.380, 0.882, 0.960)
    elif texSeed > probs['texture'][0]:
        texture = 'rainbow.png'  #icy (probably temp)
        colors=(((1,1,1),(1,1,1)))
        backgroundColor = (1,1,1)
    elif texSeed > probs['texture'][1]:
        texture = '1.png'  #icy (probably temp)
        colors=(((1,1,1),(1,1,1)))
        backgroundColor = (0.2, 0.4, 0.9)
    elif texSeed > probs['texture'][2]:
        texture = '2.png' #shitty temp
        colors=(((0.2,0.05,0),(0.8,0.95,1)))
        backgroundColor = 'opposite'
    else:
        backgroundSeed = random()
        if backgroundSeed > probs['background'][0]:
            backgroundColor = 'opposite'
        elif backgroundSeed > probs['background'][1]:
            backgroundColor = (0,0,0)
        else:
            backgroundColor = (1,1,1)
        texture = None

    if random() > probs['mirror'][0]: #I WANT DOUBLE MIRRORS
        mirror = True #7
    else:
        mirror = False

    drawSnakes = True

    if numSnakes > 1:
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

    #color type
    #gradients
    #shrinking
    #specialCases (zebra, rainbow, cotton_candy, leapord), PURE FIRE
    prop={
        'num_snakes' : numSnakes,
        'speed_range' : speedRange,
        'model_size' : modelSize,
        'num_nodes' : numNodes,
        'model_type' : modelType,
        'colors' : colors,
        'background_color' : backgroundColor,
        'transparency' : transparency,
        'mirror' : mirror,
        'texture' : texture,
        'spin_speed' : spinSpeed,
        'draw_wireframe' : drawWireframe,
        'draw_snakes' : drawSnakes
    }
    return prop
