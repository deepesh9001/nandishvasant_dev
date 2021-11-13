from cv2 import imread, morphologyEx
from skimage import data, io, filters, feature
import numpy as np
import matplotlib.pyplot as plt
# Label image regions.
from skimage.measure import regionprops
import matplotlib.patches as mpatches
from skimage.morphology import label


imgPath = 'Images1/13.jpg'
image = imread(imgPath,0)# data.coins()  # or any NumPy array!
#remove the 2 um scake
image = image[:800,:] #for 1st image
#Whoe image
io.imshow(image)

edges_sob = filters.sobel(image)
io.imshow(edges_sob)


edgeTh = 0.01
edges_sob_filtered = np.where(edges_sob>edgeTh,255,0)
io.imshow(edges_sob_filtered)

label_image = label(edges_sob_filtered)
fig,ax = plt.subplots(1,figsize=(20,10))
ax.imshow(image, cmap=plt.cm.gray)
ax.set_title('Labeled items', fontsize=24)
ax.axis('off')

#Do not plot regions smaller than sizeThLow pixels and larger than sizeThHi on each axis
sizeThLow=15
sizeThHi =100

for region in regionprops(label_image):
    # Draw rectangle around segmented coins.
    if ((region.bbox[2]-region.bbox[0])>sizeThLow and (region.bbox[3] - region.bbox[1])>sizeThLow):
        if ((region.bbox[2]-region.bbox[0])<sizeThHi and (region.bbox[3] - region.bbox[1])<sizeThHi):
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr),
                                      maxc - minc,
                                      maxr - minr,
                                      fill=False,
                                      edgecolor='red',
                                      linewidth=2)
            ax.add_patch(rect)
        
#Sort all found shapes by region size
sortRegions = [[(region.bbox[2]-region.bbox[0]) * (region.bbox[3] - region.bbox[1]),region.bbox] 
                for region in regionprops(label_image) if
                (((region.bbox[2]-region.bbox[0])>sizeThLow) and (region.bbox[3] - region.bbox[1])>sizeThLow and ((region.bbox[2]-region.bbox[0])<sizeThHi and (region.bbox[3] - region.bbox[1])<sizeThHi))]
sortRegions = sorted(sortRegions, reverse=False)

#Check particle sizes distribution
particleSize = [size[0] for size in sortRegions]

# Insert a um to pixel conversion ratio
um2pxratio = 1 #This number can directly be evaluated based on the zoom value of the microscope

print("Total number of particles detected: " + str(len(sortRegions)))

#Show histogram of non-sero Sobel edges
plt.figure()
plt.plot(np.multiply(np.power(um2pxratio,2), particleSize),np.arange(1,len(particleSize)+1),linewidth=2)
plt.ylabel('Particle count',fontsize=14)
plt.xlabel('Particle area',fontsize=14)
plt.title("Particle area cummulative distribution",fontsize=16)
    
#Show 5 largest regions location, image and edge
for region in sortRegions[-5:]:
    # Draw rectangle around segmented coins.
    minr, minc, maxr, maxc = region[1]
    fig, ax = plt.subplots(1,3,figsize=(15,6))
    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].set_title('full frame', fontsize=16)
    ax[0].axis('off')
    rect = mpatches.Rectangle((minc, minr),
                          maxc - minc,
                          maxr - minr,
                          fill=False,
                          edgecolor='red',
                          linewidth=2)
    ax[0].add_patch(rect)

    ax[1].imshow(image[minr:maxr,minc:maxc],cmap='gray')
    ax[1].set_title('Zoom view', fontsize=16)
    ax[1].axis("off")
    ax[1].plot([0.1*(maxc - minc), 0.3*(maxc - minc)],
             [0.9*(maxr - minr),0.9*(maxr - minr)],'r')
    ax[1].text(0.15*(maxc - minc), 0.87*(maxr - minr),
          str(round(0.2*(maxc - minc)*um2pxratio,1))+'um',
          color='red', fontsize=12, horizontalalignment='center')

    ax[2].imshow(edges_sob_filtered[minr:maxr,minc:maxc],cmap='gray')
    ax[2].set_title('Edge view', fontsize=16)
    ax[2].axis("off")
    plt.show()

#Show 5 smallest regions location, image and edge
for region in sortRegions[:5]:
    # Draw rectangle around segmented coins.
    minr, minc, maxr, maxc = region[1]
    fig, ax = plt.subplots(1,3,figsize=(15,6))
    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].set_title('full frame', fontsize=16)
    ax[0].axis('off')
    rect = mpatches.Rectangle((minc, minr),
                          maxc - minc,
                          maxr - minr,
                          fill=False,
                          edgecolor='red',
                          linewidth=2)
    ax[0].add_patch(rect)

    ax[1].imshow(image[minr:maxr,minc:maxc],cmap='gray')
    ax[1].set_title('Zoom view', fontsize=16)
    ax[1].axis("off")
    ax[1].plot([0.1*(maxc - minc), 0.3*(maxc - minc)],
             [0.9*(maxr - minr),0.9*(maxr - minr)],'r')
    ax[1].text(0.15*(maxc - minc), 0.87*(maxr - minr),
          str(round(0.2*(maxc - minc)*um2pxratio,1))+'um',
          color='red', fontsize=12, horizontalalignment='center')

    ax[2].imshow(edges_sob_filtered[minr:maxr,minc:maxc],cmap='gray')
    ax[2].set_title('Edge view', fontsize=16)
    ax[2].axis("off")
    plt.show()