import sys, os, glob
from PIL import Image

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 {} folder".format(__file__))
        sys.exit(0)

    folder = sys.argv[1]

    if not os.path.isdir(folder):
        print("{} is not a dir...".format(folder))
        sys.exit(1)    

    print("Initializing size processing on images from folder {}.".format(folder))
    sizes = []
    for imagefile in glob.glob(os.path.join(folder, "*.*")):
        image = Image.open(imagefile)
        sizes.append(image.size)
        image.close()

    sizes = sorted(sizes)
    
    n = len(sizes)
    i = 0
    while i < n:
        count = 1
        while i + 1 < n and sizes[i] == sizes[i + 1]:
            count += 1
            i += 1
        print(sizes[i], count)
        i += 1
