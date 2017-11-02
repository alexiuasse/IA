#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define ncesc           2
#define entrada         2
#define saida           2
#define exemplos        10

int main(){	
  float w[saida][ncesc],  
	W[ncesc][entrada], 
	errodes, 
	Erroinst,
	Erromg = 0,             // Erro medio geral
	erro[saida], 
	niesc[ncesc], 
	ni[saida], 
	biasesc[ncesc], 
	biass[saida], 
	eta, 
	phiesc[ncesc], 
	phi[saida], 
	phi1esc[ncesc], 
	phi1[saida], 
	delta[saida], 
	deltaesc[ncesc];
  int x ,  y,  cont2,  contt,  epocas,  funcao;
  float entradas[entrada][exemplos], saidas[saida][exemplos];
  
  system ("clear");
  
  printf(" Bias e pesos iniciais...\n");
  for ( y = 0; y < ncesc; y++){
      
      for (x = 0; x <saida; x++){
	  w[x][y] 	= rand()%2 + .5;	                               // Inicializa os pesos da camada de entrada
      }
      
      for (x = 0; x <saida; x++){
	  W[x][y] 	= rand()%2 + .5;	                              // Inicializa os pesos da camada oculta
      }
      biasesc[y] 	= rand()%2;	                             		// Inicializa os pesos da bias     
  }
  
  for (x = 0; x <saida; x++){
    biass[x] 	= rand()%2 + .5;
  }
  
  for (y = 0; y < saida; y++)
    printf("Neuronio de saida: bias[%d] = %f\n",  y, biass[y]);
  
  for (y = 0; y < ncesc; y++)
    printf("Neuronio da camada escondida: bias[%d] = %f\n",  y, biasesc[y]);
  
  printf("Entre com o número de epocas de treinamento:\n");
  scanf("%d",&epocas);
  
  printf("Entre com os vetores de exemplos de treinamento de entrada:\n");
  for(x=0; x < entrada; x++){
      for(y =0; y < exemplos; y++){
          printf("Entrada %d : Neuronio  %d: ",x+1,y+1);
	scanf("%f", &entradas[x][y]);
      }
  }
  
  printf("Entre com os vetores de exemplos de treinamento de saida:\n");
  for(x=0; x < entrada; x++){
      for(y =0; y < exemplos; y++){
          printf("Saida %d : Neuronio %d:",x+1,y+1);
	scanf("%f", &saidas[x][y]);
      }
  }
  
  printf("Entre com o valor da taxa de aprendizagem:\n");
  scanf("%f",&eta);
  
  printf("Entre com o erro desejado:\n");
  scanf("%f",&errodes);
  
  printf("Entre a função desejada [ (1) Degrau (2) Sigmoide \n");
  scanf("%d",&funcao);
  
  system ("clear");

  printf("Pesos Iniciais\n");
  for(y = 0; y < ncesc; y++){
    for( x = 0; x < saida ; x++){
      printf("w[%d][%d] = %f\n", x, y, w[x][y]);
    }
    for( x = 0; x < entrada ; x++){
      printf("W[%d][%d] = %f\n", x, y, W[x][y]);
    }
  }
  
  printf(" Iniciando processo iterativo ...\n");
  for(x =0 ; x < epocas; x++){
    for( y = 0; y < exemplos; y++){
	for(contt = 0; contt < ncesc; contt++){
	    niesc[contt] =0;
	    for(cont2 = 0; cont2 < entrada ; cont2++)
	      niesc[contt] = niesc[contt] + W[contt][cont2] + entradas[cont2][y];
	    niesc[contt] = niesc[contt] + biasesc[contt];
	    switch(funcao){
	      case 1 :
		if(niesc[contt] > 0) phiesc[contt] = 1;
		else phiesc[contt] = 0;
		break;
	      case 2:
		phiesc[contt] = 1/(1+exp(-niesc[contt]));
		break;
	    }
	}
        for(contt = 0; contt < saida; contt++)
            erro[contt] = saidas[contt][y] - phi[contt];
        Erroinst = 0;
        
        for(contt = 0; contt < saida; contt++)
            Erroinst = Erroinst + erro[contt]*erro[contt]/2;
        
        Erromg = (Erromg*(x*exemplos + y) + Erroinst)/(x * exemplos + (y+1));
        
        if(Erromg < errodes)
            break;
        for(cont2 =0 ; cont2 < saida; cont2++){
            phi1[cont2]         = exp(-ni[cont2])/((1+exp(-ni[cont2]))* (1+exp(-ni[cont2])));
            delta[cont2]        = -erro[cont2]*phi1[cont2];
        }
        
        for(cont2 = 0; cont2 < ncesc; cont2++){
            phi1esc[cont2] = exp(-niesc[cont2])/((1+exp(-niesc[cont2])) * (1+exp(-niesc[cont2])));
            deltaesc[cont2] = 0;
            for(contt = 0; contt < saida; contt++)
                deltaesc[cont2] = deltaesc[cont2] + phi1esc[cont2]*delta[contt]*w[contt][cont2];
        }
        
        for(cont2 = 0; cont2 < saida; cont2++){
            for(contt = 0; contt < ncesc; contt++)
                w[cont2][contt] = w[cont2][contt] - eta*delta[cont2]*phiesc[contt];
            biass[cont2] = biass[cont2] - eta*delta[cont2]*phiesc[contt];
        }
        
        for(cont2 = 0; cont2 < ncesc ; cont2++){
            for(contt = 0; contt < entrada; contt++)
                W[cont2][contt] = W[cont2][contt] - eta*deltaesc[cont2]*entradas[contt][y];
            biasesc[cont2] = biasesc[cont2] - eta*deltaesc[cont2] * entradas[contt][y];
        }
    }
    if(Erromg < errodes){
        printf("Finalizando pelo erro em %d epocas de treinamento\n", x);
        break;
    }
  }
  
  printf("Bias finais\n");
  for(y=0; y < ncesc; y++)
      printf("%f",biasesc[y]);
  printf("\n");
  
  
  for(y=0; y < saida; y++)
      printf("%f",biass[y]);
  printf("\n Pesos Finais:\n");
  for( y=0 ; y < ncesc; y++){
      for(x = 0; x < saida; x++)
          printf("w[%d][%d] = %f",x,y,w[x][y]);
      for(x = 0; x < saida; x++)
          printf("W[%d][%d] = %f",x,y,W[x][y]);
  }
  
  printf("Finalizado!\n");
  for(x=0; x < exemplos; x++){
      printf("\nEntradas:");
      for(y=0; y<entrada; y++)
          printf("%f ",entradas[y][x]);
      printf("\nSaidas esperadas: ");
      for(y=0; y < saida; y++)
          printf("%f ",saidas[y][x]);
      printf("\nSaida da Rede: ");
      for(contt =0; contt < ncesc; contt++){
          niesc[contt] = 0;
          for(cont2 = 0; cont2 < entrada; cont2++)
              niesc[contt] = niesc[contt] + W[contt][cont2]*entradas[cont2][x];
          niesc[contt] = niesc[contt] + biasesc[contt];
          switch(funcao){
              case 1:
                  if(niesc[contt] > 0 ) phiesc[contt] = 1;
                  else phiesc[contt] = 0;
                  break;
              case 2:
                  phiesc[contt] = 1/(1+exp(-niesc[contt]));
                  break;
          }
      }
      for(contt = 0 ; contt < saida; contt++){
          ni[contt]     = 0;
          for(contt =0 ; cont2 < ncesc; cont2++)
              ni[contt] = ni[contt]+w[contt][cont2]*phiesc[cont2];
          ni[contt]     = ni[contt] + biass[contt];
          switch(funcao){
              case 1:
                  if(ni[contt] > 0 ) phi[contt] = 1;
                  else phi[contt] = 0;
                  break;
              case 2:
                  phi[contt] = 1/(1+exp(-ni[contt]));
                  break;
          }
          printf("%f ",phi[contt]);
      }
  }
  printf("Erro medio global: %f", Erromg);
	
  return 0;
}                                                           // end main