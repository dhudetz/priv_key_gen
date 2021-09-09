import imageio

def generateGif(genNumber, numFrames):
    # filenames=[None] * (numFrames*2)
    # for i in range(1,numFrames+1):
    #     tempLoc = 'images/'+str(genNumber)+'/'+str(i)+'.png'
    #     filenames[i-1] = tempLoc
    #     filenames[(numFrames*2)-i] = tempLoc
    filenames=[]
    for i in range(20, numFrames+1):
        filenames.append('images/'+str(genNumber)+'/'+str(i)+'.png')
    for i in range(numFrames, 21, -1):
        filenames.append('images/'+str(genNumber)+'/'+str(i)+'.png')
    with imageio.get_writer(str(genNumber)+'.gif', mode='I',duration=(1/60)) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
# 
# for i in range(0,10):
#     generateGif(i, 200)
