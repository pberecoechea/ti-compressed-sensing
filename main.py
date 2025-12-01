import src.image_processing as imgp
from matplotlib.image import imread
from matplotlib.image import imsave
import os

__author__ = "BERECOECHEA Pablo, PLAUT-AUBRY Baptiste, JAULIN Gautier"
__copyright__ = "CYTech 2025, ING3 HPDA"

def main():
    """
    Le main effectue les étapes suivantes :
    1. Charge une image définie (définie par image_index)
    2. Découpe l'image en vecteurs (N patchs)
    3. Recréé l'image à partir des vecteurs
    4. Sauvegarde le résultat pour vérification
    """



    #1.Ouverture d'une image choisie arbitrairement pour tester le pré-traitement
    image_index = 30
    #Récupération de toutes les images du dossier
    imgs_nms = list(os.listdir("Data"))
    image = imread("Data/"+imgs_nms[image_index])

    #Affichage des informations liées à l'image
    print(f"\nOpening image : {imgs_nms[image_index]}.")
    print(f"Taille : {image.shape}")

    #2.Découpage de l'image en n blocs (patchs)
    print("\nTransforming image to vectors...")
    vectors = imgp.image_to_vec(image)

    #3.Recréation de l'image à partir des n blocs (patch)
    print("Transforming vectors to image...")
    img_bis = imgp.vec_to_image(vectors)

    #4.Sauvegarde de l'image recréée 
    print("\nSaving image !")
    imsave("test.jpg",img_bis)


if __name__ == "__main__":
    main()