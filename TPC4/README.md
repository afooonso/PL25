# 🔍 TPC3 - Analisador Léxico 🔍

2025-02-28

## Autor 👨‍💻  
**Nome:** Afonso Gonçalves Pedreira  
**Número:** A104537  
**Curso:** Engenharia Informática  
**Ano:** 2024/2025  

## Descrição do problema

Neste TPC, o objetivo é construir um **analisador léxico** para uma linguagem de consulta que permita escrever frases do género:

### Exemplo (DBPedia: Obras de Chuck Berry)
```sql
SELECT ?nome ?desc WHERE {
  ?s a dbo:MusicalArtist.
  ?s foaf:name "Chuck Berry"@en .
  ?w dbo:artist ?s.
  ?w foaf:name ?nome.
  ?w dbo:abstract ?desc
} LIMIT 1000
```

O analisador léxico deve ser capaz de identificar e classificar corretamente os diferentes **tokens** presentes na linguagem, como **palavras-chave**, **identificadores**, **literais**, **símbolos** e **números**.

## Implementação  

O analisador foi desenvolvido em **Python**, usando expressões regulares para identificar os diferentes tokens presentes nas consultas.

### 1️⃣ **Leitura da Consulta**
O programa recebe uma consulta como entrada e processa-a.

### 2️⃣ **Identificação de Tokens**
O analisador identifica os seguintes tipos de tokens:

- **Palavras-chave (`SELECT`, `WHERE`, `LIMIT`)**  
  - Capturadas ao serem usadas expressões regulares para distinguir palavras reservadas da linguagem.

- **Variáveis (`?nome`, `?desc`, `?s`)**  
  - Identificam variáveis de consulta.

- **Literais (`"Chuck Berry"@en`)**  
  - Texto entre aspas, podendo conter sufixos de idioma (`@en`).

- **Identificadores (`dbo:MusicalArtist`, `dbo:artist`)**  
  - Representam classes e propriedades da ontologia.

- **Símbolos (`{}`, `.`, `:`)**  
  - Parênteses, chaves, pontos e operadores são reconhecidos separadamente.

- **Números (`1000`)**  
  - Valores numéricos utilizados, por exemplo, no `LIMIT`.

Cada token identificado é classificado e armazenado numa estrutura de dados para posterior análise.

### 3️⃣ **Geração da Saída**
Após processar a consulta, o programa imprime uma representação dos tokens encontrados.

## Instruções de Utilização

1. Criar um ficheiro de texto com a consulta a ser analisada (exemplo: `consulta.txt`).
2. Executar o script em Python:

```sh
$ python tpc3.py < consulta.txt
```

## 📌 Exemplo de Execução

### 📥 **Entrada (Consulta)**  
```sql
SELECT ?nome ?desc WHERE {
  ?s a dbo:MusicalArtist.
  ?s foaf:name "Chuck Berry"@en .
  ?w dbo:artist ?s.
  ?w foaf:name ?nome.
  ?w dbo:abstract ?desc
} LIMIT 1000
```

### 🔽 **Saída (Tokens)**  
```bash
LexToken(SELECT,'SELECT',1,0)
LexToken(VAR,'?nome',1,7)
LexToken(VAR,'?desc',1,13)
LexToken(WHERE,'WHERE',1,19)
LexToken(OPEN_CURLY,'{',1,25)
LexToken(VAR,'?s',2,31)
LexToken(A,'a',2,34)
LexToken(IRI,'dbo:MusicalArtist',2,36)
LexToken(DOT,'.',2,53)
LexToken(VAR,'?s',3,59)
LexToken(IRI,'foaf:name',3,62)
LexToken(LITERAL,'"Chuck Berry"@en',3,72)
LexToken(DOT,'.',3,88)
LexToken(VAR,'?w',4,94)
LexToken(IRI,'dbo:artist',4,97)
LexToken(VAR,'?s',4,108)
LexToken(DOT,'.',4,110)
LexToken(VAR,'?w',5,116)
LexToken(IRI,'foaf:name',5,119)
LexToken(VAR,'?nome',5,129)
LexToken(DOT,'.',5,134)
LexToken(VAR,'?w',6,140)
LexToken(IRI,'dbo:abstract',6,143)
LexToken(VAR,'?desc',6,156)
LexToken(DOT,'.',6,161)
LexToken(CLOSE_CURLY,'}',7,163)

```

Este analisador léxico serve como base para um **interpretador de consultas**, facilitando o pré-processamento antes da sua execução numa base de dados. 📚
