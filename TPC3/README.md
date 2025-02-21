# 🎨 TPC2 - Conversor de MD para HTML 🎨

2025-02-21

## Autor 🧑‍💻 
**Nome:** Afonso Gonçalves Pedreira  
**Número:** A104537  
**Curso:** Software Engineering  
**Ano:** 2024/2025  

## Descrição do problema

Neste TPC, o objetivo é criar um **conversor de Markdown (MD) para HTML**. O programa deverá ser capaz de processar e converter os seguintes elementos básicos de formatação presentes em uma **Markdown Cheat Sheet**:

- **Cabeçalhos**: Linhas iniciadas por "# texto", ou "## texto" ou "### texto"
    - **In**: `# Exemplo`
    - **Out**: `<h1>Exemplo</h1>`
  
- **Bold**: Pedaços de texto entre `**`
    - **In**: Este é um `**exemplo**` ...
    - **Out**: Este é um `<b>exemplo</b>` ...

- **Itálico**: Pedaços de texto entre `*`
    - **In**: Este é um `*exemplo*` ...
    - **Out**: Este é um `<i>exemplo</i>` ...

- **Lista numerada**:
    - **In**: `1. Primeiro item 2. Segundo item 3. Terceiro item`
    - **Out**:
      ```html
      <ol>
        <li>Primeiro item</li>
        <li>Segundo item</li>
        <li>Terceiro item</li>
      </ol>
      ```

- **Link**: `[texto](endereço URL)`
    - **In**: Como pode ser consultado em `[página da UC](http://www.uc.pt)`
    - **Out**: Como pode ser consultado em `<a href="http://www.uc.pt">página da UC</a>`

- **Imagem**: `![texto alternativo](path para a imagem)`
    - **In**: Como se vê na imagem seguinte: `![imagem dum coelho](http://www.coellho.com)` ...
    - **Out**: Como se vê na imagem seguinte: `<img src="http://www.coellho.com" alt="imagem dum coelho"/>`


## Implementação  

O conversor foi desenvolvido em **Python**, utilizando expressões regulares para identificar e substituir os elementos Markdown pelos seus equivalentes em HTML.  

#### 1️⃣ **Leitura do ficheiro Markdown**  
O programa lê o ficheiro linha por linha, permitindo processar e converter cada elemento de forma eficiente. Para isso, utilizei `fileinput.input()`, permitindo receber a entrada diretamente do terminal.  

#### 2️⃣ **Processamento dos elementos Markdown**  
Cada tipo de formatação é tratado separadamente:  

- **Cabeçalhos (`# Título`) → `<h1>Título</h1>`**  
  - Utilizei uma expressão regular que captura `#`, `##`, `###` e os restantes níveis até `######`.  
  - O número de `#` define o nível do cabeçalho, sendo convertido em `<h1>` até `<h6>`.  

- **Texto em negrito (`**texto**`) → `<b>texto</b>`**  
  - A regex procura por `**texto**` ou `__texto__` e substitui pelo equivalente HTML.  
  - Para evitar conflitos com o itálico, dei prioridade ao negrito antes de processar o itálico.  

- **Texto em itálico (`*texto*`) → `<i>texto</i>`**  
  - Similar ao negrito, a regex captura `*texto*` e `_texto_`, garantindo que não se sobrepõe ao negrito.  

- **Listas numeradas (`1. Item`) → `<ol><li>Item</li></ol>`**  
  - Verifico se a linha começa com um número seguido de um ponto (`1.`).  
  - Cada item da lista é inicialmente convertido num `<li>Item</li>`.  
  - No final, aplico a função `handle_ordered_lists()`, que agrupa corretamente os `<li>` dentro de `<ol>`.  

- **Links (`[texto](url)`) → `<a href="url">texto</a>`**  
  - A regex identifica o padrão `[texto](url)` e substitui pelo HTML `<a>`.  

- **Imagens (`![alt](url)`) → `<img src="url" alt="alt"/>`**  
  - Segue a mesma lógica dos links, mas gerando um `<img>` em vez de `<a>`.  

#### 3️⃣ **Geração do HTML final**  
Depois de processar todas as linhas, o código junta os elementos convertidos e cria um novo ficheiro chamado `result.html`. Isso permite que o utilizador visualize o resultado diretamente num browser. 

## Instruções de utilização

1. O arquivo de entrada em Markdown deve estar na mesma pasta que o script.
2. Executar o script para converter o conteúdo de Markdown para HTML:

```sh
$ python tpc2.py < test.md
```

## 📌 Resultados  

### 📥 **Entrada (Markdown)**  

```md
# Heading 1
## Heading 2
### Heading 3

This is a **bold** text and this is an *italic* text.

This is a [link](https://example.com) and here is an image:

![Alt text](https://example.com/image.jpg)

1. First item
2. Second item
3. Third item
```
### 🔽 **Saída (HTML)**  
```html 
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>

This is a <b>bold</b> text and this is an <i>italic</i> text.

This is a <a href="https://example.com">link</a> and here is an image:

<img src="https://example.com/image.jpg" alt="Alt text"/>

<ol>
<li>First item</li>
<li>Second item</li>
<li>Third item</li>
</ol>
```

