import src.image_processing as imgp
from matplotlib.image import imread
from matplotlib.image import imsave
import scipy.signal as scs
import numpy as np
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
    ratio = 0.2
    
    #Récupération de toutes les images du dossier
    imgs_nms = list(os.listdir("Data"))
    phi = imgp.phi("gaussienne",ratio)

    for i in range(0,len(imgs_nms)):
        image = imread("Data/"+imgs_nms[29])
        gray = imgp.to_gray(image)
        vects = imgp.image_to_vec(gray)
        ys = imgp.get_ys_with_ratio_with_phi(vects,phi)

        x = imgp.iterative_bcl_spl(phi,ys)

        print("\nSaving image !")
        new = np.stack([x, x, x], axis = -1)
        imsave("test.jpg",new)   

        old = np.stack([gray, gray, gray], axis = -1)
        imsave("og.jpg",old) 
        break

        """
        print("\nSaving image !")
        new = np.stack([x, x, x], axis = -1)
        imsave("test.jpg",new)    
        break
        if(not os.path.isdir("lighter_pictures")):
            os.mkdir("lighter_pictures")
        np.savetxt("lighter_pictures/"+imgs_nms[i]+".txt",ys,fmt="%d")
        """
    #np.savetxt("lighter_pictures/_phi.txt",phi)


    print("\n",phi)

    """
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
    """

if __name__ == "__main__":
    main()

