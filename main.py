import src.image_processing as imgp
from matplotlib.image import imread
from matplotlib.image import imsave
import os

def main():
    i = 30
    imgs_nms = list(os.listdir("Data"))
    image = imread("Data/"+imgs_nms[i])

    print(f"\nOpening image : {imgs_nms[i]}.")
    print(f"Taille : {image.shape}")

    print("\nTransforming image to vectors...")
    vectors = imgp.image_to_vec(image)

    print("Transforming vectors to image...")
    img_bis = imgp.vec_to_image(vectors)

    print("\nSaving image !")
    imsave("test.jpg",img_bis)


if __name__ == "__main__":
    main()