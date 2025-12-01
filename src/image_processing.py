from matplotlib.image import imread
import numpy as np
import src.constants as cs
import os

#print(f"Nombre d'images à traiter : {len(images_noms)}\n")

def verif_taille(liste_noms_imgs: list[str]) -> bool:
    """Vérifie si les dimensions des images correspondent aux constantes globales

    Args:
        liste_noms_imgs (list[str]): Liste des images à vérifier

    Returns:
        bool: True si toutes les images sont conformes (Hauteur/Largeur), False sinon
    """

    taille_correcte = True
    for nom in liste_noms_imgs:
        image = imread(cs.PATH + nom)
        if(image.shape[0] != cs.HAUTEUR or image.shape[1] != cs.LARGEUR):
            taille_correcte = False
            print(f"Taille anormale : [ {image.shape[0]} x {image.shape[1]} ]")
    return taille_correcte

def image_to_vec(image : np.ndarray) -> list:
    """Découpe une image en blocs (patchs) et convertit chaque bloc de taille (N x N) en vecteur
        Parcourt l'image par bloc de taille définie dans les constantes (cs.N)
        et aplatit les pixels de chaque bloc

    Args:
        image (np.ndarray): L'image source sous forme de matrice numpy

    Returns:
        list: Une liste de vecteurs np, où chaque vecteur représente un bloc N x N
    """
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
    """Reconstruit l'image originale à partir de la liste de vecteurs obtenue dans image_to_vec
    Calcule la position (x, y) de chaque pixel pour le replacer au bon endroit
    dans la matrice finale à partir des données vectorisées
    
    Args:
        vectors (list): La liste des vecteurs (patchs aplatis) issue de image_to_vec
        
    Returns:
        np.ndarray: L'image reconstruite aux dimensions cs.HAUTEUR x cs.LARGEUR originales
    """
    image = np.ndarray(shape=(cs.HAUTEUR,cs.LARGEUR,3),dtype=np.uint8)
    for i in range(0,cs.HAUTEUR):
        for j in range(0,cs.LARGEUR):
            v_nb = (j // cs.N) + ((i // cs.N) * (cs.LARGEUR // cs.N))
            px_nb = (j % cs.N) + ((i * cs.N) % (cs.N**2))
            for k in range(0,3):
                image[i][j][k] = vectors[v_nb][px_nb][k]

    return image