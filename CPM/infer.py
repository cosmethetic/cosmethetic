import os

from CPM.parser import get_args

import cv2
import numpy as np
from CPM.makeup import Makeup
from PIL import Image

import time
import argparse


class TryOnModel:
    model = None
    
    def __init__(self) -> None:
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        print('CUDA_VISIBLE_DEVICES', os.environ['CUDA_VISIBLE_DEVICES'])
        
        self.model = self._load_CPM_model()

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

    def _get_textureAB(self, imgA, imgB):
        t1 = time.perf_counter()
        self.model.prn_process(imgA)
        A_txt = self.model.get_texture()
        B_txt = self.model.prn_process_target(imgB)
        t2 = time.perf_counter()
        print(f'preprocessing time: {1000*(t2-t1):.4f}ms')
        return A_txt, B_txt
       
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

        A_txt, B_txt = self._get_textureAB(imgA, imgB)
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
