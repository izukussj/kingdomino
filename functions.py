import random
import copy
import pygame,sys,os
from button import Button
import pygame_gui
joueur=1
joueuria=0

pygame.init()
class Case:
   
    def __init__(self,couleur,couronne,abv):
        self.couleur=couleur
        self.couronne=couronne
        self.abv=abv

class Tuile:
    def __init__(self,cases,indice,joueur=None):
        self.cases=cases
        self.indice=indice
        self.joueur=joueur

def translate_liste():
    liste_dominos = [
        ("C", "C"), ("C", "C"), ("B", "B"), ("B", "B"), ("B", "B"), ("B", "B"),
        ("E", "E"), ("E", "E"), ("E", "E"), ("P", "P"), ("P", "P"), ("M", "M"),
        ("B", "C"), ("C", "E"), ("C", "P"), ("C", "M"), ("B", "E"), ("B", "P"),
        ("B", "C+"), ("C+", "E"), ("C+", "P"), ("C+", "M"), ("C+", "F"), ("B+", "C"),
        ("B+", "C"), ("B+", "C"), ("B+", "C"), ("B+", "E"), ("B+", "P"), ("C", "E+"),
        ("C", "E+"), ("B", "E+"), ("B", "E+"), ("B", "E+"), ("B", "E+"), ("C", "P+"),
        ("P+", "E"), ("C", "M+"), ("P", "M+"), ("C", "F+"), ("C", "P++"), ("E", "P++"),
        ("C", "M++"), ("P", "M++"), ("C", "F++"), ("M", "F++"), ("M", "F++"), ("C", "F+++")
      ]
    new_liste_dominos=[]
    for i, l in enumerate(liste_dominos):
        l2=[]
        for j, _ in enumerate(l):
            l2.append(Case(liste_dominos[i][j].replace("+",""),liste_dominos[i][j].count("+"),liste_dominos[i][j]))
        new_liste_dominos.append(Tuile(l2,i))
    return new_liste_dominos

def choisir_tuiles(tab_tuiles):
    t=[tab_tuiles.pop(random.randrange(len(tab_tuiles))) for _ in range(4)]
    t.sort(key=lambda x: x.indice)
    return t
def select_tuiles(tab,getChoix):
   
    t1=tab
    t2=[]
    for i in range(len(t1)):
        print([(x.cases[0].abv,x.cases[1].abv) for x in t1])
        choix= getChoix()
        t2.append(t1[choix])
        t2[i].joueur=i%2
    t2.sort(key=lambda x: x.indice)
    return t2
def jouerTour(tuile,s,debut,matrice_jeu,joueur,sens=None):
    global joueuria
    i,j=debut
    if not sens:
        match s:
            case 6: sens=(0,1)
            case 4: sens=(0,-1)
            case 2: sens=(-1,0)
            case 8: sens=(1,0)
    if not coup_possible(matrice_jeu,tuile,(i,j),sens):
        if(joueuria!=0 or joueur==1):
            play_sound_once(impossible_sound)
        print("Coup Impossible!")
        return False
    matrice_jeu[i][j]=tuile.cases[0].abv
    matrice_jeu[i+sens[0]][j+sens[1]]=tuile.cases[1].abv
    return True

game_over_sound = pygame.mixer.Sound('music/game_over.mp3')
ia_destroy_sound = pygame.mixer.Sound('music/ia_destroy.mp3')
impossible_sound = pygame.mixer.Sound('music/impossible.mp3')
ia_won_sound = pygame.mixer.Sound('music/villain_laugh.mp3')
super_genius_sound = pygame.mixer.Sound('music/super_genius.mp3')
duel_sound= pygame.mixer.Sound('music/duel.mp3')
def play_sound_once(sound):
    """Plays a sound once"""
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.wait(100)
def tourA(tab_prem,tab_sec,tab_tuiles,matrice_gen):
    t2=tab_sec
    tab_sec=[]
    
    for i in range(len(tab_prem)):
        jouerTour(tab_prem[i],matrice_gen[tab_prem[i].joueur],tab_prem[i].joueur)
        print([(x.cases[0].abv,x.cases[1].abv) for x in t2])
        choix= int(input("Donnez votre choix Joueur n°"+str(tab_prem[i].joueur)))
        tab_sec.append(t2.pop(choix))
        tab_sec[i].joueur=tab_prem[i].joueur
    tab_prem=tab_sec
    tab_sec=choisir_tuiles(tab_tuiles)
    print("Fin du tour")
    return tab_prem,tab_sec
def resultat_simulation(matrice_jeu,tab_tour,tab_tour2,tuile,debut,sens,tab_tuiles,tour):
    score_simul=0
    for i in range(10):
        score_simul+=simuler_jeu_once(matrice_jeu,tab_tour,tab_tour2,tuile,debut,sens,tab_tuiles,tour)
    return score_simul/10

def meilleur_coup_monte_carlo(matrice_jeu,tab_tour,tab_tour2,tuile,tab_tuiles,tour):
    coups_possibles=lister_coups_possibles(matrice_jeu,tuile)
    res=[]
    for c in coups_possibles:
        d,s=c
        res.append(resultat_simulation(matrice_jeu,tab_tour,tab_tour2,tuile,d,s,tab_tuiles,tour))
    print("++++++++++++")
    print(res)
    print("---------------------")
    if len(res)==0:
        return (None, None)
    else:
        return coups_possibles[res.index(max(res))]

def tourTermine(tab_tour2):
    for i in range(0, len(tab_tour2)):
        if hasattr(tab_tour2[i], 'joueur') and tab_tour2[i].joueur is None:
            return False
    return True    
def simuler_jeu_once(matrice_jeu,tbt,tbt2,tuile,debut,sens,tab_tuiles,tour):
    t=copy.deepcopy(tab_tuiles)
    matrice_depart=copy.deepcopy(matrice_jeu)
    tab_tour=copy.deepcopy(tbt)
    tab_tour2=copy.deepcopy(tbt2)
    d,s=debut,sens
    tuileActuel=tuile
    for i in range(4-tour):
        while(tourTermine(tab_tour2)==False):
            if(d is None and s is None):
                return score(matrice_depart)
            jouerTour(tuileActuel,2,d,matrice_depart,s)
            for j in (1,2):
                indices = [i for i, tuile in enumerate(tab_tour) if tuile.joueur==j or tuile.joueur is None]
                indice_aleatoire = random.randint(0, len(indices) - 1)
                indice_joueur_aleatoire = indices[indice_aleatoire]
                tab_tour[indice_joueur_aleatoire].joueur=j
                indices = [i for i,  tuile in enumerate(tab_tour2) if tuile.joueur is None ]
                indice_aleatoire = random.randint(0, len(indices) - 1)
                indice_joueur_aleatoire = indices[indice_aleatoire]
                tab_tour2[indice_joueur_aleatoire].joueur=j
            tuileActuel=tab_tour[indice_joueur_aleatoire]
            d,s=choisir_coup_aleatoire(matrice_depart,tuileActuel)
        tab_tour=tab_tour2
        tab_tour2=choisir_tuiles(t)
        #print(tourTermine(tab_tour))
      
    return score(matrice_depart)



    
    

def lister_coups_possibles(matrice_jeu, tuile):
    coups_possibles = []
    for l in range(len(matrice_jeu)):
        for c in range(len(matrice_jeu[0])):
            for sens in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                debut = (l, c)
                if coup_possible(matrice_jeu, tuile, debut, sens):
                    coups_possibles.append((debut, sens))
    return coups_possibles
def choisir_coup_aleatoire(matrice_jeu, tuile):
    coups_possibles=lister_coups_possibles(matrice_jeu,tuile)
    if(len(coups_possibles)==0):
        return None,None
    index_coup = random.randint(0, len(coups_possibles) - 1)
    debut, sens = coups_possibles[index_coup]
    if coup_possible(matrice_jeu, tuile, debut, sens):
        return debut, sens
    else:
        return None, None
def coup_possible(matrice_jeu,tuile,debut,sens):
    taille_l = len(matrice_jeu)
    taille_c = len(matrice_jeu[0])
    debut_l,debut_c=debut
    for dl,dc in ((0,0),sens):
        l_index,c_index=dl+debut_l,dc+debut_c
        if (l_index < 0 or l_index >= taille_l) or (
            c_index < 0 or c_index >= taille_c
        ):
            return False
        if matrice_jeu[l_index][c_index]!=0:
            return False
    for dl,dc in ((0,0),sens):
        l_index,c_index=dl+debut_l,dc+debut_c
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            l, c = l_index + dx, c_index + dy
            if (l >= 0 and l < taille_l) and (
                c >= 0 and c < taille_c
            ):
            
                if tuile.cases[abs(dl)+abs(dc)].couleur==str(matrice_jeu[l][c]).replace("+",""):
                    return True
                if matrice_jeu[l][c]=='#':            #666==chateau
                    return True

    return False
def calcul_score_region(matrice_jeu, l_index, c_index):
    case_actuel = matrice_jeu[l_index][c_index]
    # print(matrice_jeu)
    if case_actuel == 0:
        return 0,0

    matrice_jeu[l_index][c_index] = 0
    taille_l = len(matrice_jeu)
    taille_c = len(matrice_jeu[0])
    sc=case_actuel.count("+")
    scc=1
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        l, c = l_index + dx, c_index + dy
        if (l >= 0 and l < taille_l) and (
            c >= 0 and c < taille_c
        ):
            if str(matrice_jeu[l][c]).replace("+","") == str(case_actuel).replace("+",""):
                a,aa=calcul_score_region(matrice_jeu, l, c)
                sc+=a
                scc+=aa
    return sc,scc

def score(matrice_jeu):
    copie_jeu = [l[:] for l in matrice_jeu]
    score=0
    for l_index, l in enumerate(copie_jeu):
        for c_index, _ in enumerate(l):
            if matrice_jeu[l_index][c_index] == 0:
                continue
            sc,scc=calcul_score_region(copie_jeu, l_index, c_index)
            score+=sc*scc
    return score

# def calcul_score(matrice_jeu):







# matrice=[[1,1,1,1],[2,1,1,3],[2,3,3,1]]
# print(calcul_points_couleur(matrice))


# matrice1=[[0,0,0,0,0],[0,0,0,0,0],[0,0,'#',0,0],[0,0,0,0,0],[0,0,0,0,0]]
# matrice2=[[0,0,0,0,0],[0,0,0,0,0],[0,0,'#',0,0],[0,0,0,0,0],[0,0,0,0,0]]
# matrice_gen=[matrice1,matrice2]
# print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrice]))

# cases=[5,5]
# tuile=Tuile(cases,5)
# jouerTour(tuile,matrice)
# print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrice]))
# print(coup_possible(matrice,tuile,(1,1),(1,0)))

# case1=Case("rouge",1)
# case2=Case("rouge",2)
# case3=Case("bleu",2)
# tuile1=Tuile(case1,case1,1)
# tuile2=Tuile(case1,case2,2)
# tuile3=Tuile(case3,case2,3)
# tuile4=Tuile(case1,case3,4)
# tuile5=Tuile(case3,case3,5)
# tab_tuiles=[tuile1,tuile2,tuile3,tuile4,tuile5]

# tab_prem_tour=choisir_tuiles(tab_tuiles)
# tab_sec_tour=choisir_tuiles(tab_tuiles)
# tab_choix=select_tuiles(tab_prem_tour)

# for i in range(2):
#     tab_choix,tab_sec_tour=tour(tab_choix,tab_sec_tour,tab_tuiles,matrice_gen)
# print("------------------FIN DE PARTIE-----------------")

# print("Score du joueur n° 0 "+str(score(matrice_gen[0])))
# print("Score du joueur n° 1 "+str(score(matrice_gen[1])))
# print([x.joueur for x in tab_choix])



#     # liste des dominos du jeu comme nuplet d'abbréviations de terrains avec
#     # chaque bonus marqué comme "+": ces nuplets devront être traduits

