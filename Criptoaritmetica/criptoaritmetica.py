# -*- coding: utf-8 -*-

from mensagens import *
import time, sys, random, re, signal
from random import randrange

class AG():
    
    #########################################
    #                __INIT__               #
    #########################################
    def __init__(self, population, generation, mutation, crossover):
        print MSGC('!')+COR("Que o mais apto sobreviva!",'ciano')
        # vetor de inteiros, com os numeros das letras
        self.CROMOSSOMO = []
        self.LETTERS = []
        self.POPULATION = int(population)
        self.GENERATION = int(generation)
        self.RADIATION = float(mutation)
        self.SEX = float(crossover)
        #self.STRING1 = 'send'
        #self.STRING2 = 'more'
        #self.SAIDA = 'money'
        self.STRING1 = raw_input(MSGC('.')+COR("String 1: ",'ciano')).lower()
        self.STRING2 = raw_input(MSGC('.')+COR("String 2: ",'ciano')).lower()
        self.SAIDA = raw_input(MSGC('.')+COR("Saida : ",'ciano')).lower()
        self.LISTA_SAIDA = []
        self.LISTA_STRING1 = []
        self.LISTA_STRING2 = []
        self.GERACAO = []
        self.ACTUALGEN = 0
        self.VERDADE = [1,0,6,5,2]
        
        for letter in set(self.STRING1+self.STRING2+self.SAIDA):
            self.LETTERS.append(letter)
        
        self.THRESHOLD = len(self.LETTERS)
        
        print '\n'+MSGC('!')+COR("POPULAÇÃO: ",'ciano'),self.POPULATION
        print MSGC('!')+COR("GERAÇÕES: ",'ciano'),self.GENERATION
        print MSGC('!')+COR("MUTAÇÃO: ",'ciano'),self.RADIATION, '%'
        print MSGC('!')+COR("CROSSOVER: ",'ciano'),self.SEX , '%'
        print MSGC('!')+COR("LETTERS: ",'ciano'),self.LETTERS
        
        # procurar a posição relativa da saida no vetor letters e armazenar em uma lista
        for x in list(self.SAIDA):
            for i in self.LETTERS:
                if x == i:
                    self.LISTA_SAIDA.append(self.LETTERS.index(i))
        
        for x in list(self.STRING1):
            for i in self.LETTERS:
                if x == i:
                    self.LISTA_STRING1.append(self.LETTERS.index(i))
        
        for x in list(self.STRING2):
            for i in self.LETTERS:
                if x == i:
                    self.LISTA_STRING2.append(self.LETTERS.index(i))
        
        print '\n'+MSGC('!')+COR("CHAMANDO CHINA",'ciano')
        # calling china to generate population
    
    #########################################
    #                 CHINA                 #
    #########################################    
    def china(self):
        cromossomo = []
        #print '\n'+MSGC('!')+COR("GERANDO %s "%COR(str(self.POPULATION),'branco'),'ciano')+COR("CROMOSSOMOS",'ciano')
        with open ("LOG/FirstGeneration.txt","w") as arquivo:
            #arquivo.write(str(self.LETTERS)+'\n')
            for i in range(0,self.POPULATION):
                while True:
                    cromo = random.sample([0,1,2,3,4,5,6,7,8,9], self.THRESHOLD)
                    if cromo[self.LISTA_SAIDA[0]] == 0 or cromo[self.LISTA_STRING1[0]] == 0 or cromo[self.LISTA_STRING2[0]] == 0:
                        continue
                    else:
                        cromossomo.append(cromo)
                        break
            self.escreveArquivo(arquivo, cromossomo)
        print '\n'+MSGC('OK')+COR("GERADO %s "%COR(str(self.POPULATION),'branco'),'ciano')+COR("CROMOSSOMOS",'ciano')+'\n'
        #self.maxOpressores()
    
    #########################################
    #                OPRESSOR               #
    #########################################
    def opressor(self):
        pass
        #with open ("LOG/FirstGeneration.txt","r") as arquivo:
            #cromossomo = []
            
            #for i in arquivo.read().splitlines():
                #cromossomo.append(i.split())
                
        #enem = list(cromossomo)
        #vestibular = list(cromossomo)
        #poscomp = list(cromossomo)
        
        #executar 10 vezes as 100 gerações para enem
        #self.enem(enem)
        
        #print '\n'
        #self.vestibular(vestibular)
        
        #print '\n'
        #self.poscomp(poscomp)
    
    #########################################
    #               GENERIC                 #
    #########################################
    def genericGen(self,metodo,cromossomo):
        #self.GENERATION = 10000
        # escrever cromossomo no arquivo
        with open ("LOG/{0}/{0}Generation.txt".format(metodo),"w") as arquivo:
            self.escreveArquivo(arquivo, cromossomo)
            
        for self.ACTUALGEN in range(0,self.GENERATION):
           
            # avaliação generica
            self.genericEval(cromossomo,metodo,'w')
            
            # ler arquivo que tem as avaliações
            with open ("LOG/{0}/{0}Notas.txt".format(metodo,self.ACTUALGEN),"r") as arquivo:
                eva = arquivo.read().splitlines()
            #print 'generica ', len(eva)
            # realiza o torneio
            ######################################################################################
            self.torneio(cromossomo,eva)
            
            # adicionar a nova geração aos 100 que ja existem
            with open ("LOG/{0}/{0}Generation.txt".format(metodo),"a") as arquivo:
                self.escreveArquivo(arquivo, self.GERACAO)
           
            # avalia os 60 filhos gerados   
            self.genericEval(self.GERACAO,metodo,'a')
            
            #print 'cromo ', len(cromossomo), ' gera ', len(self.GERACAO)
            
            # Limpando o cromossomo
            cromossomo[:] = []
            #leio meu arquivo novamente com os 160 cromossomos
            with open ("LOG/{0}/{0}Generation.txt".format(metodo),"r") as arquivo:
                for i in arquivo.read().splitlines():
                    cromossomo.append(i.split())
            
            # se quantidade de cromossomos for maior ou igual a 160, eliminar os 60 peores
            if len(cromossomo) >= self.POPULATION+(self.POPULATION*self.SEX):
                cromossomo = list(self.choosenOne(cromossomo, metodo))
            
            # Realiza chamada para mutação
            for x in range(0,int(len(cromossomo)*self.RADIATION)):
                rand = random.choice(cromossomo)
                cromossomo[cromossomo.index(rand)] = (self.raios_gama(rand))
            
            # escrever cromossomo no arquivo
            with open ("LOG/{0}/{0}Generation.txt".format(metodo),"w") as arquivo:
                self.escreveArquivo(arquivo, cromossomo)
                
            #for i in cromossomo:
                #if i[self.LISTA_SAIDA[0]] == 0 or i[self.LISTA_STRING1[0]] == 0 or i[self.LISTA_STRING2[0]] == 0:
                    #print 'deu merda \n'
                    #raw_input()
                    
            self.GERACAO[:] = [] 
            
            #########################################################################################
            sys.stdout.write('\r'+MSGC('OK')+COR("GENERATION {0} ".format(COR(str(self.ACTUALGEN+1),'branco')),'ciano')); sys.stdout.flush()
            
        if len(cromossomo) >= self.POPULATION+(self.POPULATION*self.SEX):
            cromossomo = list(self.choosenOne(cromossomo, metodo))
            
            # Realiza chamada para mutação
            for x in range(0,int(len(cromossomo)*self.RADIATION)):
                rand = random.choice(cromossomo)
                cromossomo[cromossomo.index(rand)] = (self.raios_gama(rand))
            # escrever cromossomo no arquivo
            with open ("LOG/{0}/{0}Generation.txt".format(metodo),"w") as arquivo:
                self.escreveArquivo(arquivo, cromossomo)
            self.genericEval(cromossomo,metodo,'w')
        
        self.ACTUALGEN = 0
   
    #########################################
    #               TORNEIO                 #
    #########################################
    def torneio(self,cromossomo,eva):
        x = 0
        op = []
        pos_op = []
        result = []
        dick = {}
        repetido = []
        aux = []
        
        while x < int(len(cromossomo)*self.SEX):
            #sys.stdout.write('\r'+MSGC('.')+COR("TORNEIO {0} ".format(COR(str(x),'branco')),'ciano')); sys.stdout.flush()
            while (len(op) < 2):
                for i in range(0,3):
                    
                    aux.append(random.choice(cromossomo))
                    # posição do cromossomo
                    pos_op.append(cromossomo.index(aux[i]))
                    # avaliação do cromossomo, na posição do cromossomo
                    result.append(eva[pos_op[i]])
            
                #(avaliação,cromossomo)
                oi = zip(result,aux)
                # coloco os cromossomos em um dicionario, onde chave é a avaliação e valor o cromossomo
                for nota, cromo in oi:
                    dick[nota] = cromo
                    
                # ordeno o resultado da avaliação dos 3 cromossomos escolhidos, assim posso pegar o melhor que j´a nao esta
                result.sort(key=int)

                flag = False
                #print len(aux), x, self.ACTUALGEN
                #print dick
                for each in range(0,len(result)):
                    if not dick[result[each]] in op:
                        op.append(dick[result[each]])
                        flag = True
                    if flag:
                        break
                aux[:] = []
                result[:] = []
                pos_op[:] = []
                dick.clear()

            #print op
            # Verificaç~ao para par de cromossomos
            if x % 2 != 0:
                if cmp(op[0],op[1]) == 0:
                    #print "\n\Para tudo!"
                    raw_input()
                    ##dick[result[0]] = self.raios_gama(dick[result[0]])
                    #x -= 1
                else:
                    #print "entrando\n"
                    flag = self.pmx(op[0],op[1])
                    # se x, quer dizer que deu bosta na hora de cruzar, e gerou filhos que ja existiam
                    if flag:
                        #sys.stdout.write('\r'+MSGC('.')+COR("PAI1 {0} PAI2 {1} ".format(COR(str(dick[result[0]]),'branco'),COR(str(dick[result[1]]),'branco')),'ciano')); sys.stdout.flush()
                        if x != 0:
                            x -= 1
                        else:
                            print "Função Torneio, erro: Execução na primeira geração e engendrado indivíduos iguais aos progenitores!\n"
                            #print "Tecle para sair"
                            raw_input()
                            sys.exit(-1)
            op[:] = []
            
            #print "saiu aqui\n"
            x += 1
        
    #########################################
    #                 FUNK                  #
    #########################################
    def funk(self, cromossomo, eva):
        w = []
        esperado = []
        resultado = 0
        obtido = [0 for i in range(0,len(self.LISTA_SAIDA))]
        
        # pegar somente os digitos do cromossomo
        for i in cromossomo:
            if i.isdigit(): 
                w.append(int(i))
        for i in self.LISTA_SAIDA:
            esperado.append(w[i])
        
        flag = False
        
        # considerando que as duas strings sao do mesmo tamanho
        for i in range(len(self.LISTA_STRING1)-1,-1,-1):
            carry = 1 if flag else 0
            soma = w[self.LISTA_STRING1[i]] + w[self.LISTA_STRING2[i]] + carry
            if soma >= 10:
                flag = True
                obtido[i+1] = (soma-10)
            else:
                obtido[i+1] = (soma)
                flag = False
        
        obtido[0] = 1 if flag else 0
        
        ############################################
        #    ESTA OK, CHECADA AVALIAÇÃO ENEM OK    #
        ############################################
        if eva == 'enem':
            resultado = (self.universal(esperado) - self.universal(obtido))
        
        ############################################
        #  ESTA OK, CHECADA AVALIAÇÃO VESTIBULAR   #
        ############################################
        elif eva == 'vestibular':
            # soma das diferenças entre a soma desejada e a soma real digito a butt digito
            dif = [0 for i in range(0,len(esperado))]
            for i in range(len(esperado)-1,-1,-1):
                dif[i] = esperado[i] - obtido[i]
            for i in dif:
                resultado += abs(i)
            #print 'ESPERADO : {0} OBTIDO : {1} RESULTADO : {2} DIF : {3}'.format(esperado,obtido,resultado,dif)
            #raw_input()
        
        ############################################
        #  ESTA OK, CHECADA AVALIAÇÃO poscomp ??   #
        ############################################
        #Produto das diferenças entre a soma desejada e a soma real dígito a dígito.
        elif eva == 'poscomp':
            resultado = 1
            flag = True
            dif = [0 for i in range(0,len(esperado))]
            for i in range(len(esperado)-1,-1,-1):
                dif[i] = esperado[i] - obtido[i]
            
            print dif
            raw_input()
            
            for i in dif:
                if i == 0:
                    continue
                resultado *= abs(i)
                
            if (self.VERDADE,obtido) == 0:
                print 'achei'
                raw_input()
                
            if resultado == 0:
                print 'ESPERADO : {0} OBTIDO : {1} RESULTADO : {2} DIF : {3}'.format(esperado,obtido,resultado, dif)
                raw_input()
            
        if resultado == 0:
            if not(cmp(self.VERDADE,obtido) == 0):
                with open ("LOG/{0}/AprovadosErroneamente.txt".format(eva),'a') as aprovado:
                        aprovado.write("\nPOPULAÇÃO : {} GERAÇÃO : {} MUTAÇÃO : {} CROSSOVER : {} MÁSCARA : {} \nGENERATION : {} CROMOSSOMUS : {}\n".format(self.POPULATION, self.GENERATION, self.RADIATION, self.SEX, self.LETTERS, self.ACTUALGEN, cromossomo))
                        send = []
                        more = []
                        money = []
                        for x in self.LISTA_SAIDA:
                            money.append(cromossomo[int(x)])
                        for x in self.LISTA_STRING1:
                            send.append(cromossomo[int(x)])
                        for x in self.LISTA_STRING2:
                            more.append(cromossomo[int(x)])
                        aprovado.write("SEND : {0} MORE : {1} MONEY : {2}\n".format(send,more,money))
                #print '\r'+MSGC('ERRO') + 'ESPERADO : {0} OBTIDO : {1} RESULTADO : {2} METODO : {3} CROMOSSOMO : {4}'.format(esperado,obtido,resultado,eva,cromossomo)
                resultado = 9999999
                #raw_input("CONTINUE?")
            
        return abs(resultado)
    
    #########################################
    #                  PMX                  #
    #########################################
    def pmx(self, pai1, pai2):
        # duplicar os pais
        filho1 = list(pai1)
        filho2 = list(pai2)
        flag = True
        flag2 = True
        flagSair = True
        
        while (cmp(filho1,pai1) == 0 or cmp(filho2,pai2) == 0) and flagSair == True:
            
            # escolher randomicamente uma janela de troca
            janela = random.choice(range(1,len(pai1)-2))
            pos = random.choice(range(0,(len(pai1)-1)-janela))
            
            #sys.stdout.write('\r'+MSGC('.')+COR("PAI1 {0} PAI2 {1}  JANELA {2} POS {3}".format(COR(str(pai1),'branco'),COR(str(pai2),'branco'),COR(str(janela),'branco'),COR(str(pos),'branco')),'ciano')); sys.stdout.flush()
            
            # executar troca de acordo com janela e pos inicial
            for i in range(pos,pos+janela):
                filho2[i] = pai1[i]
                filho1[i] = pai2[i]
                
            self.troca(filho1, pos, janela, filho2)
            self.troca(filho2, pos, janela, filho1)
            
            
            if cmp(filho1,pai1) == 0 or cmp(filho2,pai2) == 0:
                if cmp(pai2,pai1) == 0:
                    #print "\n\nmerda"
                    raw_input()
                #print "\t",self.ACTUALGEN,"\n"
                #print filho1, pai1,"\n", filho2,pai2
                flagSair = False
                #filho2 = self.raios_gama(filho2)
                #filho1 = self.raios_gama(filho1)
                
            else:
                # Só adiciono os filos se não estive sido criados antes
                if not (filho1 in self.GERACAO or filho2 in self.GERACAO):                        
                    self.GERACAO.append(filho1)
                    self.GERACAO.append(filho2)
                    flag2 = False
                    flag = False
        if not (flagSair):
            pass
            #print "certo paulo"
        if flag:
            if not (filho1 in self.GERACAO or filho2 in self.GERACAO):                        
                self.GERACAO.append(filho1)
                self.GERACAO.append(filho2)
                flag2 = False
                flagSair = False
        return flagSair
    
    #########################################
    #                 ENEM                  #
    #########################################
    def enem(self, cromossomo):
        self.genericGen('enem',cromossomo)
        
    #########################################
    #               VESTIBULAR              #
    #########################################
    def vestibular(self, cromossomo):
        self.genericGen('vestibular',cromossomo)
    
    #########################################
    #                POSCOMP                #
    #########################################
    def poscomp(self, cromossomo):
         self.genericGen('poscomp',cromossomo)
        
    #########################################
    #                TROCA                  #
    #########################################
    def troca(self, filho, pos, janela, filho2):
        flag = True
        if (len(filho) == len(set(filho))):
            flag = False
        while (flag):
            dupfilho1 = self.duplicados(filho, pos, janela)
            # Verificamos agora se existe números duplicados no filho um, caso exista
            # iremos então ver qual número dentro do outro filho, dentro da area de swap,
            # está referente a este número duplicado:
            repetidos = []
            numbers = [ int(x) for x in dupfilho1 ]
            for i in numbers:
                repetidos.append(filho[i])
            while (len(repetidos) > 0):
                #print "Executara troca\n"
                numero = repetidos[0]
                posicao = dupfilho1[0]
                for x in range(pos,pos+janela):
                    if (filho[x] == numero):
                        filho[posicao] = filho2[x]
                repetidos.remove(numero)
                dupfilho1.remove(posicao)
                
            if filho[self.LISTA_SAIDA[0]] == 0 or filho[self.LISTA_STRING1[0]] == 0 or filho[self.LISTA_STRING2[0]] == 0:
                print ' EAAAAAAEEE '
                raw_input()
                #continue
            if (len(filho) == len(set(filho))):
                flag = False
    
    #########################################
    #              CHOOSENONE               #
    #########################################
    def choosenOne(self,cromossomo, metodo):
        siga = {}
        cromossomus = []
        
        # ler arquivo que tem as avaliações
        with open ("LOG/{0}/{0}Notas.txt".format(metodo,self.ACTUALGEN),"r") as arquivo:
            eva = arquivo.read().splitlines()
            
        # faço um par ordenado (avaliação,cromossomo)
        oi = zip(eva,cromossomo)
        # adicionar no dicionario como chave a a avaliação e como valor o cromossomo correspondentes
        for nota, cromo in oi:
            siga.update({nota:cromo})
            
        # sorteia a lista com os resultados, assim os melhores ficam nas primeiras posições
        eva.sort(key=int)
        
        # pegar os 100 melhores e retornar
        for i in range(0,self.POPULATION):
            cromossomus.append(siga[eva[i]])
        
        return cromossomus
    
    #########################################
    #            GENERIC EVAL               #
    #########################################
    def genericEval(self, cromossomo, metodo, abertura):
       with open ("LOG/{0}/{0}Notas.txt".format(metodo),abertura) as arquivo:
            for i in cromossomo:
                result = self.funk(i,metodo)
                if result == 0:
                    with open ("LOG/{0}/Aprovados{0}.txt".format(metodo),'a') as aprovado:
                        aprovado.write("\nPOPULAÇÃO : {} GERAÇÃO : {} MUTAÇÃO : {} CROSSOVER : {} MÁSCARA : {} \nGENERATION : {} CROMOSSOMUS : {}\n".format(self.POPULATION, self.GENERATION, self.RADIATION, self.SEX, self.LETTERS, self.ACTUALGEN, i))
                        send = []
                        more = []
                        money = []
                        for x in self.LISTA_SAIDA:
                            money.append(i[int(x)])
                        for x in self.LISTA_STRING1:
                            send.append(i[int(x)])
                        for x in self.LISTA_STRING2:
                            more.append(i[int(x)])
                        aprovado.write("SEND : {0} MORE : {1} MONEY : {2}\n".format(send,more,money))
                arquivo.write(str(result)+'\n')
    
    #########################################
    #              RAIOS GAMA               #
    #########################################
    def raios_gama(self, cromo):
        cromossomo = list(cromo) 
        #print 'antes : ', cromossomo
        aux = cromossomo[-1]
        cromossomo[-1] = cromossomo[0]
        cromossomo[0] = aux
        #print 'depois : ', cromossomo
        return cromossomo

    #########################################
    #              DUPLICADOS               #
    #########################################
    def duplicados(self, filho, pos, janela):
        #if raw_input():
            #pass
        # posição das duplicatas em filho1 e filho2
        dupfilho = []
        # pegar a posição das duplicatas que não estão na janela
        for i in range(0,len(filho)):
            for x in range(0,len(filho)):
                if i != x:
                    if not (i in range(pos,pos+janela)):
                        if filho[i] == filho[x]:
                            dupfilho.append(i)
        return dupfilho

    #########################################
    #               ARQUIVO                 #
    #########################################
    def escreveArquivo(self, arquivo, cromossomo):
        for i in cromossomo:
            for x in i:
                arquivo.write(str(x) + ' ')
            arquivo.write('\n')

    #########################################
    #           CONVERTE CHESSUS            #
    #########################################
    def universal(self,lista):
        dec = 1
        resultado = 0
        for i in range(len(lista)-1,-1,-1):
            resultado += lista[i] * dec
            dec *= 10
        return resultado
    
    def loop(self, metodo):
        with open ("LOG/FirstGeneration.txt","r") as arquivo:
                cromossomo = []
            
                for i in arquivo.read().splitlines():
                    cromossomo.append(i.split())
        
        for x in range(0,10):
            
            copy = list(cromossomo)
            sys.stdout.write(MSGC('OK')+COR("\t\t\t\t   {1} {0}                   ".format(COR(str(x+1),'branco'),COR(metodo,'branco')),'ciano')); sys.stdout.flush()
            
            if metodo == 'enem':
                self.enem(copy)
            elif metodo == 'vestibular':
                self.vestibular(copy)
            elif metodo == 'poscomp':
                self.poscomp(copy)
                
            #print MSGC('.')+COR('GERANDO POPULAÇÃO INICIAL','ciano')
            #self.china()
    
    #########################################
    #             MAXOPRESSORES             #
    #########################################
    def maxOpressores(self):
        
        print MSGC('.')+COR('GERANDO POPULAÇÃO INICIAL','ciano')
        self.china()
        
        self.loop('enem')
        
        #print MSGC('.')+COR('GERANDO POPULAÇÃO INICIAL\n','ciano')
        #self.china()
        self.loop('vestibular')
        
        #print MSGC('.')+COR('GERANDO POPULAÇÃO INICIAL\n','ciano')
        #self.china()
        self.loop('poscomp')
        
        sys.stdout.write(MSGC('OK')+COR("TIAU <3                                                   \n",'ciano')); sys.stdout.flush()
            
#########################################
#                  MAIN                 #
#########################################
if __name__=='__main__':
    
    # criar configurações diferentes 16
    # rodar 10 vezes para cada configuração a enem
    # cada configuração é um diretorio
    
    print MSGC('OK')+COR("Inicializando algoritmo genético",'ciano')
    string = []
    while True:
        try:
            with open ("LOG/config.txt","r") as arquivo:
                sys.stdout.write(MSGC('!')+COR("Usar arquivo de configuração ? (s/n): ",'verde'))
                res = raw_input().lower()
                if res == 's':
                    string = arquivo.readlines()
                    break
                else:
                    raise Exception('error')
        except Exception, error:
            try:
                print MSGC('!')+COR("Insira os valores: ",'ciano')
                with open ("LOG/config.txt","w") as arquivo:
                    string.append(raw_input(MSGC('.')+COR("Population: ",'reverso'))+'\n')
                    string.append(raw_input(MSGC('.')+COR("Generation: ",'reverso'))+'\n')
                    string.append(raw_input(MSGC('.')+COR("Mutation: ",'reverso'))+'\n')
                    string.append(raw_input(MSGC('.')+COR("Crossover: ",'reverso'))+'\n')
                    arquivo.writelines(string)
                #ag = AG(string[0],string[1],string[2],string[3])
            except Exception, error:
                print error
    try:
        ag = AG(string[0].replace("\n", ""),string[1].replace("\n", ""),string[2].replace("\n", ""),string[3].replace("\n", ""))
        #ag.china()
        ag.maxOpressores()
        #print '\n'
    except Exception, error:
        print MSGC('ERRO')+COR("UPS, ALGUMA COISA ERRADA NÃO ESTÁ CERTA : ",'ciano')+COR(str(error),'branco')
        