import random
class Case:
    def __init__(self,couleur,couronne):
        self.couleur=couleur
        self.couronne=couronne

class Tuile:
    def __init__(self,case1,case2,indice):
        self.case1=case1
        self.case2=case2
        self.indice=indice
def afficherTuile(t):
    print(t.case1.couleur)
    print(t.case2.couleur)
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

case1=Case("rouge",1)
case2=Case("rouge",2)
case3=Case("bleu",2)
tuile1=Tuile(case1,case1,1)
tuile2=Tuile(case1,case2,2)
tuile3=Tuile(case3,case2,3)
tuile4=Tuile(case1,case3,4)
tuile5=Tuile(case3,case3,5)
tab_tuiles=[tuile1,tuile2,tuile3,tuile4,tuile5]

tab_prem_tour=choisir_tuiles(tab_tuiles)
tab_choix=select_tuiles(tab_prem_tour)
print([x.joueur for x in tab_choix])

