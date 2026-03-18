---
layout: post
title: "Aprendendo Elixir - Pattern Matching"
author: "Eduardo N. S. R."
date: 2025-04-28 20:28:00
permalink: /posts/elixir-patterns/
tags: [Programação, Programação Funcional, Elixir, Patterns]
---

Se tívessemos que apontar uma única característica que define como é programar em Elixir, seria o **pattern matching**. Esse recurso da linguagem vai muito além do que atribuição tradicional que conhecemos em outras linguagens: ela molda a forma como estruturamos o código.

O pattern matching é uma ferramenta poderosa que permite comparar estruturas de dados, extrair valores e guiar o fluxo de execução de forma clara e expressiva. Em Elixir, essa técnica não é apenas uma opção útil: ela é uma expectativa idiomática em praticamente todo o código escrito.

Ao longo deste artigo, vamos explorar a semântica do pattern matching em Elixir, desde sua interpretação básica com o operador `=`, passando pela desconstrução de tuplas e listas, até o uso intensivo em fluxos de controle e definição de funções.

Todos os exemplos práticos apresentados foram extraídos do projeto em desenvolvimento, no qual implementamos um algoritmo conhecido como **Shunting Yard**. Este algoritmo tem como objetivo converter expressões matemáticas da notação infixa (como `1 + 2 * 3`) para uma estrutura que seja mais fácil de ser interpretada por computadores, como a notação posfixa ("notação polonesa reversa"). No nosso caso, a implementação serve também para construir uma árvore sintática abstrata (AST).

O código está organizado no diretório [03-patterns](https://github.com/vndmtrx/estudo_elixir/tree/main/03-patterns) e os demais estarão organizados no [repositório principal do projeto](https://github.com/vndmtrx/estudo_elixir).

## O Significado do `=`: Atribuir e Casar ao Mesmo Tempo

Antes de nos aprofundarmos nas estruturas complexas, é essencial entender como Elixir interpreta o operador `=`. Em muitas linguagens, `=` é simplesmente atribuição. Em Elixir, ele representa uma tentativa de correspondência: "o lado esquerdo deve se parecer com o lado direito".

Por exemplo:

```elixir
x = 10
```

*Aqui, a variável `x` é setada com o valor `10`, pois ela está vazia e, para garantir a igualdade, é ajustada.*

Em um cenário mais elaborado:

```elixir
{:ok, resultado} = {:ok, "teste"}
```

*Aqui, o padrão `{:ok, resultado}` casa com a tupla `{:ok, "teste"}` e atribui o valor `"teste"` à variável `resultado`.*

Quando os padrões não combinam, ocorre erro:

```elixir
{:ok, valor} = {:error, "falha"}
# ** (MatchError) no match of right hand side value: {:error, "falha"}
```

*Neste caso, como `:ok` e `:error` são diferentes, ocorre uma falha de correspondência.*

---

## Desconstruindo Tuplas e Listas

Agora que compreendemos o conceito de correspondência básica, podemos avançar para estruturas compostas. Tuplas e listas são duas formas essenciais de dados em Elixir, e o pattern matching se mostra extremamente útil para manipulá-las.

### Tuplas

Exemplo direto do projeto:

```elixir
{:num, valor} = {:num, "42"}
IO.inspect(valor) # "42"
```

*Aqui, extraímos o segundo elemento da tupla, capturando a string "42" na variável `valor`.*

### Listas

No algoritmo Shunting Yard, manipulamos pilhas usando essa forma:

```elixir
[token | resto] = [{:num, "1"}, {:op, "+"}]
IO.inspect(token) # {:num, "1"}
IO.inspect(resto) # [{:op, "+"}]
```

*Esse trecho separa o primeiro elemento da lista (`token`) e o restante da lista (`resto`), uma prática comum para percorrer ou modificar listas.*

Além de `[head | tail]`, também é possível casar listas de outras formas:

- `[]` casa apenas com uma lista vazia.
- `[variavel]` casa apenas com uma lista que contém exatamente um elemento.
- `[head | tail]` casa com qualquer lista não vazia, separando o primeiro elemento (head) e o restante (tail).
- `[item1, item2 | tail]` casa com uma lista com pelo menos 2 elementos, retornando eles. E isso vai indo pela quantidade de elementos necessários.

## Convenção Idiomática em Elixir

Ao lidar com resultados de operações que podem falhar, Elixir adota um padrão simples e eficaz: tuplas indicando sucesso ou erro. Esse modelo torna o tratamento de erros previsível e o código mais legível.

Trecho real do projeto:

```elixir
def parse([]), do: {:error, :entrada_vazia}
def parse(tokens), do: {:ok, processa(tokens)}
```

*Aqui, caso a entrada seja vazia, retornamos `{:error, :entrada_vazia}`. Caso contrário, processamos os tokens e retornamos `{:ok, resultado}`.*

## Controle de Fluxo com Pattern Matching

Com a habilidade de desconstruir dados de forma tão natural, Elixir permite construir fluxos de decisão que se adaptam diretamente à estrutura dos dados. Vejamos como isso se aplica em diferentes construções de controle.

### Controle de Fluxo com `case`

O `case` em Elixir é uma estrutura que utiliza pattern matching para escolher entre diferentes caminhos de execução, dependendo do valor analisado. Ele permite aplicar padrões diretamente sobre o resultado de expressões.

```elixir
case parse(tokens, [], []) do
  {:ok, ast} -> valida_ast(ast)
  {:error, motivo} -> {:error, motivo}
end
```

*Nesse exemplo, o resultado da função parse/3 é analisado. Se for `{:ok, ast}`, a AST é validada. Se for `{:error, motivo}`, o erro é propagado.*

### Controle de Fluxo com `with`

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

*Nesse trecho, três etapas são executadas em sequência: parsing da esquerda, parsing da direita e montagem da AST. Se qualquer uma delas falhar, o erro é tratado no `else`. Caso tudo corra bem, retornamos o AST montado e o restante da entrada.*

## Pattern Matching em Assinaturas de Função

Talvez o uso mais elegante de pattern matching em Elixir seja na própria definição de funções. Podemos definir várias versões de uma mesma função, cada uma lidando com um padrão específico de argumentos.

O projeto usa isso amplamente:

```elixir
defp empilha({:num, valor}, pilha), do: [valor | pilha]
defp empilha({:op, operador}, pilha), do: [operador | pilha]
```

*Aqui, dependendo se o elemento é um número ou um operador, escolhemos como empilhar corretamente.*

Essa combinação de pattern matching + múltiplas cláusulas torna o código altamente modular, limpo e fácil de estender, simulando o conceito de overload de funções encontrado em outras linguagens.

## Outros Usos Poderosos de Pattern Matching

Além dos exemplos já vistos, pattern matching em Elixir é utilizado em diversas situações práticas que enriquecem ainda mais o desenvolvimento.

### Pattern Matching em Maps

Podemos casar valores de chaves específicas diretamente:

```elixir
%{nome: nome} = %{nome: "Ana", idade: 30}
IO.puts(nome) # "Ana"
```

*Aqui extraímos apenas a chave `:nome`, ignorando o restante.*

### Pattern Matching em Structs

Também podemos usar pattern matching para validar e extrair dados de structs:

```elixir
defmodule Pessoa do
  defstruct [:nome, :idade]
end

%Pessoa{nome: nome} = %Pessoa{nome: "João", idade: 25}
IO.puts(nome) # "João"
```

*Este exemplo garante que estamos lidando com uma struct `Pessoa` antes de extrair o nome.*

### Guards vs Padrões Diretos

Para listas, podemos casar explicitamente:

```elixir
def trata_lista([]), do: :vazia
def trata_lista([_ | _]), do: :com_elementos
```

Ou usar `when`:

```elixir
def trata_lista(lista) when length(lista) == 0, do: :vazia
def trata_lista(lista), do: :com_elementos
```

Embora os dois funcionem, casar diretamente padrões é mais performático e idiomático.

### Ignorar Valores com `_`

Inclusive, como visto no exemplo anterior, podemos ignorar partes do padrão que não nos interessam:

```elixir
{:ok, _} = {:ok, "qualquer coisa"}
```

*Aqui aceitamos a estrutura, mas onde está o `_`, desconsideramos o conteúdo.*

Adicionalmente, podemos ainda nomear ignorados para fins de clareza:

```elixir
{:ok, _qualquer} = {:ok, "teste"}
```

Mesmo que não usemos o valor, nomeá-lo pode ajudar na documentação implícita do código.

### Padrões para Parâmetros Opcionais

Casando entradas diferentes:

```elixir
defp valida_ast([arvore]), do: {:ok, arvore}
defp valida_ast(_), do: {:error, :ast_invalido}
```

*Aqui aceitamos tanto uma lista na primeira função quanto qualquer outra coisa na segunda, usando pattern matching nas entradas da função.*

## Pattern Matching em Binários (Strings e Bytes)

Elixir também permite aplicar pattern matching diretamente sobre dados binários, como strings e buffers de bytes. Essa funcionalidade é amplamente utilizada, especialmente para parsing de texto e manipulação de fluxos binários.

No nosso projeto, usamos bastante no módulo Tokenize, onde exploramos esse recurso para decompor strings em seus caracteres.

### Extraindo o primeiro caractere

```elixir
<<c, resto::binary>> = "abc"
IO.inspect(c)    # 97
IO.inspect(rest) # "bc"
```

*Aqui, `c` captura o primeiro byte (o código ASCII de "a"), e `resto` captura o restante da string.*

### Validando dígitos

No Tokenizer, um trecho essencial é identificar números:

```elixir
defp tokenize(<<c, resto::binary>>, acc, numero) when c in ?0..?9 do
  tokenize(resto, acc, numero <> <<c>>)
end
```

*Nessa função, capturamos o primeiro caractere e verificamos se ele é um número entre 0 e 9 usando guards, então concatenamos ele com a string na variável `numero`.*

### Casando prefixos específicos

Também podemos casar prefixos específicos de forma explícita:

```elixir
<<"sin" <> resto>> = "sin(30)"
IO.inspect(resto) # "(30)"
```

*Aqui, reconhecemos o prefixo "sin" diretamente e extraímos o restante da expressão.*

### Vantagens do Pattern Matching em Binários

- **Eficiência**: Não precisamos percorrer a string manualmente.
- **Clareza**: O que estamos tentando extrair fica visível diretamente na assinatura do padrão.
- **Combinação com guards**: Podemos validar bytes enquanto extraímos.

## Conclusão

O pattern matching em Elixir é um recurso central que influencia diretamente a maneira como funções são escritas, como fluxos de dados são controlados e como estruturas são desconstruídas. Mais do que uma facilidade de linguagem, ele é uma ferramenta prática para organizar o código de forma legível, segura e concisa.

Neste artigo, exploramos diversas aplicações do pattern matching, desde operações básicas com tuplas e listas até usos mais avançados em maps, structs e binários.

Compreender bem o pattern matching é essencial para escrever código Elixir de maneira idiomática e aproveitar ao máximo a expressividade que a linguagem oferece.

## Referências 🔗

- [Documentação oficial do Elixir](https://elixir-lang.org/)
- [Pattern Matching no Elixir School](https://elixirschool.com/en/lessons/basics/pattern_matching)
- [Pattern Matching na Documentação do Elixir](https://hexdocs.pm/elixir/pattern-matching.html)
- [Estruturas de Controle na Documentação do Elixir](https://hexdocs.pm/elixir/case-cond-and-if.html)
- [Patterns Binários na Documentação do Elixir](https://hexdocs.pm/elixir/main/patterns-and-guards.html#binaries)