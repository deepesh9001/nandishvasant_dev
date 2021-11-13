from collections import Counter
from typing import Collection
import cv2
import json


class SizeMesurment :


    def getCount(list,total,val):
        countsize=0
        for j in range(total):
            if(list[j]==val):
                countsize +=1
        return countsize

    def getSize():
        finaldata= []
        data=[]
        countArr=[]


        thresh1=120
        thresh2=255

        im = cv2.imread("images1/12.png",0)
        im = 255-im
        im = cv2.resize(im,(600,600))

        im2=cv2.Canny(im,thresh1-100,thresh2)

        ret, thresh = cv2.threshold(im2, thresh1, thresh2, 0)
        contours, _ = cv2.findContours(thresh, 1, 2)

        im=cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)

        cv2.drawContours(im,contours,-1,color=(0,255,0),thickness=1)

        # cv2.imshow("Image",im)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        totalContors = len(contours)
        print("Total",totalContors,"grains found")

        print("Area:")
        for i in range(totalContors):
            # size=cv2.contourArea(contours[i])
            # print(size)
            data.append(cv2.contourArea(contours[i]))
            # data[i]=size
            # print("[",i,"]",cv2.contourArea(contours[i]))

        # exit()
        countsize=0   

        # print(totalContors)

        for k in range(totalContors):
            # for j in range(totalContors):
            #     if(data[j]==cv2.contourArea(contours[k])):
            #         countsize +=1
            # print(countsize)
            finalDictionary={
                "count" : SizeMesurment.getCount(data,totalContors,cv2.contourArea(contours[k])),
                "size" : cv2.contourArea(contours[k])
            }
            # print(finalDictionary)
            finaldata.append(finalDictionary)
            countsize=0   

        json_data=json.dumps(finaldata, indent = 4)

        return json_data

        # print(json.dumps(finaldata, indent = 4))

    