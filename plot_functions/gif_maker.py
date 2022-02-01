import glob
from PIL import Image
def make_gif(path_to_images):
    frames = [Image.open(image) for image in sorted(glob.glob(f"{path_to_images}*.png"))]
    frame_one = frames[0]
    frame_one.save("{}_animation.gif".format(path_to_images), format="GIF", append_images=frames,
               save_all=True, duration=100, loop=0)
    
