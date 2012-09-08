# Collection of functions for building Alighiero Boetti style pixel progressions
# Alternando da uno a cento e viceversa (Alternating from one to one hundred and vice versa)
# http://www.moma.org/interactives/exhibitions/2012/boetti
# by Conor Lawless http://lwlss.net

import numpy, random, math
from PIL import Image

def randomPositions(I,J,pixels):
    '''Randomly place the appropriate number of pixels, all allowed to have different locations in each frame'''
    N=pixels.shape[0]
    # Possible locations within a single pixel array
    pixpop=[[x,y] for x in xrange(0,N) for y in xrange(0,N)]
    return(random.sample(pixpop,I*N+J))

def randomProgress(I,J,pixels):
    '''Place the next pixel in sequence randomly, maintaining position of previous pixels'''
    N=pixels.shape[0]
    # If we're at panel 1, generate a random coordinate
    if (I,J)==(0,0):
        return([])
    if I==0 and J==1:
        return([[random.randint(0,N-1),random.randint(0,N-1)]])
    # If not, analyse previous panel
    if(J==0):
        Iold,Jold=I-1,N-1
    else:
        Iold,Jold=I,J-1
    if Jold%2==0:
        bground=0
    else:
        bground=1
    fground=1-bground
    empty=[[x,y] for x in xrange(0,N) for y in xrange(0,N) if pixels[Iold,Jold,x,y]==bground]
    full=[[x,y] for x in xrange(0,N) for y in xrange(0,N) if pixels[Iold,Jold,x,y]==fground]
    newpix=random.randint(0,len(empty)-1)
    full.append(empty[newpix])
    return(full)

def nearest(I,J,pixels):
    '''Place next pixel as close to positions in previous panel as possible'''
    N=pixels.shape[0]
    # If we're at panel 1, generate a random coordinate
    if (I,J)==(0,0):
        return([])
    if I==0 and J==1:
        return([[random.randint(0,N-1),random.randint(0,N-1)]])
    # If not, analyse previous panel
    if(J==0):
        Iold,Jold=I-1,N-1
    else:
        Iold,Jold=I,J-1
    if Jold%2==0:
        bground=0
    else:
        bground=1
    fground=1-bground
    empty=[[x,y] for x in xrange(0,N) for y in xrange(0,N) if pixels[Iold,Jold,x,y]==bground]
    full=[[x,y] for x in xrange(0,N) for y in xrange(0,N) if pixels[Iold,Jold,x,y]==fground]
    # Get distances between empty and full pixels
    dmat=numpy.absolute(distances(numpy.array(empty),numpy.array(full)))
    dsum=sum(dmat.T)
    # For each empty pixel, sum distances between it and all full pixels
    farthest=min(xrange(len(dsum)),key=dsum.__getitem__)
    full.append(empty[farthest])
    return(full)

def distances(xy1, xy2):
    '''Return matrix of distances between points in xy1 and each of points xy2'''
    d0 = numpy.subtract.outer(xy1[:,0], xy2[:,0])
    d1 = numpy.subtract.outer(xy1[:,1], xy2[:,1])
    return numpy.hypot(d0, d1)

def generatePixels(N,progression="randomProgress"):
    '''Master function which builds Boetti pixels'''
    # Master array of pixel arrays
    pixels=numpy.zeros((N,N,N,N),numpy.uint8)
    for I in xrange(0,N):
        for J in xrange(0,N):
            if J%2==0:
                bground=0
            else:
                bground=1
            fground=1-bground
            pixels[I,J]=bground
            #points=randomProgress(I,J,pixels)
            points=globals()[progression](I,J,pixels)
            for p in points:
                pixels[I,J,p[0],p[1]]=fground
    return(pixels)

def makeImage(pixels,border,N,approximw,bordercol=227):
    '''Converts Boetti array into an array of RGB image pixels with border'''
    # Add border
    fpix=numpy.zeros((border+N*(N+border),border+N*(N+border)),numpy.uint8)
    fpix=fpix+bordercol
    for I in xrange(0,N):
        for J in xrange(0,N):
            for i in xrange(0,N):
                for j in xrange(0,N):
                    fpix[border+I*(N+border)+i,border+J*(N+border)+j]=pixels[I,J,i,j]*255
    im=Image.fromarray(fpix,"L")
    # Find a nice integer multiple of fpix width to resize image
    actw=border+(N+border)*N
    if actw>=approximw:
        scl=round(float(actw)/float(approximw))
        imw=int(actw/scl)
    else:
        scl=round(float(approximw)/float(actw))
        imw=int(actw*scl)

    im=im.resize((imw,imw))
    return(im)

def generateImage(N=10,border=1,approximw=800,bordercol=227,progression="randomProgress"):
    '''Wrapper function which builds array and makes image'''
    pixels=generatePixels(N,progression)
    im=makeImage(pixels,border,N,approximw,bordercol)
    return(im)

if __name__ == '__main__':
    for x in xrange(0,50):
        finim=generateImage(6,progression="randomProgress")
        finim.save("TwitterRandomProgress%03d.png"%x)
        finim=generateImage(6,progression="randomPositions")
        finim.save("TwitterRandomPositions%03d.png"%x)
        
