# Trivial Pascal

Este projeto consiste no desenvolvimento de um compilador da linguagem Pascal Standard para código compatível com a EWVM, uma máquina virtual disponibilizada no âmbito da unidade curricular de Processamento de Linguagens.

## Estrutura do Projeto

- `report/` — Contém o relatório detalhado da implementação do compilador
- `lex_pas.py` — Analisador léxico construído com o PLY (`lex`)
- `yacc_pas.py` — Analisador sintático com construção de AST e geração de código (com `ply.yacc`)
- `ast_nodes.py` — Definições dos nós da AST (árvore sintática abstrata)
- `pascal_codegen.py` — Geração de código para a EWVM a partir da AST
- `tests/` — Pasta com testes escritos em Pascal Standard

## Fases do Compilador

1. **Análise Léxica:** Utiliza o `lex_pas.py` para gerar tokens.
2. **Análise Sintática:** O ficheiro `yacc_pas.py` define a GIC e gera a AST.
3. **Análise Semântica:** Feita durante a geração de código, com verificação de tipos e declarações.
4. **Geração de Código:** Traduz a AST para instruções da EWVM, armazenadas no ficheiro `output.txt`.

## Como Executar

```bash
python yacc_pas.py <file>
```

Este comando irá:
- Analisar léxica e sintaticamente o ficheiro
- Gerar a árvore AST
- Criar uma imagem `ast_graph.png` com a estrutura
- Produzir o ficheiro `output.txt` com o código para a VM

## Exemplo

Para o seguinte código Pascal:

```pascal
program Soma;
var a, b, c: integer;
begin
  a := 2;
  b := 3;
  c := a + b;
  writeln(c);
end.
```

O código gerado será semelhante a:

```bash
pushi 2
storeg 0
pushi 3
storeg 1
pushg 0
pushg 1
add
storeg 2
pushg 2
writei
writeln
stop
```

## Notas

- São usados labels únicos para blocos `if`, `for` e `while`
- Suporte a arrays, tipos `integer`, `real`, `boolean`, `char`, `string`
- Funções embutidas: `writeln`, `read`, `atoi`, `itof`, etc.
- A análise semântica deteta erros de tipo e declarações em falta

