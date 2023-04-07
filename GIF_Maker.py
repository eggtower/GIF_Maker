import os
import pathlib
import shutil
import numpy as np
import cv2
from PIL import Image

def make_gif(clipPath, savePath):
    frameList = list()
    
    clip = cv2.VideoCapture(clipPath)
    fps = clip.get(5) # 影片 fps
    frames = int(clip.get(cv2.CAP_PROP_FRAME_COUNT)) # 影片總幀數
    width, height = clip.get(3), clip.get(4) # 影片寬度,高度
    reSize = (int(width/height*450), 450) # 調整大小, 高固定 450
    
    for i in range(frames):
        ret, frame = clip.read()
        if not ret: break
            
        if i%4==0:
            frame = cv2.resize(frame, reSize)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGBA)
            # 圖像增強
            frame = 255*np.power(frame/255, 1.136)
            frame = np.around(frame)
            frame[frame>255] = 255
            frame = frame.astype(np.uint8)
            
            frame = Image.fromarray(frame)
            frame = frame.convert('RGB') 
            frameList.append(frame)
    clip.release()
    frameList[0].save(savePath, format="GIF", append_images=frameList[1:],
                      save_all=True, duration=fps/4, loop=0, disposal=2)
                      
def main():
    if not os.path.exists('clips'):
        print("There is no 'clips' folder")

    if os.path.exists('GIF'): shutil.rmtree("GIF")
    try:
        os.mkdir('GIF')
    except IOError:
        print("Error occurred creating output folder")
    #         return
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
        make_gif(clipPath, savePath)
        cnt += 1
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()