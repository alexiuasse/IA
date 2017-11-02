# -*- coding: cp1252 -*-
from random import choice
from numpy import array, dot, random

# dot : faz o produto em arrays
# random : gera numeros aleatorios
# choice : escolhe um item randômico dentro de uma lista
# array : vetor/matriz

ERRO = '\033[91m[ERRO]\033[0m'
LOGIC = '\033[1m[X0,X1,BIAS]\033[0m'
OK = '\033[92m[RESULTADO]\033[0m'
ESPERADO = '\033[94m[ESPERADO]\033[0m'
PESO = '\033[95m[PESO]\033[0m'
INTE = "\033[92m\033[1m[Número de interações [0,300] ]: \033[0m"
FL = "\033[92m\033[1m[Função Lógica]: \033[0m"
TA = "\033[92m\033[1m[Taxa de Aprendizado]: \033[0m"
TERMINADO = '\033[94m\033[1m[TERMINADO, INTERAÇÕES]\033[0m'
OBS = "\033[91m\033[1m[OBS]\033[93m Devido ao uso de pesos aleatórios iniciais, a quantidade de interações sofrerá algumas anomalias. Bias como 0 somente dará certo com implicação e nor.\033[0m"
YB = "\033[93m\033[1m\033m"
CONTINUA = "\033[94m\033[1m[CONTINUAR [\033[92mENTER\033[94m/\033[91mN\033[94m] ]: \033[0m"

degrau = lambda x: 0 if x < 0 else 1     # Função retorna 0 se x < 0 e 1 se x > 0
# implica bias 0 OK
# and bias 0 NOT OK
# or bias 0 NOT OK
# nand bias 0 NOT OK
# nor bias 0 OK
bias = 1
# array[entrada1,entrada2,bias], resultado esperado
implica = [
    (array([0,0,bias]), 1),
    (array([0,1,bias]), 1),
    (array([1,0,bias]), 0),
    (array([1,1,bias]), 1),
]
ou = [
    (array([0,0,bias]), 0),
    (array([0,1,bias]), 1),
    (array([1,0,bias]), 1),
    (array([1,1,bias]), 1),
]
e = [
    (array([0,0,bias]), 0),
    (array([0,1,bias]), 0),
    (array([1,0,bias]), 0),
    (array([1,1,bias]), 1),
]
nand = [
    (array([0,0,bias]), 1),
    (array([0,1,bias]), 1),
    (array([1,0,bias]), 1),
    (array([1,1,bias]), 0),
]
nor = [
    (array([0,0,1]), 1),
    (array([0,1,1]), 0),
    (array([1,0,1]), 0),
    (array([1,1,1]), 0),
]
logic_func = {'implica':implica, 'or':ou, 'and':e, 'nand':nand, 'nor':nor}

w = random.rand(3)      # Escolher três números randomicos para os pesos (entre 0 e 1)
print OBS
print PESO,YB,w
errors = []             # Erros
while True:
    x = raw_input(CONTINUA).lower()
    if x == 'n':
        break
    while True:
        try:
            aprendizado = float(raw_input(TA))
            print FL,YB,logic_func.keys()
            logic = raw_input(FL)
            if not logic in logic_func.keys():
                raise Exception(ERRO)
            for row in logic_func[logic]:
                print YB,"\t".join(([str(x) for x in row]))
            n = int(raw_input(INTE))
            if n > 300:   # Numero maximo de interações
                raise Exception(ERRO)   # Caso passe de 300 lançar erro
            break
        except Exception:
            print ERRO
    cont_ = 0
    flag = True # Para perguntar se quer continuar a cada interação
    for i in xrange(n):
        if cont_ >= 4: break
        print '\n\033[94m\033[1m[INTERAÇÃO]: ',i,'\033[0m\n'
        for x, expected in logic_func[logic]:
            result = dot(w, x)
            error = expected - degrau(result)
            if error == 0: cont_ = cont_ + 1
            else: cont_ = 0
            errors.append(error)
            w += aprendizado * error * x
            print LOGIC,YB,x,ESPERADO,YB,expected
            print OK,YB,result,ERRO,YB,error
            print PESO,YB,w,'\033[0m\n'
        if flag:
            continua = raw_input(CONTINUA).lower()
            if continua == 'n':
                break
    print ERRO,YB,errors
    print TERMINADO,YB,i
    print LOGIC,PESO,"\033[95m\033[1m-> FINAL"
    for x, _ in logic_func[logic]:
        result = dot(x, w)
        print("{}: {} -> {}".format(x[:3], result, degrau(result)))
print '\033[93mBye ... \033[0m'
