import random
class Case:
    def __init__(self,couleur,couronne):
        self.couleur=couleur
        self.couronne=couronne

class Tuile:
    def __init__(self,cases,indice):
        self.cases=cases
        self.indice=indice

def choisir_tuiles(tab_tuiles):
    t=[tab_tuiles.pop(random.randrange(len(tab_tuiles))) for _ in range(4)]
    t.sort(key=lambda x: x.indice)
    return t
def select_tuiles(tab_prem_tour):
    t1=tab_prem_tour
    t2=[]
    for i in range(len(t1)):
        print([x.indice for x in t1])
        choix= int(input("Donnez votre choix"))
        t2.append(t1.pop(choix))
        t2[i].joueur=i%2
    t2.sort(key=lambda x: x.indice)
    return t2

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
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            l, c = l_index + dx, c_index + dy
            if (l >= 0 and l < taille_l) and (
                c >= 0 and c < taille_c
            ):
            
                if tuile.cases[abs(dl)+abs(dc)]==matrice_jeu[l][c]:
                    return True
                if matrice_jeu[l][c]==666:            #666==chateau
                    return True

    return False
def calcul_score_region(matrice_jeu, l_index, c_index):
    case_actuel = matrice_jeu[l_index][c_index]
    # print(matrice_jeu)
    if case_actuel == 0:
        return

    matrice_jeu[l_index][c_index] = 0
    taille_l = len(matrice_jeu)
    taille_c = len(matrice_jeu[0])
    sc=case_actuel
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        l, c = l_index + dx, c_index + dy
        if (l >= 0 and l < taille_l) and (
            c >= 0 and c < taille_c
        ):
            if matrice_jeu[l][c] == case_actuel:
                a,_=calcul_score_region(matrice_jeu, l, c)
                sc+=a
                print(sc)
    return sc,case_actuel

def calcul_points_couleur(matrice_jeu):
    copie_jeu = [l[:] for l in matrice_jeu]
    tab_couleurs=[]
    for l_index, l in enumerate(copie_jeu):
        for c_index, _ in enumerate(l):
            if matrice_jeu[l_index][c_index] == 0:
                continue
            tab_couleurs.append(calcul_score_region(copie_jeu, l_index, c_index))
    return [val for val in tab_couleurs if val is not None]
# def calcul_score(matrice_jeu):


# matrice=[[1,1,1,1],[2,1,1,3],[2,3,3,1]]
# print(calcul_points_couleur(matrice))


matrice=[[0,0,0,0,0],[0,0,0,0,0],[0,0,666,0,0],[0,0,0,0,0],[0,0,0,0,0]]
cases=[5,5]
tuile=Tuile(cases,5)
print(coup_possible(matrice,tuile,(1,1),(1,0)))

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
# tab_choix=select_tuiles(tab_prem_tour)
# print([x.joueur for x in tab_choix])

