import os
from parser import get_args

import cv2
import numpy as np
from makeup import Makeup
from PIL import Image
import glob


def color_makeup(A_txt, B_txt, alpha):
    color_txt = model.makeup(A_txt, B_txt)
    color = model.render_texture(color_txt)
    color = model.blend_imgs(model.face, color * 255, alpha=alpha)
    return color


def pattern_makeup(A_txt, B_txt, render_texture=False):
    mask = model.get_mask(B_txt)
    mask = (mask > 0.0001).astype("uint8")
    pattern_txt = A_txt * (1 - mask)[:, :, np.newaxis] + B_txt * mask[:, :, np.newaxis]
    pattern = model.render_texture(pattern_txt)
    pattern = model.blend_imgs(model.face, pattern, alpha=1)
    return pattern


if __name__ == "__main__":

    os.environ["CUDA_VISIBLE_DEVICES"]="0"
    args = get_args()
    model = Makeup(args)

    if not os.path.exists(args.savedir):
        os.mkdir(args.savedir)

    imgA = np.array(Image.open(args.input))
    
    print("got imgA!")

    model.prn_process(imgA)
    A_txt = model.get_texture()

    imgBs = [f.replace("\\", "/") for f in glob.glob(os.path.join(args.style_dir, "*"))]
    for style in imgBs:
        try:
            imgB = np.array(Image.open(style))
            imgB = cv2.resize(imgB, (256, 256))

            B_txt = model.prn_process_target(imgB)

            if args.color_only:
                output = color_makeup(A_txt, B_txt, args.alpha)
            elif args.pattern_only:
                output = pattern_makeup(A_txt, B_txt)
            else:
                color_txt = model.makeup(A_txt, B_txt) * 255
                mask = model.get_mask(B_txt)
                mask = (mask > 0.001).astype("uint8")
                new_txt = color_txt * (1 - mask)[:, :, np.newaxis] + B_txt * mask[:, :, np.newaxis]
                output = model.render_texture(new_txt)
                output = model.blend_imgs(model.face, output, alpha=1)

            save_path = os.path.join(args.savedir, os.path.basename(style))

            Image.fromarray((output).astype("uint8")).save(save_path)
            print(save_path, "saved")
        except:
            continue

