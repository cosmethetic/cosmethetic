import os
import cv2
import numpy as np
import time
import threading

from CPM.makeup import Makeup
from CPM.parser import get_args
from PIL import Image



class TryOnModel:
    model = None
    
    def __init__(self) -> None:
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        print('CUDA_VISIBLE_DEVICES', os.environ['CUDA_VISIBLE_DEVICES'])
        
        self.model = self._load_CPM_model()
        
        # alias func
        self.bsn = os.path.basename
        

    def _load_CPM_model(self):
        if TryOnModel.model == None:
            args = get_args(["--style", '', '--input', '', '--savedir', '', '--filename', ''])
            t1 = time.perf_counter()
            TryOnModel.model = Makeup(args)
            t2 = time.perf_counter()
            print(f'model loading time: {1000*(t2-t1):.4f}ms')
         
        return TryOnModel.model

    def _color_makeup(self, model,A_txt, B_txt, alpha):
        color_txt = model.makeup(A_txt, B_txt)
        color = model.render_texture(color_txt)
        color = model.blend_imgs(model.face, color * 255, alpha=alpha)
        return color

    def _pattern_makeup(self, model, A_txt, B_txt, render_texture=False):
        mask = model.get_mask(B_txt)
        mask = (mask > 0.0001).astype("uint8")
        pattern_txt = A_txt * (1 - mask)[:, :, np.newaxis] + B_txt * mask[:, :, np.newaxis]
        pattern = model.render_texture(pattern_txt)
        pattern = model.blend_imgs(model.face, pattern, alpha=1)
        return pattern

    def get_textureA(self, imgA):
        self.model.prn_process(imgA)
        A_txt = self.model.get_texture()
        return A_txt
    
    def get_textureB(self, imgB):
        B_txt = self.model.prn_process_target(imgB)
        return B_txt

    def _get_makeup(self, A_txt, B_txt, args):
        t1 = time.perf_counter()
        if args.color_only:
            output = self._color_makeup(self.model, A_txt, B_txt, args.alpha)
        elif args.pattern_only:
            output = self._pattern_makeup(self.model, A_txt, B_txt)
        else:
            color_txt = self.model.makeup(A_txt, B_txt) * 255
            mask = self.model.get_mask(B_txt)
            mask = (mask > 0.001).astype("uint8")
            new_txt = color_txt * (1 - mask)[:, :, np.newaxis] + B_txt * mask[:, :, np.newaxis]
            output = self.model.render_texture(new_txt)
            output = self.model.blend_imgs(self.model.face, output, alpha=1)
        t2 = time.perf_counter()
        print(f'inference time: {1000*(t2-t1):.4f}ms')
        return output
        
    def execute(self, style_path, input_path, save_dir, file_name):
        args = get_args([
            '--style', style_path, 
            '--input', input_path, 
            '--savedir', save_dir, 
            '--filename', file_name])
        
        imgA = np.array(Image.open(input_path))
        imgB = np.array(Image.open(style_path))
        imgB = cv2.resize(imgB, (256, 256))

        # Check whether textures of input_path, style_path images exists
        # textures are stored at /CPM/imgs/textures <- it should be changed to 'static' path
        
        # for A
        txt_path_A = os.path.join("CPM", "imgs", "textures", self.bsn(input_path))
        if os.path.isfile(txt_path_A): 
            A_txt = np.array(Image.open(txt_path_A))
        else: 
            raise FileNotFoundError("Input image is not prepared please wait 10seconds")
        
        # for B
        txt_path_B = os.path.join("CPM", "imgs", "textures", self.bsn(style_path))
        if os.path.isfile(txt_path_B): 
            B_txt = np.array(Image.open(txt_path_B))
        else: 
            raise FileNotFoundError("Input image is not prepared please wait 10seconds")
            
        output = self._get_makeup(A_txt, B_txt, args)
        
        # Restore its original size
        H, W, C = imgA.shape
        output = cv2.resize(output, (W, H))

        # x2, y2, x1, y1 = model.location_to_crop()
        # output = np.concatenate([imgB[x2:], model.face[x2:], output[x2:]], axis=1)

        save_path = save_dir + file_name

        Image.fromarray((output).astype("uint8")).save(save_path)

        save_path = "저장 완료"

        print("Completed 👍 Please check result in: {}".format(save_path))

class TexturePreprocessingThread(threading.Thread):
    def __init__(self, img_path, type):
        """_summary_
        Args:
            type (string): "A" or "B". "A" means profile image, "B" means makeup style image
        """
        self.type = type
        self.img_path = os.path.join("CPM", "imgs", img_path)
        self.model = TryOnModel()
        self.bsn = os.path.basename
        super().__init__()

    def run(self):
        print(f"preprocessing start: {self.img_path}")
        img = np.array(Image.open(self.img_path))
        if self.type == "A":
            # Need to refactor. path is hard coded
            txt_path_A = os.path.join("CPM", "imgs", "textures", self.bsn(self.img_path))
            A_txt = self.model.get_textureA(img)
            Image.fromarray(A_txt).save(txt_path_A)
        elif self.type == "B":
            # Need to refactor. path is hard coded
            txt_path_B = os.path.join("CPM", "imgs", "textures", self.bsn(self.img_path))
            B_txt = self.model.get_textureB(img)
            Image.fromarray(B_txt).save(txt_path_B)  
        else:
            raise RuntimeError(f"type: {self.type}. type must be A or B.")
        
