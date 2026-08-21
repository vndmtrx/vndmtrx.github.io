---
layout: post
title: "Aprendendo Elixir - Pattern Matching"
subtitle: "Desconstrução de dados, fluxo idiomático e a implementação do algoritmo Shunting Yard"
author:
  - "Eduardo N. S. R."
date: 2025-04-28 20:28:00 GMT-3
permalink: /posts/elixir-patterns/
tags: [Programação, Programação Funcional, Elixir, Patterns]
series: Aprendendo Elixir
---

Se tivéssemos que apontar uma única característica que define como é programar em Elixir [^1], seria o **pattern matching**. Esse recurso da linguagem vai muito além da atribuição tradicional que conhecemos em outras linguagens: ele molda a forma como pensamos e estruturamos o código.

O pattern matching [^2] é uma ferramenta poderosa que permite comparar estruturas de dados, extrair valores e guiar o fluxo de execução de forma clara e expressiva. Em Elixir, essa técnica não é apenas uma opção útil: ela é uma expectativa idiomática em praticamente todo o código escrito.

Ao longo deste artigo, vamos explorar a semântica do pattern matching em Elixir, desde sua interpretação básica com o operador `=`, passando pela desconstrução de tuplas e listas, até o uso intensivo em fluxos de controle e definição de funções.

Todos os exemplos práticos apresentados foram extraídos do projeto em desenvolvimento, no qual implementamos um algoritmo conhecido como **Shunting Yard**. Este algoritmo tem como objetivo converter expressões matemáticas da notação infixa (como `1 + 2 * 3`) para uma estrutura que seja mais fácil de ser interpretada por computadores, como a notação posfixa ("notação polonesa reversa"). No nosso caso, a implementação serve também para construir uma árvore sintática abstrata (AST).

O código está organizado no diretório [03-patterns](https://github.com/vndmtrx/estudo_elixir/tree/main/03-patterns) e os demais estarão organizados no [repositório principal do projeto](https://github.com/vndmtrx/estudo_elixir).

## O Significado do Igual: Atribuir e Casar ao Mesmo Tempo

Antes de nos aprofundarmos nas estruturas complexas, é essencial entender como Elixir interpreta o operador `=` [^3]. Em muitas linguagens, `=` é simplesmente atribuição. Em Elixir, ele representa uma tentativa de correspondência: "o lado esquerdo deve se parecer com o lado direito".

Por exemplo:

```elixir
x = 10
```

*Aqui, a variável `x` recebe o valor `10` para satisfazer a igualdade com o lado direito.*

Em um cenário mais elaborado:

```elixir
{:ok, resultado} = {:ok, "teste"}
```

*Aqui, o padrão `{:ok, resultado}` casa com a tupla `{:ok, "teste"}` e vincula `"teste"` à variável `resultado`.*

Quando os padrões não combinam, ocorre erro de casamento:

```elixir
{:ok, valor} = {:error, "falha"}
# ** (MatchError) no match of right hand side value: {:error, "falha"}
```

*Como os átomos `:ok` e `:error` são distintos, o Elixir lança um MatchError impedindo a execução.*

## Desconstruindo Tuplas e Listas

Agora que compreendemos o conceito de correspondência básica, podemos avançar para estruturas compostas. Tuplas e listas são duas formas essenciais de dados em Elixir, e o pattern matching se mostra extremamente útil para manipulá-las.

### Tuplas

Exemplo direto do projeto:

```elixir
{:num, valor} = {:num, "42"}
IO.inspect(valor) # "42"
```

*Extrai o segundo elemento da tupla, capturando a string "42" diretamente na variável `valor`.*

### Listas

No algoritmo Shunting Yard, manipulamos pilhas separando cabeça e cauda:

```elixir
[token | resto] = [{:num, "1"}, {:op, "+"}]
IO.inspect(token) # {:num, "1"}
IO.inspect(resto) # [{:op, "+"}]
```

*Separa o primeiro elemento da lista (`token`) e mantém o restante dos itens na lista `resto`.*

Além de `[head | tail]`, também é possível casar listas de outras formas:

- `[]` casa apenas com uma lista vazia.
- `[variavel]` casa apenas com uma lista que contém exatamente um elemento.
- `[head | tail]` casa com qualquer lista não vazia, separando o primeiro elemento (head) e o restante (tail).
- `[item1, item2 | tail]` casa com uma lista com pelo menos 2 elementos, retornando-os. E isso pode ser estendido conforme a necessidade.

## Convenção Idiomática em Elixir

Ao lidar com resultados de operações que podem falhar, Elixir adota um padrão simples e eficaz: tuplas indicando sucesso ou erro. Esse modelo torna o tratamento de erros previsível e o código mais legível.

Trecho real do projeto:

```elixir
def parse([]), do: {:error, :entrada_vazia}
def parse(tokens), do: {:ok, processa(tokens)}
```

*Retorna tuplas tagged `{:error, motivo}` ou `{:ok, resultado}` conforme o padrão da lista recebida.*

## Controle de Fluxo com Pattern Matching

Com a habilidade de desconstruir dados de forma tão natural, Elixir permite construir fluxos de decisão que se adaptam diretamente à estrutura dos dados. Vejamos como isso se aplica em diferentes construções de controle.

### Controle de Fluxo com case

O `case` em Elixir é uma estrutura que utiliza pattern matching para escolher entre diferentes caminhos de execução [^4], dependendo do valor analisado. Ele permite aplicar padrões diretamente sobre o resultado de expressões.

```elixir
case parse(tokens, [], []) do
  {:ok, ast} -> valida_ast(ast)
  {:error, motivo} -> {:error, motivo}
end
```

*Avalia o retorno de `parse/3`: se for `{:ok, ast}` avança para a validação, caso contrário propaga o erro.*

### Controle de Fluxo com with

O `with` é utilizado para encadear múltiplas operações que podem falhar. Cada etapa precisa casar corretamente para o fluxo continuar; caso contrário, o controle é transferido imediatamente para o bloco `else`.

```elixir
with {:ok, esq, resto1} <- parse_tokens(resto),
     {:ok, dir, resto2} <- parse_tokens(resto1),
     {:ok, ast} <- monta_ast({:op, token, esq, dir}) do
  {:ok, ast, resto2}
else
  {:error, motivo} -> {:error, motivo}
end
```

*Executa três etapas de parsing em pipeline: qualquer falha de casamento desvia imediatamente para o bloco `else`.*

## Pattern Matching em Assinaturas de Função

Talvez o uso mais elegante de pattern matching em Elixir seja na própria definição de funções. Podemos definir várias versões de uma mesma função, cada uma lidando com um padrão específico de argumentos.

O projeto usa isso amplamente:

```elixir
defp empilha({:num, valor}, pilha), do: [valor | pilha]
defp empilha({:op, operador}, pilha), do: [operador | pilha]
```

*Define cláusulas distintas para a mesma função dependendo da tag da tupla (`:num` ou `:op`).*

Essa combinação de pattern matching com múltiplas cláusulas torna o código altamente modular, limpo e fácil de estender, substituindo com elegância estruturas de `if`/`switch` ou sobrecarga de métodos.

## Outros Usos Poderosos de Pattern Matching

Além dos exemplos já vistos, pattern matching em Elixir é utilizado em diversas situações práticas que enriquecem ainda mais o desenvolvimento.

### Pattern Matching em Maps

Podemos casar valores de chaves específicas diretamente:

```elixir
%{nome: nome} = %{nome: "Ana", idade: 30}
IO.puts(nome) # "Ana"
```

*Extrai o valor da chave `:nome` ignorando as demais propriedades presentes no map.*

### Pattern Matching em Structs

Também podemos usar pattern matching para validar e extrair dados de structs:

```elixir
defmodule Pessoa do
  defstruct [:nome, :idade]
end

%Pessoa{nome: nome} = %Pessoa{nome: "João", idade: 25}
IO.puts(nome) # "João"
```

*Garante que o dado seja estritamente uma instância da struct `Pessoa` antes de extrair o campo `:nome`.*

### Guards vs Padrões Diretos

Para listas, podemos casar explicitamente:

```elixir
def trata_lista([]), do: :vazia
def trata_lista([_ | _]), do: :com_elementos
```

*Usa casamento estrutural direto para diferenciar lista vazia de lista com elementos.*

Ou usar `when`:

```elixir
def trata_lista(lista) when length(lista) == 0, do: :vazia
def trata_lista(lista), do: :com_elementos
```

*Aplica a guard clause `when length(lista) == 0` para validar o tamanho da coleção.*

Embora os dois funcionem, casar diretamente padrões é mais performático e idiomático.

### Ignorar Valores com Underscore

Inclusive, como visto no exemplo anterior, podemos ignorar partes do padrão que não nos interessam:

```elixir
{:ok, _} = {:ok, "qualquer coisa"}
```

*Valida que o retorno é uma tupla iniciada com `:ok`, descartando o segundo elemento com `_`.*

Adicionalmente, podemos ainda nomear ignorados para fins de clareza:

```elixir
{:ok, _qualquer} = {:ok, "teste"}
```

*Nomeia o valor ignorado com prefixo `_` para documentar a intenção do código sem gerar warnings do compilador.*

### Padrões para Parâmetros Opcionais

Casando entradas diferentes:

```elixir
defp valida_ast([arvore]), do: {:ok, arvore}
defp valida_ast(_), do: {:error, :ast_invalido}
```

*Aceita uma lista com um único elemento na primeira cláusula e trata qualquer outro formato como erro.*

## Pattern Matching em Binários (Strings e Bytes)

Elixir também permite aplicar pattern matching diretamente sobre dados binários [^5], como strings e buffers de bytes. Essa funcionalidade é amplamente utilizada, especialmente para parsing de texto e manipulação de fluxos binários.

No nosso projeto, usamos bastante no módulo Tokenize, onde exploramos esse recurso para decompor strings em seus caracteres.

### Extraindo o primeiro caractere

```elixir
<<c, resto::binary>> = "abc"
IO.inspect(c)     # 97
IO.inspect(resto) # "bc"
```

*Captura o primeiro byte ASCII na variável `c` e o restante da string no binário `resto`.*

### Validando dígitos

No Tokenizer, um trecho essencial é identificar números:

```elixir
defp tokenize(<<c, resto::binary>>, acc, numero) when c in ?0..?9 do
  tokenize(resto, acc, numero <> <<c>>)
end
```

*Extrai o caractere `c`, valida se é um dígito numérico via guard e o concatena ao acumulador.*

### Casando prefixos específicos

Também podemos casar prefixos específicos de forma explícita:

```elixir
<<"sin" <> resto>> = "sin(30)"
IO.inspect(resto) # "(30)"
```

*Reconhece o prefixo literal "sin" no início da string e extrai o restante dos caracteres.*

### Vantagens do Pattern Matching em Binários

- **Eficiência**: Não precisamos percorrer a string manualmente.
- **Clareza**: O que estamos tentando extrair fica visível diretamente na assinatura do padrão.
- **Combinação com guards**: Podemos validar bytes enquanto extraímos.

## Conclusão

O pattern matching em Elixir é um recurso central que influencia diretamente a maneira como funções são escritas, como fluxos de dados são controlados e como estruturas são desconstruídas. Mais do que uma facilidade de linguagem, ele é uma ferramenta prática para organizar o código de forma legível, segura e concisa.

Neste artigo, exploramos diversas aplicações do pattern matching, desde operações básicas com tuplas e listas até usos mais avançados em maps, structs e binários. Compreender bem o pattern matching é essencial para escrever código Elixir de maneira idiomática e aproveitar ao máximo a expressividade que a linguagem oferece.

## Referências

[^1]: **Documentação oficial do Elixir** {*Elixir Lang*} ([Link](https://elixir-lang.org/))

[^2]: **Pattern Matching** {*Elixir School*} ([Link](https://elixirschool.com/en/lessons/basics/pattern_matching))

[^3]: **Pattern Matching** {*HexDocs*} ([Link](https://hexdocs.pm/elixir/pattern-matching.html))

[^4]: **Estruturas de Controle** {*HexDocs*} ([Link](https://hexdocs.pm/elixir/case-cond-and-if.html))

[^5]: **Patterns Binários** {*HexDocs*} ([Link](https://hexdocs.pm/elixir/main/patterns-and-guards.html#binaries))
