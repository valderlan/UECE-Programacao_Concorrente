
import threading
import time
import random
from datetime import datetime
from queue import Queue
#Nesse programa está usando a instânca Queue da linguagem Python
#a queue jé tem uma condição de bloqueio, e assim não precisamos nos preocupar.
#aluno: Francisco Valderlan Jorge Nobre - Matricula: 1493327

id = 0  #contador usado para ser usado na id
cont_1 = 0 #contador de avioes que desejam decolar
cont_0 = 0 #contador de avioes que desejam pousar
muda = False #para controle da quantidade de aeronaves
muda1 = False #para controle da quantidade de aeronaves
aux = 0 #variavel auxiliar 

class Aircraft(): # Objeto aeronave, tem os atributos do aviao e o tipo se quer pousar ou decolar
    def __init__(self, id,t_nascimento,tempo_voo):
        global max 
        self.id = id #identificacao do voo e thread
        self.nascimento = t_nascimento#self.get_tempo() #tempo em que foi criado o aviao
        self.t_voo = tempo_voo 
        self.acao = self.get_acao() #tipo de acao: decolar ou pousar
        self.t_inicio = 0 #tempo onde se inicia a acao
        self.t_fim = 0 #tempo onde termina a acao
        self.t_espera = 0
        #print("O avião {}: criado".format(id))
       
    def get_acao(self): #obtem a acao da aeronave
        global muda, muda1, cont_1, cont_0
        tipo = random.randint(0, 1) #realiza o sorteio entre os dois tipos: 0 para pousar e 1 para decolar
        if tipo == 1 and not muda: #tipo 1 a acao sera de decolar
            #self.t_voo = None
            if cont_1 <= (max/2):
                cont_1 = cont_1 + 1
                if cont_1 > (max/2):
                    muda = True
                
        if tipo == 0 and not muda1: #tipo 0 a acao sera de pousar
            if cont_0 <= (max/2):
                cont_0 = cont_0 + 1
                if cont_0 > (max/2):
                    muda1 = True
        #controle para garantir a divisão igual de aeronaves que querem decolar e pousar
        if tipo == 1 and muda: 
            tipo = 0
            cont_0 = cont_0 + 1
            
        if tipo == 0 and muda1:
            tipo = 1
            #self.t_voo = None
            cont_1 = cont_1 + 1
        return tipo
#--------------------------------------------------------------------------------------
def get_tempo(): #obtem o tempo
    d = datetime.today() #pega a hora do sistema na hora, para ser a hora de criacao do aviao
    tempo_seg = (int(d.minute)*60) + int(d.second) 
    tempo = d.strftime('%H:%M:%S')
    return tempo, tempo_seg        

def get_tempo_comparar(): #obtem o tempo atual para comparar o tempo de combustivel
    a = datetime.today()
    tempo_atual = (int(a.minute)*60) + int(a.second)
    return tempo_atual

def pousar(av): #funcao que cuidara da acao de pousar
        print("O avião {}: Iniciou a ação de pousar".format(av.id))
        pista.acquire()
        av.t_inicio, aux = get_tempo()
        av.t_espera = aux - av.t_voo
        #Nesse ponto sao os 5s que o aviao fica na fase da espera
        time.sleep(10)
        print("O avião {}: pousou".format(av.id))
        av.t_fim, aux = get_tempo()
        aux = 0
        pista.release()   

def decolar(av): #funcao que cuidara da acao de decolar
        print("O avião {}: Iniciou a ação de decolar".format(av.id))
        pista.acquire()
        av.t_inicio, aux = get_tempo()
        av.t_espera = aux - av.t_voo
        #Nesse ponto sao os 5s que o aviao fica na fase da espera
        print('O avião {}: esperando para decolar'.format(av.id))
        time.sleep(5)
        #Nesse ponto sao os 5s que o aviao finalmente inicia a decolagem
        time.sleep(5)
        print("O avião {}: Decolou".format(av.id))
        av.t_fim, aux = get_tempo()
        aux = 0
        pista.release()

def Produzir_Trafego(terminar,max):
    
    global aeronaves
    terminar.put(False) #queue que irá fazer o controle de sincronia entre o produtor e consumidor.
    #put() tem a lógica de adquirir o bloqueio antes de inserir os dados
    #também verifica se a queue tá cheia, se estiver ela chama um wait() internamente e o produtor espera.
    #put() também tem a lógica para fazer a notificação
    for id in range(max):
        t_nascimento, tempo_voo = get_tempo()
        aviao = Aircraft(id,t_nascimento,tempo_voo)
        #colocar os tipos de aeronaves nos buffers correspondentes
        if (aviao.acao==0):
            buffer_pouso.append(aviao)
        elif (aviao.acao==1):
            buffer_dec.append(aviao)
        #----------------------------------------------------------
        aeronaves.append(aviao) #lista para a realização das operações
        aeronaves1.append(aviao) #lista para o relatório
        time.sleep(7) #tempo de espera para criar uma nova aeronave
    terminar.put(True)

def Consumir_Trafego(aeronaves,terminar):
    
    while True:
        print()
        if aeronaves:
            av = aeronaves.pop(0) #retira a primeira aeronave que estiver presente na queue
            #Espaço para as politicas - regras para o consumo
            #caso um dos buffers passe de 3 lugares o programa irá parar dando a mensagem a baixo
            if (((len(buffer_pouso)) > 3) or (len(buffer_dec)) > 3): 
                #raise 'Houve Acidente'
                print('houve acidente: ', get_tempo())
            
            #caso não tenha aviao para pousar e o buffer de decolar não estiver vazio
            #será dado a permissão para o aviao decolar     
            elif (av.acao == 1) and ((((len(buffer_pouso)) == 0) and (len(buffer_dec)) !=0)):
                aviao0=buffer_dec.pop(0) #retira o primeiro aviao do buffer de decolagem
                decolar(aviao0) #chama a função de decolar
            
            #caso que o avião deseja decolar, mas tem avião no buffer que já deseja pousar
            #então será dada prioridada para o avião que deseja pousar
            elif (av.acao == 1) and (((len(buffer_pouso)) != 0) and ((len(buffer_dec)) < 3)):
                #avião que desejava decolar é recolocado no inicio da fila novamente para
                #ser chamado na sua tentativa seguinte
                aeronaves.insert(0,av)
                aviao0=buffer_pouso.pop(0)
                pousar(aviao0)
            #caso o aviao deseja decolar, o seu buffer esteja cheio e o buffer de pouso nao
            #eh testado se o primeiro a pousar tem tempo de combustivel, se tiver sera
            #permitido o aviao decolar, se nao o aviao ira pousar e o aviao que desejava decolar
            #sera recolocado no inicio da fila
            elif (av.acao == 1) and (((len(buffer_pouso)) != 0) and ((len(buffer_dec)) == 3)):
                aviao1 = buffer_pouso.pop(0)
                
                if ((aviao1.t_voo + 30) - get_tempo_comparar()) in range(11,31):
                    buffer_pouso.insert(0,aviao1)
                    aviao0=buffer_dec.pop(0)
                    decolar(aviao0)
                    
                else: #caso o tempo de combutivel esteja menor, entao vai pousar
                    aeronaves.insert(0,av)
                    pousar(aviao1)
            
            #caso o aviao que queria pousar já estiver pousado e seu buffer vazio, pois tinha sido
            #recolado na fila principal, entao sera tirado um aviao que deseja decolar do buffer de decolagem
            elif (av.acao == 0) and ((((len(buffer_pouso)) == 0) and (len(buffer_dec)) !=0)):
                aviao0=buffer_dec.pop(0) #retira o primeiro aviao do buffer de decolagem
                decolar(aviao0) #chama a função de decolar        
            
            #caso o buffer de decolagem estiver menor do que 3 e o avião selecionado deseja pousar
            #caso o buffer de pouso não esteja vazio, a prioridade será dada ao avião que deseja pousar
            elif (av.acao == 0) and (((len(buffer_dec)) < 3) and ((len(buffer_pouso)) != 0)):
                aviao0=buffer_pouso.pop(0)
                pousar(aviao0)
           
            #caso o buffer de decolagem estiver cheia e o avião selecionado deseja pousar
            #será verificado se tem combustível, se tiver ele irá esperar e
            #será retirado o primeiro avião do buffer de decolagem para decolar
            elif (av.acao == 0) and ((len(buffer_dec)) == 3) and ((len(buffer_pouso))!=0): 
                #avião que desejava pousar é recolocado no incio da fila novamente para 
                #ser chamado na sua tentativa seguinte
                aviao0=buffer_pouso.pop(0)
                
                if ((int(aviao0.t_voo) + 30) - int(get_tempo_comparar())) in range(11,31):
                    aeronaves.insert(0,av)
                    buffer_pouso.insert(0,aviao0) 
                    aviao0=buffer_dec.pop(0)
                    decolar(aviao0)
                    
                else: #caso o tempo de combutivel esteja menor, entao vai pousar
                    #aviao0=buffer_pouso.pop(0)
                    pousar(aviao0)
                   
                    
            #print()
            #-------------------------------------------------------------------------------    
        else:
            sair = terminar.get() #Se o produtor não tiver ainda produzido, esse get irá colocar o consumidor na espera
            #get() tem a lógica de adquirir o bloqueio antes de remover os dados
            #também verifica se a queue está vazia, se estiver ela chama um wait() internamente e o consumidor espera
            #get() também tem a lógica para fazer a notificação
            if sair == True: #quando o produtor tiver produzido tudo o get() anterior irá obter um True
                break

#--------- main --------------------------------------------------------------
pista = threading.BoundedSemaphore(value=1) 
aeronaves1 = [] #lista que irá armazenar o históricos dos avioes para usar no relatório
aeronaves = [] #lista que irá armazenar o históricos dos avioes para usar no consumidor
buffer_dec = [] #buffer para decolagem
buffer_pouso = [] #buffer para pouso
terminar = Queue() #fila de controle entre as funções de Produzir e Consumir o tráfego
max = 18 #max representa o número máximo de aeronaves   
thread0 = threading.Thread(target=Produzir_Trafego,args=[terminar,max])
thread1 = threading.Thread(target=Consumir_Trafego,args=[aeronaves,terminar])
thread0.start()
thread1.start()
thread0.join()
print('Todo o tráfego foi produzido!')
thread1.join()
print('Todas os aviões realizaram as suas ações!')
#------------------------------------------------------------------------------    
    
#--------- gera relatorio -----------------------------------------------------
#--------- gera um arquivo txt com as acoes -----------------------------------    
with open("relatorio.txt", "w") as arquivo:
    for i in range(0,max):
        if aeronaves1[i].acao == 1:
            print("Voo {} | deseja decolar ação {} | criado em {}, começou em {} e terminou em {} - tempo de espera {}".format(aeronaves1[i].id,aeronaves1[i].acao,aeronaves1[i].nascimento,aeronaves1[i].t_inicio,aeronaves1[i].t_fim,aeronaves1[i].t_espera))
            arquivo.writelines(str("Voo {} | deseja decolar ação {} | criado em {}, começou em {} e terminou em {} - tempo de espera {}\n".format(aeronaves1[i].id,aeronaves1[i].acao,aeronaves1[i].nascimento,aeronaves1[i].t_inicio,aeronaves1[i].t_fim,aeronaves1[i].t_espera)))
        if aeronaves1[i].acao == 0:
            print("Voo {} | deseja pousar  ação {} | criado em {}, começou em {} e terminou em {} - tempo de espera {}".format(aeronaves1[i].id,aeronaves1[i].acao,aeronaves1[i].nascimento,aeronaves1[i].t_inicio,aeronaves1[i].t_fim,aeronaves1[i].t_espera))
            arquivo.writelines(str("Voo {} | deseja pousar  ação {} | criado em {}, começou em {} e terminou em {} - tempo de espera {}\n".format(aeronaves1[i].id,aeronaves1[i].acao,aeronaves1[i].nascimento,aeronaves1[i].t_inicio,aeronaves1[i].t_fim,aeronaves1[i].t_espera)))
arquivo.close()

