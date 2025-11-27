from matplotlib.image import imread
import numpy as np
import src.constants as cs
import os

#print(f"Nombre d'images à traiter : {len(images_noms)}\n")

def verif_taille(liste_noms_imgs: list[str]) -> bool:
    taille_correcte = True
    for nom in liste_noms_imgs:
        image = imread(cs.PATH + nom)
        if(image.shape[0] != cs.HAUTEUR or image.shape[1] != cs.LARGEUR):
            taille_correcte = False
            print(f"Taille anormale : [ {image.shape[0]} x {image.shape[1]} ]")
    return taille_correcte

def image_to_vec(image : np.ndarray) -> list:
    vector_list = []
    for cell_x in range(0,cs.HAUTEUR,cs.N):
        for cell_y in range(0,cs.LARGEUR,cs.N):
            cell_rgb_list = []
            for pixel_x in range(cell_x,cell_x+cs.N):
                for pixel_y in range(cell_y,cell_y+cs.N):
                    #print(image[pixel_x][pixel_y])
                    cell_rgb_list.append(image[pixel_x][pixel_y])
            vector_list.append(np.array(cell_rgb_list))
    return vector_list


def vec_to_image (vectors : list) -> np.ndarray:
    image = np.ndarray(shape=(cs.HAUTEUR,cs.LARGEUR,3),dtype=np.uint8)
    for i in range(0,cs.HAUTEUR):
        for j in range(0,cs.LARGEUR):
            v_nb = (j // cs.N) + ((i // cs.N) * (528 // 11))
            px_nb = (j % cs.N) + ((i * cs.N) % (cs.N**2))
            for k in range(0,3):
                image[i][j][k] = vectors[v_nb][px_nb][k]

    return image




#print(f"Ouverture : {nom}")
#print(f"Taille : [ {image.shape[0]} x {image.shape[1]} ]")