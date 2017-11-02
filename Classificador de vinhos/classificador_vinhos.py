import tensorflow as tf
from numpy import genfromtxt
import numpy as np
import sklearn
import sys
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#Fonte dos dados
#https://archive.ics.uci.edu/ml/datasets/wine

#Tarefa de casa
#http://archive.ics.uci.edu/ml/datasets/Wine+Quality

'''
"fixed acidity";        0
"volatile acidity";     1
"citric acid";          2
"residual sugar";       3
"chlorides";            4
"free sulfur dioxide";  5
"total sulfur dioxide"; 6
"density";              7
"pH";                   8
"sulphates";            9
"alcohol";              10
"quality"               11
'''

if __name__ == "__main__":
    run_number = int(sys.argv[1])

    #Carrega CSV
    data = genfromtxt('winequality-white.csv', delimiter=';')

    #Separa features das respostas
    data_x = data[:,0:7]
    data_y = data[:,-1]

    #Separa conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.30, random_state=42)

    #Normaliza dados
    #X_train = sklearn.preprocessing.normalize(X_train, norm='l2')
    #X_test = sklearn.preprocessing.normalize(X_test, norm='l2')

    #Numero de neuronios na camada escondida
    n_h = 5
    #Numero de neuronios na camada de saida
    n_o = np.count_nonzero(np.unique(data_y))
    #Numero de features de entrada
    n_i = X_train.shape[1]

    #Define variaves de entrada do grafo
    X = tf.placeholder(tf.float32, [None, n_i])
    Y = tf.placeholder(tf.int64   , [None])

    y = tf.one_hot(Y, on_value = 1.0, off_value = 0.0,depth=7)

    #Inicializa pesos para a camada escondida
    h_w = tf.Variable(tf.random_normal([n_i, n_h]))
    h_b = tf.Variable(tf.zeros([n_h]))

    #Inicializa pesos para a camada de saida
    o_w = tf.Variable(tf.random_normal([n_h, n_o]))
    o_b = tf.Variable(tf.zeros([n_o]))

    #Calcula o feedfoward
    out_h = tf.nn.sigmoid(tf.add(tf.matmul(X, h_w), h_b))
    out = tf.nn.sigmoid(tf.add(tf.matmul(out_h, o_w), o_b))

    #Calcula o erro quadratico medio em todos os dados
    error = tf.subtract(out, y)
    mse = tf.reduce_mean(tf.square(error))

    #Executa o backpropagation com SGD
    starter_learning_rate = 0.1
    global_step = tf.Variable(0, trainable=False)
    lr = tf.train.exponential_decay(starter_learning_rate, global_step, 100000, 0.97, staircase=True)
    train = tf.train.GradientDescentOptimizer(lr).minimize(mse)

    #Calcula a acuracia da rede
    correct_prediction = tf.equal(tf.argmax(out, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    #inicializa a sessao do TF
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    erro_treino = []
    erro_teste = []
    acc_treino = []
    acc_teste = []

    epoca = 0
    max_epochs = 6000

    while epoca < max_epochs:
        epoca += 1
        feed_dict = {X: X_train, Y: y_train}
            #Executa sessao que ira treinar a rede
        erro, _, acc = sess.run([mse, train, accuracy], feed_dict=feed_dict)
        #print('Epoca:', '%04d' % (epoca), 'perda =', '{:.9f}'.format(erro), 'Acuracia de Treino = ','{:.2f}'.format(acc))
        erro_treino.append(erro)
        acc_treino.append(acc)
        
        feed_dict = {X: X_test, Y: y_test}
            #Executa sessao que ira avaliar a rede com os dados de teste
        erro, acc = sess.run([mse, accuracy], feed_dict=feed_dict)
        #print('           perda de teste =', '{:.9f}'.format(erro), 'Acuracia de Teste = ','{:.2f}'.format(acc))
        erro_teste.append(erro)
        acc_teste.append(acc)


    #Plota os graficos de erro e acuracia
    fig, axs = plt.subplots(1,2,figsize=(15,5))
    axs[0].set_xlabel('epocas')
    axs[0].set_ylabel('erros')
    axs[0].set_title('Vinhos')

    red_patch = mpatches.Patch(color='red', label='Erro treino')
    blue_patch = mpatches.Patch(color='blue', label='Erro validacao')
    axs[0].legend(handles=[red_patch,blue_patch])

    axs[0].axis([0.0, epoca, 0.0, np.amax([erro_treino,erro_teste])])
    axs[0].plot(np.arange(0.0, epoca , 1.0),erro_treino,'r-')  
    axs[0].plot(np.arange(0.0, epoca , 1.0),erro_teste,'b-')


    axs[1].set_xlabel('epocas')
    axs[1].set_ylabel('acertos')
    axs[1].set_title('Vinhos')

    red_patch = mpatches.Patch(color='red', label='ACC treino')
    blue_patch = mpatches.Patch(color='blue', label='ACC validacao')
    axs[1].legend(handles=[red_patch,blue_patch])

    axs[1].axis([0.0, epoca, 0.0, 1.0])
    axs[1].plot(np.arange(0.0, epoca , 1.0),acc_treino,'r-')  
    axs[1].plot(np.arange(0.0, epoca , 1.0),acc_teste,'b-')

    name = str(n_h) + "-" + str(starter_learning_rate) + "-" + str(max_epochs) + "-" + str(run_number) + ".png"
    fig.savefig('result/'+name)

    #plt.show()
