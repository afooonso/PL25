# TPC5 - Máquina de Vending 🥤

📅 **Data:** 2025-03-12

## 👨‍💻 Autor
**Nome:** Afonso Gonçalves Pedreira  
**Número:** A104537  
**Curso:** Engenharia Informática
**Ano:** 2024/2025  

---

## 📝 Descrição do Problema

O objetivo deste trabalho é desenvolver um programa que simula o funcionamento de uma **máquina de vending** e treinar o uso do *ply.lex* e a gestão de estados exclusivos dentro do analisador léxico. 

A máquina tem um stock de produtos, onde cada produto é identificado por:
- **Código** 💾
- **Nome** 🏷️
- **Quantidade** 📦
- **Preço** 💰

A informação do stock está armazenada num ficheiro JSON (`stock.json`) e é carregada em memória quando o programa inicia. No final da execução, o stock atualizado é gravado de volta no mesmo ficheiro, garantindo a persistência dos dados. 

O programa também permite interação com o utilizador, onde este pode:
- Inserir moedas na máquina 🪙
- Selecionar produtos disponíveis 🛒
- Consultar o saldo atual 💲
- Listar os produtos em stock 📜
- Sair e recolher o troco 🚪

O programa lida com diferentes cenários, como:
- Produto inexistente ❌
- Stock esgotado 🔴
- Saldo insuficiente ⚠️

---
## ⚙️ Funcionamento

### 📌 Regras:
1. O utilizador deve inserir moedas antes de selecionar um produto.
2. A máquina aceita apenas moedas válidas: `2e, 1e, 50c, 20c, 10c, 5c, 2c, 1c`.
3. Se o saldo for suficiente, o produto é dispensado e o stock é atualizado.
4. Caso o saldo seja insuficiente, a compra é recusada.
5. O utilizador pode consultar o saldo e o stock a qualquer momento.
6. Ao sair, o troco é devolvido automaticamente.

---

## 🛠️ Instruções de Utilização

### 1️⃣ Executar o Programa
Para correr o programa, basta executar o seguinte comando num terminal:
```bash
python tpc5.py
```

### 2️⃣ Comandos Disponíveis

| Comando         | Descrição                                        |
|---------------|------------------------------------------------|
| `SHOW`       | Lista todos os produtos em stock 📋           |
| `BALANCE`    | Mostra o saldo atual 💵                        |
| `INSERT X`   | Insere moeda `X` na máquina 🪙 (ex: `INSERT 1e`,`INSERT 2e,1e,50c`) |
| `SELECT Y`   | Seleciona o produto com código `Y` 🛍️ (ex: `SELECT A01`) |
| `EXIT`       | Sai do programa e devolve o troco 🚪💰        |

---

## 🔬 Testes Realizados

### ✅ Testes de Fluxo Normal:
- Inserção de diferentes combinações de moedas.
- Selecionar produtos com saldo suficiente.
- Listar o stock corretamente.
- Verificar saldo após compra.

### ⚠️ Testes de Erro:
- Tentar comprar sem saldo suficiente.
- Escolher um produto inexistente.
- Selecionar um produto esgotado.
- Inserir comandos inválidos.

### 🔄 Testes de Persistência:
- Garantir que o stock é guardado no `stock.json` corretamente.
- Reabrir o programa e verificar se os dados foram mantidos.

---

## 🎯 Conclusão
Este projeto permitiu simular uma máquina de vending funcional, utilizando manipulação de ficheiros JSON, gestão de saldo e interação com o utilizador. O programa trata diferentes exceções e garante persistência de dados entre sessões. 
