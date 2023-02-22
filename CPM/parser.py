import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint_pattern", default="/home/hbk/media/temp/cosmethetic/CPM/checkpoints/pattern.pth", type=str)
    parser.add_argument("--checkpoint_color", default="/home/hbk/media/temp/cosmethetic/CPM/checkpoints/color.pth", type=str)
    parser.add_argument("--device", default="cuda", type=str)
    parser.add_argument('--batch_size', default = '1', type = int)
    parser.add_argument("--prn", default=True, type=bool)
    parser.add_argument("--color_only", default=False, action="store_true")
    parser.add_argument("--pattern_only", default=False, action="store_true")

    parser.add_argument(
        "--input",
        type=str,
        default="/home/hbk/media/temp/cosmethetic/CPM/imgs/non-makeup.png",
        help="Path to input image (non-makeup)",
    )
    parser.add_argument(
        "--style_dir",
        type=str,
        default="/home/hbk/media/temp/cosmethetic/CPM/imgs/reference",
        help="Path to style image (makeup style | reference image)",
    )
    parser.add_argument("--alpha", type=float, default=0.5, help="opacity of color makeup")
    parser.add_argument("--savedir", type=str, default="/home/hbk/media/temp/cosmethetic/CPM/infer_results")

    args = parser.parse_args()

    print("           ⊱ ──────ஓ๑♡๑ஓ ────── ⊰")
    print("🎵 hhey, arguments are here if you need to check 🎵")
    for arg in vars(args):
        print("{:>15}: {:>30}".format(str(arg), str(getattr(args, arg))))
    print()
    return args


if __name__ == "__main__":
    get_args()
