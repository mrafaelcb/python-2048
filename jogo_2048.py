# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 01:39:13 2019

@author: Maycon Rafael Campos Borba
"""
import platform
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains


class Game2040:
    #construtor
    def ___init__(self):
        pass
    
    #iniciar game      
    def iniciar(self):
        #teclas que pode utilizar
        directions = [Keys.UP, Keys.DOWN, Keys.RIGHT, Keys.LEFT]
        #sistema operacional usado
        if(self.sistema_utilizado() == "Windows"):
            print("Rodando versão do Windows.")
            #instala drive se precisar
            firefox = webdriver.Firefox(executable_path=GeckoDriverManager().install())
            #tela cheia
            firefox.maximize_window()
            #link do jogo
            firefox.get('https://play2048.co/')
            #pega elemento do html para ir utilizando as teclas
            body_jogo = firefox.find_element_by_tag_name('body')
            #variavel para salvar os movimentos ou setar movimentos
            movimentos = []
            while(True):
                #caso jogo estiver acabado ira reiniciar returnando os valores obtidos na partida
                valor = self.reiniciar(firefox, movimentos)
                if(valor!=None):
                    return valor
                #salvando os movimentos setados randomicamente
                movimentos.append(randint(0, 3))
                body_jogo.send_keys(directions[randint(0, 3)])

        elif (self.sistema_utilizado() == "Linux"):
            print("Rodando versão do Linux.")
            print("Não implantado.")
            return None
            pass
        else:
            print("Sistema não identificado: " + self.sistema_utilizado())
            return None
            pass
    
    #reiniciar game 
    def reiniciar(self, firefox, movimentos):
        try:
            #tenta encontrar o elemento que indica que o player perdeu
            retry = firefox.find_element_by_link_text('Try again')
        except:
            pass
        else:
            #conseguiu achar elemento que indica a derrota
            valor_atual = int(firefox.find_element_by_class_name('score-container').text)
            #pegando valores relativo ao resultado
            result = {'valor_atual': valor_atual, 'valor_maximo': self.valor_maior(firefox), 'movimentos': movimentos}
            #reinicia a partida
            retry.click()
            return result
        
    #função encarregada de pegar o maior valor de um bloco
    def valor_maior(self, firefox):
        maior = 0
        #percorre uma matriz(4, 4)
        for i in range(1,5):
            for j in range(1,5):
                #acessando a cada bloco e obtendo o resultado
                aux = int(firefox.find_element_by_class_name('tile-position-'+str(i)+'-'+str(j)).text)
                #verificando se o valor do bloco é o maior encontrado até o momento
                if(maior < aux):
                    maior = aux
        return maior
    
    def sistema_utilizado(self):
        return platform.system()

#main para teste
if __name__ == '__main__':
    #inicia o objeto
    game = Game2040()
    #inicia uma rodada
    result = game.iniciar()
    #verifica se possui resultado
    if(result != None):
        score_atual = int(result["valor_atual"])
        valor_maximo = int(result["valor_maximo"])
        movimentos = result["movimentos"]
            
        print("Score Atual: %s\n" % score_atual)
        print("Valor Maximo Bloco: %s\n" % valor_maximo)
        print("Movimentos: %s\n" % movimentos)
    else:
        pass