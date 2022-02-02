import glob
from PIL import Image

def make_gif(path_to_images):
    frames = [Image.open(image) for image in sorted(glob.glob(f"{path_to_images}*.png"))]
    frame_one = frames[0]
    save_as = "{}_animation.gif".format(path_to_images)
    frame_one.save(save_as, format="GIF", append_images=frames,
                   save_all=True, duration=100, loop=0)
    print("Gif saved as {}".format(save_as))
