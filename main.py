
from functions import *
import subprocess
# Initialisation de Pygame
pygame.init()
# Définition de la taille de la fenêtre

pygame.mixer.music.load("music/audio.mp3")
fullscreen_flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF

# Créer la fenêtre en plein écran
joueur1 = ''
joueur2 = ''

# Jouer la musique en boucle
pygame.mixer.music.play(-1)

manager = pygame_gui.UIManager((1280, 720))

mute_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((615, 350), (100, 50)), text='Mute', manager=manager)

slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((385, 270), (550, 75)), start_value=1.0, value_range=(0.0, 1.0), manager=manager)
clock = pygame.time.Clock()
muted = False
largeur_fenetre = 1280
hauteur_fenetre = 720
taille_case = 75
espace_entre_matrices = 50
sens=2
choix1,choix2=-1,-1
tour=0
taille_matrice = 5
marge_vert = 200
marge_hor = 45
marge_vert2,marge_hor2=marge_vert,850
marge_tab1=500,-50/2+marge_vert
marge_tab2=700, -50/2+marge_vert
matrice_jeu=[[0,0,0,0,0],[0,0,0,0,0],[0,0,'#',0,0],[0,0,0,0,0],[0,0,0,0,0]]
matrice_jeu2=[[0,0,0,0,0],[0,0,0,0,0],[0,0,'#',0,0],[0,0,0,0,0],[0,0,0,0,0]]



text_color = (255, 255, 255)
game_over_sound = pygame.mixer.Sound('music/game_over.mp3')
ia_destroy_sound = pygame.mixer.Sound('music/ia_destroy.mp3')
impossible_sound = pygame.mixer.Sound('music/impossible.mp3')
ia_won_sound = pygame.mixer.Sound('music/villain_laugh.mp3')
super_genius_sound = pygame.mixer.Sound('music/super_genius.mp3')
duel_sound= pygame.mixer.Sound('music/duel.mp3')
# Définition des couleurs
font = pygame.font.Font(None, 30)
BLANC = (255, 255, 255)
BLEU = (145,177,172)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
def open_pdf():
    subprocess.run(['start', 'Kingdomino-Free-Sample-FR.pdf'], shell=True)
# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
# Chargement des images
image_bleue = pygame.Surface((taille_case, taille_case))
image_bleue.fill((128, 128, 128))
etape_jeu=0
image_rouge = pygame.Surface((taille_case, taille_case))
image_rouge.fill(ROUGE)
image_verte= pygame.Surface((taille_case//2, taille_case//2))
image_verte.fill(VERT)
image_noir = pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA)
image_noir.fill(NOIR)
im_rotate = pygame.image.load("images/rotate.png")
im_rotate = pygame.transform.scale(im_rotate, (taille_case//3, taille_case//3))
im_valider = pygame.image.load("images/valider.png")
im_valider = pygame.transform.scale(im_valider, (taille_case//3, taille_case//3))
im_discard = pygame.image.load("images/discard.png")
im_discard = pygame.transform.scale(im_discard, (taille_case//3, taille_case//3))
im_exit = pygame.image.load("images/exit.png")
im_exit = pygame.transform.scale(im_exit, (taille_case*1.5, taille_case))
im_score = pygame.image.load("images/score.png")
im_score = pygame.transform.scale(im_score, (taille_case, taille_case))
im_hi = pygame.image.load("images/highestscores.png")
im_hi = pygame.transform.scale(im_hi, (600, 100))
def play_sound_once(sound):
    """Plays a sound once"""
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.wait(100)
# Matrice pour stocker les images bleues
def addCouronnes(image,couronne,taille_case):
    crown = pygame.image.load("images/couronne.png")
    crown = pygame.transform.scale(crown, (taille_case//3, taille_case//3))
    for i in range(couronne):
        # Définir la position de la couronne
        crown_x = i * (taille_case / couronne) + (taille_case / couronne / 2) - (taille_case//3 / 2)
        crown_y = taille_case - taille_case//3
        
         # Ajouter la couronne à l'image
        image.blit(crown, (crown_x, crown_y))
def addRoi(image,joueur,taille_case):
    king = pygame.image.load("images/king"+str(joueur)+".png")
    king = pygame.transform.scale(king, (taille_case//3, taille_case//3))
    king_x = 15
    king_y = 0
    image.blit(king, (king_x, king_y))

def transform_image(val,couronne,taille_case):
    if(val=='0'):
        
        image_grise=pygame.Surface((taille_case, taille_case))
        image_grise.fill((128,128,128))
        return image_grise
    else:
        image=pygame.image.load("images/"+val+".png")
        image=pygame.transform.scale(image, (taille_case, taille_case))
        addCouronnes(image,couronne,taille_case)
        return image
def val_and_couronne(alpha):
    couronne=str(alpha).count("+")
    val=str(alpha).replace("+","")
    return val,couronne
def transform_matrice(matrice_jeu):
    matrice_bleue = []
    for i in range(taille_matrice):
        ligne = []
        for j in range(taille_matrice):
            #print(i,j)
            val,couronne=val_and_couronne(matrice_jeu[i][j])
            ligne.append(transform_image(val,couronne,taille_case))
            
        matrice_bleue.append(ligne)
    return matrice_bleue

def get_grid_pos(mouse_pos,marge_tab,number_rows,number_col):
    x, y = mouse_pos
    lig = (x - marge_tab[0]) // taille_case
    col = (y - marge_tab[1]) // taille_case
    if(lig>=0 and lig<number_rows+1 and col>=0 and col<number_col+1):
        return int(lig),int(col)
    else: 
        return None,None

def transform_tuiles(tuile):
    couronne1=tuile.cases[0].couronne
    val1=tuile.cases[0].couleur
    couronne2=tuile.cases[1].couronne
    val2=tuile.cases[1].couleur
    image1=transform_image(val1,couronne1,taille_case//2)
    image2=transform_image(val2,couronne2,taille_case//2)
    position1 = (0, 0)
    position2 = (taille_case // 2,0)
    image_tuile=pygame.Surface((taille_case, taille_case),pygame.SRCALPHA)
    image_tuile.blit(image1, position1)
    image_tuile.blit(image2, position2)
    return image_tuile
def changerChoix(matrice,choix):
    
    val,couronne=val_and_couronne(tab_tour[choix-1].cases[0].abv)
    image=transform_image(val,couronne,taille_case//2)
    matrice[1][1]=image
    x,y=(sens-1)//3,(sens-1)%3
    val,couronne=val_and_couronne(tab_tour[choix-1].cases[1].abv)
    image=transform_image(val,couronne,taille_case//2)
    matrice[x][y]=image
# Matrice pour stocker les images rouges
def joueurAleatoire(matrice_jeu2,tab_tour,tab_tour2,matrice_images):
    global etape_jeu,choix2,tuileActuel,sens,joueur,joueuria,tab_tuiles,tour

    if(etape_jeu==4):
        if(tour>0):
            indices = [i for i, tuile in enumerate(tab_tour) if tuile.joueur==2]
        else:
            indices = [i for i, tuile in enumerate(tab_tour) if tuile.joueur is None]
        if indices:
            indice_aleatoire = random.randint(0, len(indices) - 1)
            indice_joueur_aleatoire = indices[indice_aleatoire]
            choix2=indice_joueur_aleatoire+1
            tuileActuel=tab_tour[indice_joueur_aleatoire]
            tab_tour[choix2-1].joueur=joueur
        indices = [i for i, tuile in enumerate(tab_tour2) if tuile.joueur is None]
        if indices:
            indice_aleatoire = random.randint(0, len(indices) - 1)
            indice_joueur_aleatoire = indices[indice_aleatoire]
            x2=indice_joueur_aleatoire
            addRoi(tab_rouge2[x2],joueur,taille_case)
            tab_tour2[x2].joueur=joueur

        d,s=choisir_coup_aleatoire(matrice_jeu2,tuileActuel) if joueuria==1 else meilleur_coup_monte_carlo(matrice_jeu2,tab_tour,tab_tour2,tuileActuel,tab_tuiles,tour)
        if(d!=None and s!=None):
            jouerTour(tuileActuel,sens,d,matrice_jeu2,2,s)
        tab_rouge[choix2-1]=pygame.Surface((taille_case, taille_case),pygame.SRCALPHA)
        matrice_images_noires = []
        for i in range(3):
            ligne_images_noires = []
            for j in range(3):
                ligne_images_noires.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
            matrice_images_noires.append(ligne_images_noires)
        matrice_images_noires2 = []
        for i in range(3):
            ligne_images_noires2 = []
            for j in range(3):
                ligne_images_noires2.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
            matrice_images_noires2.append(ligne_images_noires2)
        
      
        etape_jeu=0
        joueur=1
        sens=2

tab_tuiles=translate_liste()
tab_tour=choisir_tuiles(tab_tuiles)
tab_tour2=choisir_tuiles(tab_tuiles)
def afficher_tuiles(tab_tour):
    tab_rouge = []
    for i in range(4):
        tab_rouge.append(transform_tuiles(tab_tour[i]))
    return tab_rouge
bouton = Button(im_rotate, (320,70), None, pygame.font.SysFont('Arial', 20), NOIR, VERT)
bouton_valider = Button(im_valider, (250,70), None, pygame.font.SysFont('Arial', 20), NOIR, VERT)
bouton_discard = Button(im_discard, (390,70), None, pygame.font.SysFont('Arial', 20), NOIR, VERT)
bouton_exit = Button(im_exit, (1190,640), None, pygame.font.SysFont('Arial', 20), NOIR, VERT)
bouton2 = Button(im_rotate, (1120,70), None, pygame.font.SysFont('Arial', 20), NOIR, VERT)
bouton_valider2 = Button(im_valider, (1050,70), None, pygame.font.SysFont('Arial', 20), NOIR, VERT)
bouton_discard2 = Button(im_discard, (1190,70), None, pygame.font.SysFont('Arial', 20), NOIR, VERT)
bouton_score = Button(im_score, (1190,640), None, pygame.font.SysFont('Arial', 20), NOIR, VERT)
def switchSens(s):
    match s:
        case 2:
            s=6
        case 6:
            s=8
        case 8:
            s=4
        case 4:
            s=2
    return s
def reset_game():
    global choix1, choix2, tour, matrice_jeu, matrice_jeu2, joueur, etape_jeu,manager2,player2_label,text_input2
    global tab_tuiles, tab_tour, tab_tour2, matrice_images_noires, matrice_images_noires2, tab_rouge, tab_rouge2
    choix1,choix2=-1,-1
    tour=0  
    matrice_jeu=[[0,0,0,0,0],[0,0,0,0,0],[0,0,'#',0,0],[0,0,0,0,0],[0,0,0,0,0]]
    matrice_jeu2=[[0,0,0,0,0],[0,0,0,0,0],[0,0,'#',0,0],[0,0,0,0,0],[0,0,0,0,0]]
    joueur=1
    etape_jeu=0   
    sens=2
    tab_tuiles=translate_liste()
    tab_tour=choisir_tuiles(tab_tuiles)
    tab_tour2=choisir_tuiles(tab_tuiles)
    matrice_images_noires = []
    for i in range(3):
        ligne_images_noires = []
        for j in range(3):
            ligne_images_noires.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
        matrice_images_noires.append(ligne_images_noires)
    matrice_images_noires2 = []
    for i in range(3):
        ligne_images_noires2 = []
        for j in range(3):
            ligne_images_noires2.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
        matrice_images_noires2.append(ligne_images_noires2)
    tab_rouge=afficher_tuiles(tab_tour)
    tab_rouge2=afficher_tuiles(tab_tour2)



matrice_images_noires = []
for i in range(3):
    ligne_images_noires = []
    for j in range(3):
        ligne_images_noires.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
    matrice_images_noires.append(ligne_images_noires)
matrice_images_noires2 = []
for i in range(3):
    ligne_images_noires2 = []
    for j in range(3):
        ligne_images_noires2.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
    matrice_images_noires2.append(ligne_images_noires2)
    



# Boucle principale
def tourTermine(tab_tour2):
    for i in range(0, len(tab_tour2)):
        if tab_tour2[i].joueur is None:
            return False
    return True
tab_rouge=afficher_tuiles(tab_tour)
tab_rouge2=afficher_tuiles(tab_tour2)

def jeuprincipal():
    global SCREEN,tab_rouge,tab_rouge2,tab_tour,tab_tour2,etape_jeu,matrice_images_noires,matrice_images_noires2,font,tour,choix2,choix1,sens,joueur
    while True:
        SCREEN.blit(fenetre, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        matrice1_pos = get_grid_pos(MENU_MOUSE_POS, (marge_hor, marge_vert), taille_matrice, taille_matrice)
        matrice2_pos = get_grid_pos(MENU_MOUSE_POS, (marge_hor2, marge_vert2), taille_matrice, taille_matrice)
        # Effacement de l'écran
        fenetre.blit(BG, (0, 0))
        if(joueuria!=0):
            joueurAleatoire(matrice_jeu2,tab_tour,tab_tour2,etape_jeu)

        # Affichage des deux matrices bleues
        matrice_bleue=transform_matrice(matrice_jeu)
        matrice_bleue2=transform_matrice(matrice_jeu2)
        for i in range(taille_matrice):
            for j in range(taille_matrice):
                pygame.draw.rect(matrice_bleue[i][j], BLEU, pygame.Rect((0, 0), (taille_case, taille_case)), 1)
                fenetre.blit(matrice_bleue[i][j], (i*taille_case+marge_hor, j*taille_case+marge_vert))
                pygame.draw.rect(matrice_bleue2[i][j], BLEU, pygame.Rect((0, 0), (taille_case, taille_case)), 1)
                fenetre.blit(matrice_bleue2[i][j], (i*taille_case+marge_hor2, j*taille_case+marge_vert))
                if matrice1_pos is not None:
                    lig, col = matrice1_pos
                    if lig == i and col == j:
                        # Dessin du contour bleu
                        pygame.draw.rect(fenetre, VERT, pygame.Rect((i*taille_case+marge_hor, j*taille_case+marge_vert), (taille_case, taille_case)), 1)       
        # Affichage des images noires
                if matrice2_pos is not None:
                    lig2, col2 = matrice2_pos
                    if lig2 == i and col2 == j:
                        # Dessin du contour bleu
                        pygame.draw.rect(fenetre, VERT, pygame.Rect((i*taille_case+marge_hor2, j*taille_case+marge_vert2), (taille_case, taille_case)), 1)       
        for i in range(3):
            for j in range(3):
                fenetre.blit(matrice_images_noires[i][j], (i*taille_case//2+marge_hor+100/2, j * taille_case//2+15))
        if(joueuria==0):
            for i in range(3):
                for j in range(3):
                    fenetre.blit(matrice_images_noires2[i][j], (i*taille_case//2+900, j * taille_case//2+15))
        # Affichage des deux matrices rouges dans l'espace entre les matrices bleues
        
        for i in range(4):
                fenetre.blit(tab_rouge[i], (marge_tab1[0], marge_tab1[1]+(i+1)*taille_case))
                fenetre.blit(tab_rouge2[i], (marge_tab2[0], marge_tab2[1]+(i+1)*taille_case))
        etape_actions = {
            0: "Choisissez une tuile "+joueur1.capitalize(),
            1: "Veuillez choisir le sens et valider",
            2: "Jouez votre coup "+joueur1.capitalize(),
            3: "Choisissez votre coup pour le tour suivant "+joueur1.capitalize(),
            4: "Choisissez une tuile "+joueur2.capitalize(),
            5: "Veuillez choisir le sens et valider",
            6: "Jouez votre coup "+joueur2.capitalize(),
            7: "Choisissez votre coup pour le tour suivant "+joueur2.capitalize(),
        } 
        background_color = (128, 128, 128)

        text_surface = font.render("{}".format(etape_actions[etape_jeu]), True, "BLACK")
        text_surface2 = font.render("Tour: {}".format(tour+1), True, "BLACK")
        SCREEN.blit(text_surface2, (50, 650))
        # Create the background surface
        background_surface = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 10))
        background_surface.fill(background_color)

        # Blit the text surface onto the background surface
        background_surface.blit(text_surface, (5, 5))

        # Get the rect for the background surface and center it
        background_rect = background_surface.get_rect()
        background_rect.center = (largeur_fenetre // 2, 625)
        if(joueuria==0):
            bouton_discard2.update(fenetre)
            bouton_valider2.update(fenetre)
            bouton2.update(fenetre)
             # Blit the background surface onto the screen
        fenetre.blit(background_surface, background_rect)
        bouton.update(fenetre)
        bouton_valider.update(fenetre)
        bouton_discard.update(fenetre)
        bouton_exit.update(fenetre)

        if tourTermine(tab_tour2):
            tour+=1
            tab_tour=tab_tour2
            tab_tour2=choisir_tuiles(tab_tuiles)
            tab_rouge=afficher_tuiles(tab_tour)
            tab_rouge2=afficher_tuiles(tab_tour2)
            for i in range(4):
                if hasattr(tab_tour[i], 'joueur'):
                    addRoi(tab_rouge[i],tab_tour[i].joueur,taille_case)


        if(tour==6):
            if(joueuria!=0 and score(matrice_jeu)<score(matrice_jeu2)):
                play_sound_once(ia_won_sound)
            else:
                play_sound_once(game_over_sound)
            play()
    
        # Rafraîchissement de l'écran
        pygame.display.flip()
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                _,x = get_grid_pos(MENU_MOUSE_POS,marge_tab1,1,4)
                _,x2= get_grid_pos(MENU_MOUSE_POS,marge_tab2,1,4)
                if (x) :
                    if(etape_jeu==0 and tab_tour[x-1].joueur!=2):
                        choix1=x
                        changerChoix(matrice_images_noires,choix1)
                        etape_jeu=1
                    if(etape_jeu==4 and tab_tour[x-1].joueur!=1):
                        choix2=x
                        changerChoix(matrice_images_noires2,choix2)
                        etape_jeu=5
                if(x2):
                    if(etape_jeu==3 and tab_tour2[x2-1].joueur==None):
                        addRoi(tab_rouge2[x2-1],joueur,taille_case)
                        tab_tour2[x2-1].joueur=joueur
                        etape_jeu=4
                        joueur=2
                        sens=2
                    if(etape_jeu==7 and tab_tour2[x2-1].joueur==None):
                        addRoi(tab_rouge2[x2-1],joueur,taille_case)
                        tab_tour2[x2-1].joueur=joueur
                        etape_jeu=0
                        joueur=1
                        sens=2
                
                if(etape_jeu==2):
                    if(matrice1_pos!=(None,None)):
                        if(jouerTour(tab_tour[choix1-1],sens,matrice1_pos,matrice_jeu,joueur)):
                            matrice_bleue=transform_matrice(matrice_jeu)
                            etape_jeu=3
                            tab_rouge[choix1-1]=pygame.Surface((taille_case, taille_case),pygame.SRCALPHA)
                            matrice_images_noires = []
                            for i in range(3):
                                ligne_images_noires = []
                                for j in range(3):
                                    ligne_images_noires.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
                                matrice_images_noires.append(ligne_images_noires)
                            matrice_images_noires2 = []
                            for i in range(3):
                                ligne_images_noires2 = []
                                for j in range(3):
                                    ligne_images_noires2.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
                                matrice_images_noires2.append(ligne_images_noires2)
                            tab_tour[choix1-1].joueur=joueur
                        else:
                            print("Coup impossible")
                if(etape_jeu==6):
                    if(matrice2_pos!=(None,None)):
                        if(jouerTour(tab_tour[choix2-1],sens,matrice2_pos,matrice_jeu2,joueur)):
                            matrice_bleue2=transform_matrice(matrice_jeu2)
                            etape_jeu=7
                            tab_rouge[choix2-1]=pygame.Surface((taille_case, taille_case),pygame.SRCALPHA)
                            matrice_images_noires = []
                            for i in range(3):
                                ligne_images_noires = []
                                for j in range(3):
                                    ligne_images_noires.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
                                matrice_images_noires.append(ligne_images_noires)
                            matrice_images_noires2 = []
                            for i in range(3):
                                ligne_images_noires2 = []
                                for j in range(3):
                                    ligne_images_noires2.append(pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA))
                                matrice_images_noires2.append(ligne_images_noires2)
                            tab_tour[choix2-1].joueur=joueur
                        else:
                            print("Coup impossible")
                    
                for bt,choix,mat in ((bouton,choix1,matrice_images_noires),(bouton2,choix2,matrice_images_noires2)):
                    if bt.checkForInput(MENU_MOUSE_POS):
                        sens=switchSens(sens)
                        for i in (2,4,6,8):
                            x,y=(i-1)//3,(i-1)%3
                            val,couronne=val_and_couronne(tab_tour[choix-1].cases[1].abv)
                            imageC=transform_image(val,couronne,taille_case//2)
                            if i!=sens:
                                mat[x][y]=pygame.Surface((taille_case//2, taille_case//2),pygame.SRCALPHA)
                            else:
                                mat[x][y]=imageC
                # if bouton2.checkForInput(MENU_MOUSE_POS):
                #     sens2=switchSens(sens2)
                #     print('2')
                #     for i in (2,4,6,8):
                #         x,y=(i-1)//3,(i-1)%3
                #         val,couronne=val_and_couronne(tab_tour[choix2-1].cases[1].abv)
                #         image=transform_image(val,couronne,taille_case//2)
                #         if i!=sens:
                #             matrice_images_noires2[x][y]=image_noir
                #         else:
                #             matrice_images_noires2[x][y]=image
                if bouton_valider.checkForInput(MENU_MOUSE_POS) and etape_jeu==1 :   
                    etape_jeu=2
                if bouton_valider2.checkForInput(MENU_MOUSE_POS) and etape_jeu==5 :   
                    etape_jeu=6
                if bouton_discard.checkForInput(MENU_MOUSE_POS) and (etape_jeu==1 or etape_jeu==2): 
                    tab_tour[choix1-1].joueur=joueur 
                    tab_rouge[choix1-1]=pygame.Surface((taille_case, taille_case),pygame.SRCALPHA) 
                    etape_jeu=3
                if bouton_discard.checkForInput(MENU_MOUSE_POS) and (etape_jeu==5  or etape_jeu==6) :
                    tab_tour[choix2-1].joueur=joueur 
                    tab_rouge[choix2-1]=pygame.Surface((taille_case, taille_case),pygame.SRCALPHA)  
                    etape_jeu=7
                if bouton_exit.checkForInput(MENU_MOUSE_POS):
                    reset_game()
                    main_menu()
                    
                        

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

SCREEN = pygame.display.set_mode((1280,720), fullscreen_flags)
pygame.display.set_caption("Menu")

BG = pygame.image.load("images/bg.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    with open('scores.txt', 'a', encoding='utf-8') as file:
        file.write(f'{joueur1},{score(matrice_jeu)}\n')
        if(joueuria==0):
            file.write(f'{joueur2},{score(matrice_jeu2)}\n')
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        surface_scores = pygame.Surface((1280, 720))
        surface_scores.fill("black")
        font = get_font(75)
        
        if joueuria!=0:
            joueur2="IA" 
        for sc,i,j in ((score(matrice_jeu),1,joueur1),(score(matrice_jeu2),2,joueur2)):

            texte = j.capitalize()+": "+str(sc)
            surface_texte = font.render(texte, True, (255, 255, 255))
            x = (1280 - surface_texte.get_width()) // 2
            y = (i+1) * surface_texte.get_height()+(720 - surface_texte.get_width()) // 2
            surface_scores.blit(surface_texte, (x, y))
        SCREEN.blit(surface_scores, (0, 0))

        PLAY_BACK = Button(image=None, pos=(640, 580), 
                            text_input="MENU", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    reset_game()
                    main_menu()

        pygame.display.update()

def typematch():
    global joueuria
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_BUTTON1 = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 150), 
                              text_input="2 JOUEURS", font=get_font(40), base_color="Black", hovering_color="White")
        PLAY_BUTTON2 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 300), 
                            text_input="IA FACILE", font=get_font(40), base_color="Black", hovering_color="White")
        PLAY_BUTTON4 = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 450), 
                            text_input="IA DIFFICILE", font=get_font(40), base_color="Black", hovering_color="White")
        PLAY_BUTTON3 = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 600), 
                            text_input="QUITTER", font=get_font(40), base_color="Black", hovering_color="White")
                            
        for button in [PLAY_BUTTON1, PLAY_BUTTON2, PLAY_BUTTON3,PLAY_BUTTON4]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

     

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON3.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if PLAY_BUTTON2.checkForInput(OPTIONS_MOUSE_POS):
                    play_sound_once(ia_destroy_sound)
                    joueuria=1
                    get_user_name()
                if PLAY_BUTTON1.checkForInput(OPTIONS_MOUSE_POS):
                    play_sound_once(duel_sound)
                    joueuria=0
                    get_user_name()
                if PLAY_BUTTON4.checkForInput(OPTIONS_MOUSE_POS):
                    joueuria=2
                    play_sound_once(super_genius_sound)
                    get_user_name()

        pygame.display.update()
def options():
    global muted
    while True:
        time_delta = clock.tick(60) / 1000.0
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == mute_button:
                        muted = not muted  # toggle the mute state
                        if muted:
                            pygame.mixer.music.set_volume(0)  # mute the sound
                            mute_button.set_text('Unmute')
                        else:
                            pygame.mixer.music.set_volume(slider.get_current_value())  # unmute the sound and set volume to current slider value
                            mute_button.set_text('Mute')

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if not muted:  # only set volume if not muted
                        pygame.mixer.music.set_volume(event.value)
        PLAY_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(665, 500), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        manager.update(time_delta)

        SCREEN.fill((0, 0, 0))

        manager.draw_ui(SCREEN)
        PLAY_BACK.update(SCREEN)

        pygame.display.update()


font3 = pygame.font.Font(None, 50)
theme = "text_entry_line.json"
manager2 = pygame_gui.UIManager((1280, 720))
manager2.get_theme().load_theme(theme)
manager3= pygame_gui.UIManager((1280, 720))
manager3.get_theme().load_theme(theme)
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((450, 175), (500, 75)), manager=manager2,
                                               object_id='#main_text_entry')
text_input2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((450, 375), (500, 75)), manager=manager2,
                                               object_id='#main_text_entry2')
player1_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((250, 175), (200, 75)),
    text="Nom du joueur 1:",
    manager=manager2
)

player2_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((250, 375), (200, 75)),
    text="Nom du joueur 2:",
    manager=manager2
)

text_inputbis = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((450, 175), (500, 75)), manager=manager3,
                                               object_id='#main_text_entry3')
player1_labelbis = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((250, 175), (200, 75)),
    text="Nom du joueur 1:",
    manager=manager3
)

def get_user_name():
    global joueur2,joueur1,joueuria
    print(joueuria)
    while True:
  

        UI_REFRESH_RATE = clock.tick(60)/1000
        USER_MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and
                (event.ui_object_id == '#main_text_entry' or event.ui_object_id == '#main_text_entry3' )):
                joueur1=event.text
            if (event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and
                event.ui_object_id == '#main_text_entry2'):
                joueur2=event.text
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(USER_MOUSE_POS):
                    print(joueur1,joueur2)
                    jeuprincipal()
            if joueuria==0:
                manager2.process_events(event)
            else:
                manager3.process_events(event) 
            
        
        
        PLAY_BACK = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(665, 600), 
                            text_input="VALIDER", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(USER_MOUSE_POS)

        text_surface = font3.render("Saisie noms des joueurs", True, "white")

       
        text_rect = text_surface.get_rect()
        text_rect.center = (1280 // 2, 100)

        # Blit the background surface onto the screen
   

        SCREEN.fill("black")
        if joueuria==0:
            manager2.update(UI_REFRESH_RATE)
            manager2.draw_ui(SCREEN)
        else:
            manager3.update(UI_REFRESH_RATE)
            manager3.draw_ui(SCREEN) 
        SCREEN.blit(text_surface, text_rect)
        PLAY_BACK.update(SCREEN)

        pygame.display.update()
    
def main_menu():
    
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("KINGDOMINO", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 200), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 350), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HELP_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), 
                            text_input="AIDE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 650), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        bouton_score.update(SCREEN)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON,HELP_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    typematch()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    open_pdf()
                if bouton_score.checkForInput(MENU_MOUSE_POS):
                    scoremenu()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
def scoremenu():
    scores_file = 'scores.txt'
    if not os.path.exists(scores_file):
        open(scores_file, 'w').close()  # create the file if it doesn't exist
    with open(scores_file, 'r') as f:
        scores = [line.strip().split(',') for line in f.readlines()]

    # sort the scores by score value (the second element in each line)
    scores.sort(key=lambda x: int(x[1]), reverse=True)
    # display the top 5 scores
    y = 50
    SCREEN.fill("BLACK")
    score_surfaces = []
    font_name = pygame.font.SysFont("Courier New", 40)
    font_score = pygame.font.SysFont("Courier New", 40)
    for i in range(5):
        if i < len(scores):
            name_surface = font_name.render(scores[i][0], True, "WHITE")
            score_surface = font_score.render(str(scores[i][1]), True, "WHITE")
            score_surfaces.append((name_surface, score_surface))
        else:
            score_surfaces.append((None, None))

    # Draw scores to screen
    SCREEN.fill("BLACK")
    for i, (name_surface, score_surface) in enumerate(score_surfaces):
        if name_surface is not None:
            SCREEN.blit(name_surface, (250, 200 + i * 50))
        if score_surface is not None:
            SCREEN.blit(score_surface, (1280 - 450, 200 + i * 50))
    SCREEN.blit(im_hi,(300,50))
    # main game loop
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 650), 
                            text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        main_menu()
        pygame.display.update()
main_menu()