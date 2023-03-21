import pygame
import os
import random

tela_largura = 500
tela_altura = 800

imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('fbird','imgs','pipe.png')))
imagem_chão = pygame.transform.scale2x(pygame.image.load(os.path. join('fbird','imgs','base.png')))
imagem_back = pygame.transform.scale2x(pygame.image.load(os.path.join('fbird','imgs','bg.png')))
imagens_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('fbird','imgs','bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('fbird','imgs','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('fbird','imgs','bird3.png')))
]

pygame.font.init()
fonte_pontos = pygame.font.SysFont('Berlin Sans FB', 50)
fonte_parabéns = pygame.font.SysFont('Imprint MT Shadow', 35)
fonte_mitada = pygame.font.SysFont('Imprint MT Shadow',40)
fonte_perdeu = pygame.font.SysFont('Berlin Sans FB', 50)
texto4 = fonte_perdeu.render('Você PERDEU!', 1, (0, 0, 0))


class Passaro:
    img = imagens_passaro
    #animações da rotação
    rotacao_max = 25
    vel_rotacao = 20
    tempo_anim = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_img = 0
        self.imagem = self.img[0]
    
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        #restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        #angulo do pássaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_max:
                self.angulo = self.rotacao_max
        else:
            if self.angulo > -90:
                self.angulo -= self.vel_rotacao
    
    def desenhar(self, tela):
        #definir imagens
        self.contagem_img += 1

        if self.contagem_img < self.tempo_anim:
            self.imagem = self.img[0]
        elif self.contagem_img < self.tempo_anim * 2:
            self.imagem = self.img[1]
        elif self.contagem_img < self.tempo_anim * 3:
            self.imagem = self.img[2]
        elif self.contagem_img < self.tempo_anim * 4:
            self.imagem = self.img[2]
        elif self.contagem_img >= self.tempo_anim * 4 + 1:
            self.imagem = self.img[0]
            self.contagem_img = 0
            
        #passaro caindo sem bater asas
        if self.angulo <= -80:
            self.imagem = self.img[1]
            self.contagem_img = self.tempo_anim*2

        #desenhar imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center= pos_centro_img)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.cano_topo = pygame.transform.flip(imagem_cano, False, True)
        self.cano_base = imagem_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))
    
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

    

class chão:
    velocidade = 5
    largura = imagem_chão.get_width()
    imagem = imagem_chão

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura
    
    def desenhar(self,tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(imagem_back, (0,0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = fonte_pontos.render(f'Pontuação: {pontos}', 1, (255, 255, 255))
    texto2 = fonte_parabéns.render(f'Você passou de 5!', 1, (240, 220, 130))
    texto3 = fonte_mitada.render(f'Você está MITANDO!', 1, (255, 0, 0))
        
    tela.blit(texto,(tela_largura - 10 - texto.get_width(), 10))
    if pontos == 5:
        tela.blit(texto2,(tela_largura - 5 - texto2.get_width(), 75))
    elif pontos >= 10:
        tela.blit(texto3,(tela_largura - 5 - texto3.get_width(), 75))

    
                               
    chao.desenhar(tela)
    pygame.display.update()



def main():
    passaros = [Passaro(230, 350)]
    chao = chão(730)
    canos = [Cano(700)]
    tela =  pygame.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
                  
        #movimentações
        for passaro in passaros:
            passaro.mover() 
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate (passaros):
                if cano.colidir(passaro):                                            
                    passaros.pop(i) 
                    tela.blit(texto4,(tela_largura - 5 - texto4.get_width(), 75))                    
                else:
                    chao.mover()
                    cano.mover()
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True   
                    adicionar_cano = True   
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    main()

        
        

