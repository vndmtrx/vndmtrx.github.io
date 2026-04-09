---
layout: post
title: "Aprendendo Elixir - Estrutura Modular com Umbrella"
author: "Eduardo N. S. R."
date: 2025-04-20 15:46:00 GMT-3
permalink: /posts/elixir-umbrella/
tags: [Programação, Programação Funcional, Elixir, Umbrella, Modularização, Testes]
---

Neste segundo post da série *Aprendendo Elixir*, vamos explorar como organizar projetos maiores usando **arquitetura modular** com uma estrutura de guarda-chuva (chamado *Umbrella* pelo Elixir). A ideia é dividir o sistema em múltiplas aplicações menores e coesas, que podem ser desenvolvidas, testadas e integradas dentro de uma aplicação principal. Esse modelo segue o princípio de separação de responsabilidades, facilitando a manutenção e o crescimento do código. 

Os exemplos desse post estão em [02-umbrella](https://github.com/vndmtrx/estudo_elixir/tree/main/02-umbrella), e os demais estarão organizados no [repositório principal do projeto](https://github.com/vndmtrx/estudo_elixir).

Nosso projeto de exemplo é um **conversor unificado** com três apps:

- `conversor_temperatura` – conversão entre Celsius e Fahrenheit
- `conversor_distancia` – conversão entre metros e pés
- `main` – aplicação principal que orquestra as conversões com interação do usuário

## Por que usar um projeto Guarda-Chuva?

Projetos Guarda-Chuva são ideais quando queremos:

- **Modularizar funcionalidades** de forma clara e reaproveitável
- **Separar domínios** de forma independente (ex: API, banco, workers)
- Facilitar **testes e manutenção** em projetos maiores
- Gerenciar **dependências locais** entre apps sem necessidade de publicar pacotes

Cada app tem seu próprio ciclo de vida e testes, mas todos podem ser carregados e orquestrados a partir do projeto raiz. O Elixir lida muito bem com esse modelo graças à sua estrutura de aplicações OTP, onde cada subprojeto pode ter seu ciclo de vida próprio.

## Criando o projeto guarda-chuva

Crie o projeto principal com:

```bash
mix new conversor --umbrella
cd conversor
```

O comando `--umbrella` cria uma estrutura inicial com a pasta `apps/` onde viverão as subaplicações.

> ⚠️ **Aviso**: A partir daqui, sempre que falarmos da **raiz** do projeto, estamos considerando esta pasta inicial criada com o comando acima.

Agora dentro do diretório `apps`, criamos os três subprojetos:

```bash
cd apps
mix new conversor_distancia
mix new conversor_temperatura
mix new main
```

## Estrutura do projeto

A estrutura do projeto após esses comandos será:

```
conversor
├── apps
│   ├── conversor_distancia
│   │   ├── lib
│   │   │   └── conversor_distancia.ex
│   │   └── test
│   │       └── conversor_distancia_test.exs
│   ├── conversor_temperatura
│   │   ├── lib
│   │   │   └── conversor_temperatura.ex
│   │   └── test
│   │       └── conversor_temperatura_test.exs
│   └── main
│       ├── lib
│       │   └── main.ex
│       ├── mix.exs
│       └── test
│           └── main_test.exs
└── mix.exs
```

> ⚠️ **Aviso**: Esta não é a estrutura completa gerada pelos comandos, mas somente os arquivos que iremos nos preocupar neste momento.

O arquivo `mix.exs` da raiz define que o projeto é do tipo umbrella por conta da opção `apps_path: "apps"`, fazendo a centralização da orquestração do projeto.

## Implementando os apps

### `Conversor.Distancia`

Este app de exemplo lida com conversões entre metros e pés.

**apps/conversor_distancia/lib/conversor_distancia.ex:**

```elixir
defmodule Conversor.Distancia do
  @moduledoc """
  Conversão entre metros e pés.
  """

  @doc """
  Converte metros para pés.

      iex> Conversor.Distancia.m_para_ft(1) |> Float.round(4)
      3.2808
  """
  def m_para_ft(m) when is_number(m), do: m * 3.28084

  @doc """
  Converte pés para metros.

      iex> Conversor.Distancia.ft_para_m(1) |> Float.round(4)
      0.3048
  """
  def ft_para_m(ft) when is_number(ft), do: ft / 3.28084
end
```

### `Conversor.Temperatura`

Este app de exemplo trata de conversão entre escalas de temperatura:

**apps/conversor_temperatura/lib/conversor_temperatura.ex:**

```elixir
defmodule Conversor.Temperatura do
  @moduledoc """
  Conversão entre Celsius e Fahrenheit.
  """

  @doc """
  Converte Celsius para Fahrenheit.

      iex> Conversor.Temperatura.c_para_f(0)
      32.0
  """
  def c_para_f(c) when is_number(c), do: (c * 1.8) + 32

  @doc """
  Converte Fahrenheit para Celsius.

      iex> Conversor.Temperatura.f_para_c(212)
      100.0
  """
  def f_para_c(f) when is_number(f), do: (f - 32) / 1.8
end
```

> 💡 Uma coisa interessante sobre módulos no Elixir é que eles costumam usar nomes com namespaces para formar uma estrutura mais organizada, como `Conversor.Temperatura`. Isso ajuda a deixar o código mais legível e bem dividido, além de permitir uma organização estrutural, mostrando claramente a que parte do sistema cada módulo pertence. É uma convenção comum na linguagem, que facilita entender a função de cada módulo só pelo nome, além de evitar confusão com outros módulos parecidos.

## App integrador: `Main`

Para usar nossos apps, iremos implementar um app principal para chamarmos direto do terminal. Pela simplicidade, vamos implementar uma simples aplicação de terminal com captura de input.

Não é para ser algo bonito, é só para mostrar como podemos rodar nosso projeto do terminal, mas serve facilmente para entender como funciona o ponto de entrada para nossa aplicação.

No `mix.exs` do `main`, declaramos dependências para os outros dois apps:

**apps/main/mix.exs:**

```elixir
defp deps do
  [
    {:conversor_temperatura, in_umbrella: true},
    {:conversor_distancia, in_umbrella: true}
  ]
end
```

> 💡 Em projetos do tipo *umbrella*, cada app é isolado em sua própria pasta, mas todos compartilham o mesmo ambiente de execução, o que permite que módulos definidos em um app sejam utilizados em outro. Para isso, basta declarar a dependência no `mix.exs` do app que irá consumir (com `{:nome_do_app, in_umbrella: true}`), como fizemos em `main`, e os módulos ficam disponíveis automaticamente para uso, sem necessidade de configuração adicional. Isso torna a comunicação entre os apps simples e direta, mantendo a modularização do projeto.

O código interativo:

**apps/main/lib/main.ex:**

```elixir
defmodule Main do
  def main do
    IO.puts("Digite uma temperatura em Celsius:")
    celsius = get_float_input()
    fahrenheit = Conversor.Temperatura.c_para_f(celsius)
    IO.puts("Em Fahrenheit: #{fahrenheit}")

    IO.puts("Digite uma distância em metros:")
    metros = get_float_input()
    ft = Conversor.Distancia.m_para_ft(metros)
    IO.puts("Em pés: #{Float.round(ft, 4)}")
  end

  defp get_float_input do
    input = IO.gets("> ") |> String.trim()
    case Float.parse(input) do
      {valor, ""} -> valor
      _ ->
        IO.puts("Entrada inválida, tente novamente.")
        get_float_input()
    end
  end
end
```

> ⚠️ **Aviso**: Em projetos futuros não iremos usar esse modo de rodar o projeto, ele serve só de exemplo para podermos interagir com o projeto de forma *standalone*.

## Compilação e execução standalone

Para compilar todo o projeto não têm muito segredo:

```bash
mix compile
```

Isso irá criar uma pasta `_build` na raiz do nosso projeto. Essa pasta é sempre gerada automaticamente, então pode ser descartada do gerenciador de versões em uso.

Para rodar nosso projeto de forma *standalone*, temos três formas diferentes de rodar. Vamos passar por cada uma abaixo:

### Usando mix run

Não têm muito o que falar, só mostrar:

```bash
mix run -e 'Main.main'
```

> ⚠️ **Aviso**: Apesar de existir a opção de fazermos a execução usando `mix run` sem parâmetros, isso pode causar problemas inesperados com outras partes da execução do projeto (como testes, compilação ou Servers), pois o `mix run` por padrão executa um script, ou, quando você define uma application com `mod: {Main, []}`, em que ele chama `start/2` e se a função `start/2` não estiver bem configurada, podemos gerar problemas de difícil depuração, por isso não iremos abordar esse método aqui. Mas se quiser verificar, você pode checar na documentação do [start/2 no módulo Application](https://hexdocs.pm/elixir/Application.html#c:start/2), na documentação do Elixir.

### Usando Aliases

Para fazermos a execução usando alias no comando `mix`, vamos criar um novo alias no projeto. Para isso, configure o `mix.exs` da raiz:

**mix.exs:**

```elixir
defp aliases do
  [
    conversor_main: "run -e 'Main.main'"
  ]
end
```

Será necessário colocar também a linha `aliases: aliases()` no `project` do `mix.exs` da raiz. Feito isso, é só rodar o comando que o código interativo de Main será executado.

```bash
mix conversor_main
```

Esse comando é o equivalente a rodarmos, no terminal:

```bash
mix run -e 'Main.main'
```

### Usando Mix.Tasks

Aqui vamos criar um novo arquivo em `apps/main/lib/mix/tasks/conversor_task.ex`, que também cria um alias no mix, com o seguinte conteúdo:

**apps/main/lib/mix/tasks/conversor_task.ex:**

```elixir
defmodule Mix.Tasks.ConversorTask do
  use Mix.Task

  @shortdoc "Executa a aplicação interativa do conversor"
  def run(_args) do
    # Garante que os apps do projeto estão carregados
    Mix.Task.run("app.start")

    # Chama a função interativa
    Main.main()
  end
end
```

Criada a task, conseguiremos rodar nossa aplicação com a task nova criada.

```bash
mix conversor_task
```

> 💡 Para simplificar um pouco, usamos uma nomenclatura que nos permite ver quais os comandos que criamos, caso haja dúvidas. Ao rodar `mix help | grep conversor` iremos ver só os comandos que nós criamos.

## Usando IEx com projetos umbrella

Com o projeto estruturado, você pode iniciar um console interativo a partir da raiz do projeto umbrella com:

```bash
iex -S mix
```

Isso compila e carrega todas as aplicações definidas em `apps/`. Feito isso, você pode interagir com qualquer módulo dentro do projeto:

```elixir
iex> Conversor.Temperatura.f_para_c(212)
100.0
iex> Conversor.Distancia.m_para_ft(10)
32.8084
```

## Testes

Vamos adicionar testes automatizados para os nossos módulos. Cada módulo possui seus testes, organizados em arquivos separados com `ExUnit`. Usaremos valores aleatórios gerados pela seed do ExUnit, garantindo reprodutibilidade com o comando `mix test --seed <valor>`. Isso é útil para capturar inconsistências sutis em cálculos com ponto flutuante.

### Testes para `Conversor.Distancia`

**apps/conversor_distancia/test/conversor_distancia_test.exs:**

```elixir
defmodule Conversor.DistanciaTest do
  use ExUnit.Case, async: true
  doctest Conversor.Distancia

  describe "Teste do Conversor de Distâncias" do
    test "m_para_ft/1 com inteiro aleatório" do
      valor = :rand.uniform(100)
      esperado = valor * 3.28084
      assert_in_delta Conversor.Distancia.m_para_ft(valor), esperado, 0.0001
    end

    test "ft_para_m/1 com inteiro aleatório" do
      valor = :rand.uniform(100)
      esperado = valor / 3.28084
      assert_in_delta Conversor.Distancia.ft_para_m(valor), esperado, 0.0001
    end
  end
end
```

### Testes para `Conversor.Temperatura`

**apps/conversor_temperatura/test/conversor_temperatura_test.exs:**

```elixir
defmodule Conversor.TemperaturaTest do
  use ExUnit.Case, async: true
  doctest Conversor.Temperatura

  describe "Teste do Conversor de Temperaturas" do
    test "c_para_f/1 com inteiro aleatório" do
      valor = :rand.uniform(100) - 50
      esperado = (valor * 1.8) + 32
      assert_in_delta Conversor.Temperatura.c_para_f(valor), esperado, 0.0001
    end

    test "f_para_c/1 com inteiro aleatório" do
      valor = :rand.uniform(212)
      esperado = (valor - 32) / 1.8
      assert_in_delta Conversor.Temperatura.f_para_c(valor), esperado, 0.0001
    end
  end
end

```

### Teste para a chamada interativa de `Main`

**apps/main/test/main_test.exs:**

```elixir
defmodule MainTest do
  use ExUnit.Case
  import ExUnit.CaptureIO

  test "main/0 realiza interação com o usuário" do
    output =
      capture_io("100\n10\n", fn ->
        Main.main()
      end)

    assert output =~ "Digite uma temperatura em Celsius:"
    assert output =~ "Em Fahrenheit: 212.0"
    assert output =~ "Digite uma distância em metros:"
    assert output =~ "Em pés: 32.8084"
  end
end
```

Para executar todos os testes, é só rodar na raiz:

```bash
mix test
```

Se quiser ver os testes de forma completa:

```bash
mix test --trace
```

Ou testar apenas um app:

```bash
cd apps/conversor_distancia
mix test
```

A separação por apps facilita testes unitários isolados e estimula boas práticas.

## Conclusão

Neste post, criamos um projeto guard-chuva com três apps Elixir. Com ele, aprendemos a:

- Organizar um sistema modular e escalável
- Integrar múltiplos apps com dependências locais
- Utilizar `iex`, `mix test`, `mix compile` e `mix run` de forma produtiva

Além disso, reforçamos a idéia de que **apps no Elixir** são unidades organizacionais que permitem estruturar bem o código. Ao usar nomes como `Conversor.Temperatura` e `Conversor.Distancia`, deixamos clara a intenção e responsabilidade de cada parte do sistema.

Essa estrutura favorece a clareza, testes isolados e evolução contínua de sistemas mais robustos.

## Referências 🔗

- [Documentação oficial do Elixir](https://elixir-lang.org/)
- [Guia oficial do Mix](https://hexdocs.pm/mix/Mix.html)
- [Umbrella Projects no Elixir School](https://elixirschool.com/en/lessons/advanced/umbrella_projects/)
- [Testing no Elixir School](https://elixirschool.com/en/lessons/testing/basics)
- [Custom Mix Tasks no Elixir School](https://elixirschool.com/en/lessons/intermediate/mix_tasks)

