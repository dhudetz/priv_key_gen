from random import random, randint

def generate():
    themePoints = {
        'common' :              70,
        'neon_sunset' :         5,
        'ice' :                 5,
        'lava' :                5,
        'hubba_bubba' :         5,
        'yin_yang' :            5,
        'rgb_zebra':            5,
        'purple_zebra' :        5,
        'sprinkles' :           5,
        'rainbow' :             2,
        'diamond' :             2,
        'red_blue' :            5,
        'galaxy' :              1,
        'peacock' :             1,
        'alien_candy' :         1
    }
    totalPoints = 0
    for key in themePoints:
        totalPoints += themePoints[key]
    prevVal = 1
    themeProbs={}
    for key in themePoints:
        themeProbs[key] = prevVal - (themePoints[key] / totalPoints)
        prevVal = themeProbs[key]

    rotateModel=True
    texture = None
    testing = False

# colors=((1,1,1),(1,1,1))
# backgroundColor = (0.5,0.5,0.5)
# filter=(1,0,False)
# colorPattern='gradient'
# texture = '2.png'
    postProcess = ''
    lights = (('p', (0.9, 0.9, 0.9, 1), 0, 0, 0),('a', (0.5, 0.5, 0.5, 1)))
    #THEMES
    if testing:
        colors=((1, 0.549, 0.078),(1, 0.113, 0.078),(0.568, 0.188, 0.094),(0.925, 0.776, 0.196),(0.925, 0.196, 0.227),(0.627, 0.443, 0.133),(1, 0.549, 0.078),(1, 0.113, 0.078),(0.568, 0.188, 0.094),(0.925, 0.776, 0.196),(0.925, 0.196, 0.227),(0.627, 0.443, 0.133))
        backgroundColor=(0.819, 0.274, 0.101)
        filter=(0,0.1,False)
        colorPattern='gradient'

        #postProcess='starrynight.jfif'
    else:
        themeSeed = random()
        if themeSeed > themeProbs['common']:
            color = (random()*0.5,random()*0.5,random()*0.5)
            colors=(color,color)
            backgroundColor='opposite'
            filter=(0,0,False)
            colorPattern='gradient'
        elif themeSeed > themeProbs['neon_sunset']:
            colors=((.55,.2,1),(0.9,0.4,0),(.55,.2,1),(0.9,0.4,0),(.55,.2,1),(0.9,0.4,0),(.55,.2,1),(0.9,0.4,0))
            backgroundColor=(0.074, 0.066, 0.309)
            filter=(0,0,False)
            colorPattern='gradient'
        elif themeSeed > themeProbs['ice']:
            colors=((0.788, 0.898, 0.972),(0.588, 0.749, 0.894),(0.788, 0.898, 0.972),(0.588, 0.749, 0.894),(0.788, 0.898, 0.972),(0.588, 0.749, 0.894))
            backgroundColor=(0.937, 0.949, 0.960)
            filter=(1,0,False)
            colorPattern='gradient'
        elif themeSeed > themeProbs['lava']:
            colors=((1, 0.549, 0.078),(1, 0.113, 0.078),(0.568, 0.188, 0.094),(0.925, 0.776, 0.196),(0.925, 0.196, 0.227),(0.627, 0.443, 0.133),(1, 0.549, 0.078),(1, 0.113, 0.078),(0.568, 0.188, 0.094),(0.925, 0.776, 0.196),(0.925, 0.196, 0.227),(0.627, 0.443, 0.133))
            backgroundColor=(0.819, 0.274, 0.101)
            filter=(0,0.1,False)
            colorPattern='gradient'
        elif themeSeed > themeProbs['hubba_bubba']:
            colors=((0.921, 0.227, 0.933),(0.227, 0.933, 0.384),(0.921, 0.227, 0.933),(0.227, 0.933, 0.384),(0.921, 0.227, 0.933),(0.227, 0.933, 0.384),(0.921, 0.227, 0.933),(0.227, 0.933, 0.384),(0.921, 0.227, 0.933),(0.227, 0.933, 0.384),(0.921, 0.227, 0.933),(0.227, 0.933, 0.384))
            backgroundColor=(0.901, 0.580, 0.886)
            filter=(0,0,False)
            colorPattern='gradient'
        elif themeSeed > themeProbs['yin_yang']:
            colors=((0,0,0),(1,1,1),(0,0,0),(1,1,1),(0,0,0),(1,1,1),(0,0,0))
            backgroundColor='opposite'
            filter=(1,0,False)
            colorPattern='gradient'
            lights = []
        elif themeSeed > themeProbs['rgb_zebra']:
            colors=((0.182, 0.578, 0.697),(1,1,1),(0.904, 0.110, 0.0013),(1,1,1),(0.535, 0.928, 0.0319),(1,1,1))
            backgroundColor=(0.2,0.2,0.2)
            filter=(2,0,False)
            colorPattern='alternate'
        elif themeSeed > themeProbs['purple_zebra']:
            colors=((0.862, 0.545, 0.933),(1,1,1),(0.619, 0.380, 0.741),(1,1,1),(0.882, 0.623, 0.917),(1,1,1))
            backgroundColor=(0.756, 0.580, 0.901)
            filter=(0,0.4,False)
            colorPattern='alternate'
        elif themeSeed > themeProbs['sprinkles']:
            texture = 'rainbow.png'
            colors=((1,1,1),(1,1,1))
            backgroundColor = (1,1,1)
            filter=(0,0,False)
            colorPattern='gradient'
        elif themeSeed > themeProbs['rainbow']:
            colors=((0.9,0,0),(0.9,0.4,0),(0.95,0.9,0.05),(0.2,0.95,0.2),(0.2,0.2,0.95),(.55,.2,1),(0.9,0,0),(0.9,0.4,0),(0.95,0.9,0.05),(0.2,0.95,0.2),(0.2,0.2,0.95),(.55,.2,1),(0.9,0,0),(0.9,0.4,0),(0.95,0.9,0.05),(0.2,0.95,0.2),(0.2,0.2,0.95),(.55,.2,1),(0.9,0,0))
            backgroundColor = 'opposite'
            filter=(1,0,False)
            colorPattern='gradient'
        elif themeSeed > themeProbs['diamond']:
            texture = '1.png'
            colors=((1,1,1),(1,1,1))
            backgroundColor = (0.8,0.8,1)
            filter=(1,0,False)
            colorPattern='gradient'
        elif themeSeed > themeProbs['red_blue']:
            colors=((1,0,0),(0,0,1),(1,0,0),(0,0,1),(1,0,0),(0,0,1),(1,0,0),(0,0,1),(1,0,0))
            backgroundColor=(0.87,0.83,0.87)
            filter=(1,0,True)
            colorPattern='gradient'
        elif themeSeed > themeProbs['galaxy']:
            colors=((1,0,0),(0,0,1))
            backgroundColor=(0.95,0.95,0.95)
            filter=(1,0,True)
            colorPattern='gradient'
            postProcess='galaxy.png'
        elif themeSeed > themeProbs['peacock']:
            colors=((1,0,0),(0,0,1))
            backgroundColor=(0.95,0.95,0.95)
            filter=(1,0,True)
            colorPattern='gradient'
            postProcess='starrynight.jfif'
        elif themeSeed > themeProbs['alien_candy']:
            colors=((1,0,0),(0,0,1))
            backgroundColor=(0.95,0.95,0.95)
            filter=(1,0,False)
            colorPattern='gradient'
            postProcess='spiral.jpg'

    modelProbs = {
        'monkey' : 0.99,
        'shard' : 0.95,
        'icosahedron' : 0.5,
        'cube' : 0
    }
    #MODEL SELECTION
    modelSeed = random()
    if modelSeed > modelProbs['monkey']:
        sizeNormalizer = 8
        scaleMod = (1,1,1)
        modelType = 'monkey.egg'
    elif modelSeed > modelProbs['shard']:
        sizeNormalizer = 2
        scaleMod = (3,0.5,0.5)
        modelType = 'Icosahedron.egg'
    elif  modelSeed > modelProbs['icosahedron']:
        sizeNormalizer = 2
        scaleMod = (1,1,1)
        modelType = 'Icosahedron.egg'
    elif modelSeed > modelProbs['cube']:
        sizeNormalizer = 4.5
        scaleMod = (1,1,1)
        modelType = 'box.egg'
        rotateModel=False

    snakeProbs = {
        '5' : 0.99,
        '4' : 0.92,
        '3' : 0.8,
        '2' : 0.5,
        '1' : 0
    }
    #NUMBER OF MEGARMS, S, SIZES
    snakeSeed = random()
    if snakeSeed > snakeProbs['5']:
        numSnakes=5
        sizeMod = 1.6
        numNodes = 120
    elif snakeSeed > snakeProbs['4']:
        numSnakes=4
        sizeMod = 1.7
        numNodes = 110
    elif snakeSeed > snakeProbs['3']:
        numSnakes=3
        sizeMod = 1.9
        numNodes = 90
    elif snakeSeed > snakeProbs['2']:
        sizeMod = 2
        numNodes = 80
        numSnakes=2
    elif snakeSeed > snakeProbs['1']:
        sizeMod = 2.3
        numNodes = 50
        numSnakes=1

    modelScale = (sizeMod * sizeNormalizer * scaleMod[0], sizeMod * sizeNormalizer * scaleMod[1], sizeMod * sizeNormalizer * scaleMod[2])

    speedProbs = {
        'hyper' : 0.99,
        'quick' : 0.6,
        'normal' : 0
    }
    #JOINT SPEED RANGE
    speedSeed = random()
    if speedSeed > speedProbs['hyper']: #SPARKLES
        jointSpeedRange = (20,40)
        modelSpin = 0
    elif speedSeed > speedProbs['quick']:
        jointSpeedRange = (3,6)
        modelSpin = 2
    elif speedSeed > speedProbs['normal']:
        jointSpeedRange = (2,3)
        modelSpin = 3.5
    lengthRange = (0,20)

    #BASE SPEED RANGE
    if speedSeed > speedProbs['hyper']: #SPARKLES
        baseSpeedRange = (20,40)
        modelSpin = 0
    elif speedSeed > speedProbs['quick']:
        baseSpeedRange = (3,6)
        modelSpin = 2
    elif speedSeed > speedProbs['normal']:
        baseSpeedRange = (1.5,3)
        modelSpin = 3.5
    lengthRange = (0,20)

    transparency = True

    #CAMERA SPINNING
    spinSeed = random()
    if spinSeed > 1:
        spinSpeed = randint(6,15)
    elif spinSeed > 1:
        spinSpeed = randint(2,5)
    else:
        spinSpeed = random()+1
        #none, zebra, multi
    if random() > 0.5:
        spinSpeed*-1

    #TEXTURES
    backgroundImage = None #BACKGROUND IMAGES DONT WORK WITH FILTERING ON


    mirrorProb = 0.8
    if random() > mirrorProb: #I WANT DOUBLE MIRRORS
        mirror = True #7
    else:
        mirror = False

    shapeProbs = {
        'wire_snake' : 0.8,
        'wire' : 0.8,
        'snake' : 0
    }
    shapeSeed = random()
    if shapeSeed > shapeProbs['wire_snake'] and numSnakes>1:
        drawWireframe = True
        drawSnakes = True
    elif shapeSeed > shapeProbs['wire'] and numSnakes>2:
        drawWireframe = True
        drawSnakes = False
    elif shapeSeed > shapeProbs['snake']:
        drawWireframe = False
        drawSnakes = True

    #STICKERGEN
    stickerProbs = {
        '3' : 0.9995,
        '2' : 0.995,
        '1' : 0.95,
        '0' : 0
    }
    stickerSeed = random()
    if stickerSeed > stickerProbs['3']:
        stickers = 3
    elif stickerSeed > stickerProbs['2']:
        stickers = 2
    elif stickerSeed > stickerProbs['1']:
        stickers = 1
    else:
        stickers = 0

    prop={
        'num_snakes' : numSnakes,
        'color_pattern' : colorPattern,
        'base_speed_range' : baseSpeedRange,
        'joint_speed_range' : jointSpeedRange,
        'model_scale' : modelScale,
        'num_nodes' : numNodes,
        'num_wireframes' : 50,
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
        'model_spin' : modelSpin,
        'filter' : filter,
        'rotate_model' : rotateModel,
        'post_process' : postProcess,
        'lights' : lights
    }
    return prop
