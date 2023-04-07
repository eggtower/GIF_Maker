import os
import pathlib
import shutil
import numpy as np
import cv2
from PIL import Image, ImageEnhance

def make_gif(clipPath, savePath, q):
    frameList = list()
    
    clip = cv2.VideoCapture(clipPath)
    fps = clip.get(5)
    width, height = clip.get(3), clip.get(4)
    reSize = (int(width/height*450), 450) # reshape, fixed height 450
    
    # for i in range(frames):
    frameCnt = 0
    while clip.isOpened():
        ret, frame = clip.read()
        if not ret: break
            
        if frameCnt%q==0:
            frame = cv2.resize(frame, reSize)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
            # Convert to a format that PIL can handle
            frame = Image.fromarray(np.uint8(frame))
            frame = ImageEnhance.Brightness(frame).enhance(1.006)
            frame = ImageEnhance.Color(frame).enhance(1.158)
            
            frameList.append(frame)
        frameCnt+=1
    clip.release()
    frameList[0].save(savePath, format="GIF", append_images=frameList[1:],
                      save_all=True, duration=1000/fps*q, loop=0, disposal=2)
                      
def main():
    if not os.path.exists('clips'):
        print("There is no 'clips' folder")
        return
    if os.path.exists('GIF'): shutil.rmtree("GIF")
    try:
        os.mkdir('GIF')
    except IOError:
        print("Error occurred creating output folder")
        return
    currPath = pathlib.Path().absolute()
    clipsDir = os.path.join(currPath, 'clips')
    saveDir = os.path.join(currPath, 'GIF')
    
    inputDate = input('Enter date: ')
    
    files = os.listdir(clipsDir)
    cnt = 1
    for file in files:
        if not file.endswith('.mp4'): continue
        print('Processing..', file)
        clipPath = os.path.join(clipsDir, file)
        savePath = '{0}/{1}_{2}.gif'.format(saveDir, inputDate, cnt)
        make_gif(clipPath, savePath, 1)
        cnt += 1
    cv2.destroyAllWindows()
    input('Press any key to end.')
    
if __name__ == "__main__":
    main()