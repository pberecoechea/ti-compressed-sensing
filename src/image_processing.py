from typing import Literal
from matplotlib.image import imread
import numpy as np
import scipy.sparse as scp
from scipy.fftpack import dct,idct
import scipy.signal as scs
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

def to_gray(image : np.ndarray):
    gray = np.dot(image[...,:3], [0.299, 0.587, 0.114])
    return gray.astype(np.uint8)

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

def vec_to_image (vectors : list):
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
            px_nb = (i % cs.N) * cs.N + (j % cs.N)
            for k in range(0,3):
                image[i][j][k] = vectors[v_nb][px_nb][k]

    return image

def gray_vec_to_gray_image (vectors : list):
    """Reconstruit l'image originale à partir de la liste de vecteurs obtenue dans image_to_vec
    Calcule la position (x, y) de chaque pixel pour le replacer au bon endroit
    dans la matrice finale à partir des données vectorisées
    
    Args:
        vectors (list): La liste des vecteurs (patchs aplatis) issue de image_to_vec
        
    Returns:
        np.ndarray: L'image reconstruite aux dimensions cs.HAUTEUR x cs.LARGEUR originales
    """
    image = np.ndarray(shape=(cs.HAUTEUR,cs.LARGEUR),dtype=np.uint8)
    for i in range(0,cs.HAUTEUR):
        for j in range(0,cs.LARGEUR):
            v_nb = (j // cs.N) + ((i // cs.N) * (cs.LARGEUR // cs.N))
            px_nb = (i % cs.N) * cs.N + (j % cs.N)
            
            image[i][j] = vectors[v_nb][px_nb]

    return image

def phi(id:Literal['uniforme','bernouilli [-1;1]','bernouilli [0;1]','gaussienne','creuse'],ratio:float):
    m = cs.N**2
    div = (1/ratio)
    n = int(m // div)
    
    # + ou - uniforme racine M (on prend N * m données)

    if(m % div != 0):
        n = n + 1
       
    res = np.zeros((n,m))
    generator = np.random.default_rng(108)

    match id:
        case "uniforme" : #phi1 distribution uniforme
            res = generator.uniform(0,1,(n,m))#compléter

        case "bernouilli [-1;1]" : # phi2 Loi de Bernoulli (-1,1)
            res = generator.binomial(1,0.5,(n,m))
            res = np.where(res < 0.5, -1, 1)

        case "bernouilli [0;1]":# phi 3 bernoulli (0,1)
            res = generator.binomial(1,0.5,(n,m))
            res = np.where(res < 0.5, 0, 1)

        case "gaussienne" :# phi 4 distribution gaussienne
            res = generator.normal(0,1/n,(n,m))

        case "creuse" :# phi5 matrice creuse
            res = scp.random(n,m, density =  0.25, random_state = 2000)
            res = res.toarray()  # transformation en array

    return(res)


def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')

def idct2(a):
    return idct(idct(a.T, norm='ortho').T, norm='ortho')  



def get_ys_with_ratio(vectors : list,id:Literal['uniforme','bernouilli [-1;1]','bernouilli [0;1]','gaussienne','creuse'],ratio: float) -> tuple[list[np.ndarray],np.ndarray]:
    phi_n = phi(id,ratio)
    y = []
    for vect in vectors:
        y.append(np.dot(phi_n,vect))

    return y,phi_n

def get_ys_with_ratio_with_phi(vectors : list,phi:np.ndarray) -> list[np.ndarray]:
    y = []
    for vect in vectors:
        y.append(np.dot(phi,vect))

    return y

def threshold(gamma_1: np.ndarray, seuil_lambda: int = 6) -> np.ndarray:
    """
    1. Calcul(Tau)
    2. Applique ce seuil aux coefficients
    
    Returns:
        np.ndarray: Les coefficients DCT filtrés
    """
    
    abs_gamma_1 = np.abs(gamma_1)
    median_gamma = np.median(abs_gamma_1)
    
    # 2. Calcul du seuil Tau
    sigma = median_gamma / 0.6745
    term_log = np.sqrt(2 * np.log(cs.HAUTEUR * cs.LARGEUR))
    
    tau_k = seuil_lambda * sigma * term_log
    
    # 3. Création du Masque
    # On garde le coefficient s'il est supérieure au seuil
    mask = abs_gamma_1 > tau_k
    
    # 4. Calcul de Gamma_2
    # Si masque == 1, on garde la valeur, Sinon 0
    gamma_2 = gamma_1 * mask
    
    return gamma_2

def bcl_spl(phi, x, y, lmbd):
    """
    Fonction de résolution du problème de minimisation
    min ||y - phi(x)||_2^2 + lambda * ||x||_1
    Renvoie x à l'itération r+1
    """
    # Implémentation de l'algorithme de BCL-SPL
    # phi : matrice de mesure
    # lambda : paramètre de régularisation
    # y : liste des vecteur d'observations
    # x : image à optimiser
    
    # Filtre de Wiener pour initialiser x_hat
    x_hat = scs.wiener(x,(3,3))
    
    #Transfomation en imagettes
    x_hat_blocks = image_to_vec(x_hat)

    phi_bis = np.linalg.pinv(phi)

    #Parcours de chaque bloc et mise à jour de ceux ci
    for i in range(0,len(x_hat_blocks)):
        # Étape de mise à jour de x_hat_blocks
        x_hat_blocks[i] = x_hat_blocks[i] + 0.45 * phi.T @ (y[i] - phi @ x_hat_blocks[i])

    # Reconstruction de l'image à partir des blocs mis à jour
    x_hat_hat = gray_vec_to_gray_image(x_hat_blocks)

    # DCT de l'image reconstruite
    x_hat_hat = dct2(x_hat_hat)

    # Seuil de hard-thresholding
    x_hat_hat = threshold(x_hat_hat, lmbd)

    # IDCT pour obtenir l'image finale
    x_barre = idct2(x_hat_hat)

    #Calcul de x_r_1
    #Transformation en imagettes
    x_barre_blocks = image_to_vec(x_barre)
    #Parcours de chaque bloc et mise à jour de ceux ci
    for i in range(len(x_barre_blocks)):
        # Étape de mise à jour de x_barre_blocks
        x_barre_blocks[i] = x_barre_blocks[i] + 0.45 * phi.T @ (y[i] - phi @ x_barre_blocks[i])
    #Reconstruction de l'image à partir des blocs mis à jour
    x_r_1 = gray_vec_to_gray_image(x_barre_blocks)

    return x_r_1


def iterative_bcl_spl(phi:np.ndarray, y:list):
    """
    Itérative BCL-SPL jusqu'a convergence
    """

    phi_bis = np.linalg.pinv(phi)
    x = gray_vec_to_gray_image([phi_bis @ ys for ys in y])
    i = 0
    max_iter = 100
    epsilon = 1e-6
    lmbd = 3
    while True:
        x_old = x.copy()
        x = bcl_spl(phi, x, y,lmbd)
        #Critère d'arrêt
        if (np.linalg.norm(x - x_old)*(1/np.sqrt(cs.HAUTEUR*cs.LARGEUR))) < epsilon or i >= max_iter:
            break
        i += 1
        lmbd = max(lmbd * 0.85, 0.05)
        print(f"BCL NORM : {(np.linalg.norm(x - x_old)*(1/np.sqrt(cs.HAUTEUR*cs.LARGEUR)))}")
        print(i)
    return x