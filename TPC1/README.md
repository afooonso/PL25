# TPC1 - Somador on/off

2025-02-07

## Autor
**Nome:** Afonso Gonçalves Pedreira  
**Número:** A104537  
**Curso:** Software Engineering  
**Ano:** 2024/2025  

## Descrição do problema

1. Pretende-se um programa que some todas as sequências de dígitos que encontre num texto;
2. Sempre que encontrar a string “Off” em qualquer combinação de maiúsculas e minúsculas, esse comportamento é desligado;
3. Sempre que encontrar a string “On” em qualquer combinação de maiúsculas e minúsculas, esse comportamento é novamente ligado;
4. Sempre que encontrar o caráter “=”, o resultado da soma é colocado na saída.

## Funcionamento

O programa processa um texto dado como entrada, somando as sequências de dígitos encontrados apenas quando o comportamento de soma está "On". Quando o comportamento está "Off", o programa ignora as sequências de dígitos e não as soma. A soma é finalizada e apresentada sempre que o programa encontra o sinal "=".

### Regras:
- **"On"**: Ativa o comportamento de soma.
- **"Off"**: Desativa o comportamento de soma.
- **"="**: Mostra o resultado acumulado da soma até o momento.


## Instruções de utilização
1. O arquivo de entrada deve estar na mesma pasta que o script.
2. Executar o script:

```sh
$ python tpc1.py < filename.txt
```

## Testes realizados

### Teste 1:
**Arquivo de entrada: `teste_1.txt`**
```sh
$ python tpc1.py <teste_1.txt
Total: 350
Total: 350
Total: 750

```



### Teste 2:
**Arquivo de entrada: `teste_2.txt`**

```bash
$ python tpc1.py <teste_2.txt
Total: 100
Total: 170
```



### Teste 3:
**Arquivo de entrada: `teste_3.txt`**
```bash

$ python tpc1.py <teste_3.txt
Total: 3370
Total: 3370
Total: 4770
Total: 4770
Total: 7770
Total: 7770


```




### Teste 4:
**Arquivo de entrada: `teste_4.txt`**
```bash 
$ python tpc1.py <teste_4.txt
Total: 300
Total: 300
Total: 1400
```

