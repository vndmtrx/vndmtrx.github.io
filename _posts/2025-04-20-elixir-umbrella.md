---
layout: post
title: "Aprendendo Elixir - Estrutura Modular com Umbrella"
subtitle: "Organizando aplicações complexas e domínios independentes com projetos guarda-chuva"
author:
  - "Eduardo N. S. R."
date: 2025-04-20 15:46:00 GMT-3
modified_date: 2026-05-10 10:26:00 GMT-3
permalink: /posts/elixir-umbrella/
tags: [Programação, Programação Funcional, Elixir]
series: Aprendendo Elixir
---

Neste segundo post da série *Aprendendo Elixir* [^1], vamos explorar como organizar projetos maiores usando arquitetura modular com uma estrutura guarda-chuva (chamada *Umbrella* pelo ecossistema Elixir). A proposta é dividir o sistema em múltiplas aplicações menores, focadas e coesas, que podem ser desenvolvidas, testadas e integradas dentro de um mesmo repositório sob o comando do Mix. Esse modelo segue o princípio de separação de responsabilidades, facilitando a manutenção e a escalabilidade do código.

Os exemplos deste post estão disponíveis na pasta [02-umbrella](https://github.com/vndmtrx/estudo_elixir/tree/main/02-umbrella) do [repositório de estudos](https://github.com/vndmtrx/estudo_elixir). Para demonstrar o conceito na prática, construímos um conversor unificado composto por três aplicações internas: o `conversor_temperatura` (cálculos entre Celsius e Fahrenheit), o `conversor_distancia` (conversões entre metros e pés) e o app integrador `main`, responsável por orquestrar as entradas do usuário no terminal.

## Por que usar um projeto Guarda-Chuva?

Projetos Guarda-Chuva são ideais quando queremos modularizar funcionalidades de forma clara e reaproveitável, separar domínios de negócio independentes (como APIs, persistência e workers em background) e gerenciar dependências locais entre subprojetos sem a necessidade de publicar pacotes no Hex.

Cada subaplicação mantém seu próprio ciclo de vida, arquivos de configuração e suíte de testes unitários isolados, ao mesmo tempo em que podem ser carregadas e executadas conjuntamente a partir da raiz. O Elixir lida com essa organização com muita naturalidade graças à arquitetura de aplicações OTP da BEAM [^3].

## Criando o projeto guarda-chuva

Para criar o projeto guarda-chuva principal no terminal, execute:

```bash
mix new conversor --umbrella
cd conversor
```

*Cria a estrutura base do projeto umbrella e entra no diretório raiz da aplicação.*

A flag `--umbrella` inicializa a estrutura com a pasta `apps/`, onde viverão todas as nossas subaplicações.

> ⚠️ *Aviso*: A partir daqui, sempre que falarmos da **raiz** do projeto, estamos nos referindo a esta pasta inicial criada com o comando acima.

Agora, dentro do diretório `apps`, criamos os três subprojetos independentes:

```bash
cd apps
mix new conversor_distancia
mix new conversor_temperatura
mix new main
```

*Inicializa cada uma das três subaplicações dentro da pasta apps.*

## Estrutura do projeto

A árvore de diretórios resultante para os arquivos que iremos trabalhar fica assim:

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

> ⚠️ *Aviso*: Esta listagem resume apenas os arquivos principais de lógica e teste para mantermos o foco didático.

O arquivo `mix.exs` [^2] da raiz define que o projeto é do tipo umbrella através da opção `apps_path: "apps"`, centralizando a compilação e a execução dos testes.

## Implementando os apps

### Módulo Conversor.Distancia

Este app lida exclusivamente com conversões métricas entre metros e pés.

**Arquivo:** `apps/conversor_distancia/lib/conversor_distancia.ex`

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

*Implementa funções de conversão métrica com guards numéricos e doctests de precisão.*

### Módulo Conversor.Temperatura

Este app implementa as fórmulas de conversão entre escalas termométricas:

**Arquivo:** `apps/conversor_temperatura/lib/conversor_temperatura.ex`

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

*Implementa conversões de temperatura entre escalas Celsius e Fahrenheit.*

> 💡 *Nota*: Uma convenção comum e elegante no Elixir é usar nomes com namespaces modulares, como `Conversor.Temperatura` e `Conversor.Distancia`. Isso organiza a estrutura de pacotes, evita conflitos de identificadores e esclarece imediatamente o domínio de cada função.

## App Integrador: Main

Para consumir nossos módulos, implementamos um app principal chamado `main` para rodar diretamente no terminal com captura de input interativo.

No `mix.exs` do app `main`, declaramos a dependência local para os outros dois subprojetos via `in_umbrella: true`:

**Arquivo:** `apps/main/mix.exs`

```elixir
defp deps do
  [
    {:conversor_temperatura, in_umbrella: true},
    {:conversor_distancia, in_umbrella: true}
  ]
end
```

*Declara dependências internas do projeto guarda-chuva utilizando a opção in_umbrella.*

> 💡 *Nota*: Em projetos umbrella, cada app vive isolado em sua própria pasta, mas todos compartilham o mesmo ambiente de execução na compilação. Ao adicionar `in_umbrella: true`, os módulos dos apps dependentes ficam imediatamente disponíveis no namespace sem necessidade de configurações adicionais.

O módulo interativo de terminal:

**Arquivo:** `apps/main/lib/main.ex`

```elixir
defmodule Main do
  def main do
    IO.puts("Digite uma temperatura em Celsius:")
    celsius = get_float_input()
    fahrenheit = Conversor.Temperatura.c_para_f(celsius)
    IO.puts("#{celsius}°C equivalem a #{Float.round(fahrenheit, 2)}°F")

    IO.puts("\nDigite uma distância em metros:")
    metros = get_float_input()
    pes = Conversor.Distancia.m_para_ft(metros)
    IO.puts("#{metros}m equivalem a #{Float.round(pes, 2)}ft")
  end

  defp get_float_input do
    case IO.gets("> ") |> String.trim() |> Float.parse() do
      {valor, _} ->
        valor

      _ ->
        IO.puts("Entrada inválida, tente novamente.")
        get_float_input()
    end
  end
end
```

*Orquestra as chamadas aos conversores recebendo entradas do usuário e tratando parsing inválido recursivamente.*

> ⚠️ *Aviso*: Em aplicações corporativas dificilmente usaremos loop de console interativo dessa forma; trata-se apenas de um exemplo simples para demonstrar a orquestração e execução de múltiplos módulos locais.

## Compilação e execução standalone

Para compilar todos os subprojetos da árvore ao mesmo tempo, execute na raiz:

```bash
mix compile
```

*Compila todo o projeto umbrella gerando os binários unificados dentro do diretório `_build`.*

Para executar o ponto de entrada da aplicação, temos três abordagens práticas:

### Usando mix run

A forma mais direta de rodar uma função específica a partir da linha de comando:

```bash
mix run -e 'Main.main'
```

*Executa a função `Main.main/0` carregando todo o contexto do projeto umbrella.*

### Usando Aliases no Mix

Podemos definir atalhos customizados no arquivo `mix.exs` da raiz:

**Arquivo:** `mix.exs`

```elixir
defp aliases do
  [
    conversor_main: "run -e 'Main.main'"
  ]
end
```

*Configura um alias customizado no Mix apontando para o comando de execução.*

Adicione também a opção `aliases: aliases()` na função `project` do `mix.exs`. Feito isso, basta rodar:

```bash
mix conversor_main
```

*Executa o alias definido no Mix chamando a função principal do console.*

### Usando Mix.Tasks

Outra abordagem flexível é criar uma Mix Task dedicada em `apps/main/lib/mix/tasks/conversor_task.ex` [^5]:

**Arquivo:** `apps/main/lib/mix/tasks/conversor_task.ex`

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

*Define uma tarefa Mix oficial para inicializar a aplicação e disparar a rotina interativa.*

Com a task declarada, você pode invocá-la normalmente pelo Mix:

```bash
mix conversor_task
```

*Roda a Mix Task recém-criada a partir de qualquer nível do projeto.*

> 💡 *Dica*: Ao rodar `mix help | grep conversor`, o Mix listará automaticamente a sua task com o resumo que você definiu no `@shortdoc`.

## Usando IEx com projetos umbrella

Você pode carregar todas as aplicações no console interativo a partir da raiz com:

```bash
iex -S mix
```

*Abre o shell IEx com todos os subprojetos e dependências compilados e disponíveis.*

Com isso, podemos testar os módulos diretamente no terminal:

```elixir
iex> Conversor.Temperatura.f_para_c(212)
100.0
iex> Conversor.Distancia.m_para_ft(10)
32.8084
```

*Testa interativamente chamadas aos módulos de temperatura e distância no IEx.*

## Testes Automatizados

Vamos adicionar testes com `ExUnit` [^4] para cada aplicação. Usaremos geradores aleatórios controlados pela seed do ExUnit para testar intervalos numéricos com precisão flutuante.

### Testes para Conversor.Distancia

**Arquivo:** `apps/conversor_distancia/test/conversor_distancia_test.exs`

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

*Valida conversões de distância com delta de precisão em ponto flutuante sobre entradas aleatórias.*

### Testes para Conversor.Temperatura

**Arquivo:** `apps/conversor_temperatura/test/conversor_temperatura_test.exs`

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

*Testa as fórmulas de conversão termométrica cobrindo números positivos e negativos.*

### Teste para a Chamada Interativa de Main

**Arquivo:** `apps/main/test/main_test.exs`

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

*Utiliza `CaptureIO` para simular entrada de usuário no terminal e validar as saídas geradas pelo app.*

Para rodar todos os testes de todas as subaplicações em paralelo:

```bash
mix test
```

*Executa os testes de todos os subprojetos a partir da raiz do umbrella.*

Se quiser inspecionar cada teste individualmente:

```bash
mix test --trace
```

*Executa a suíte detalhando cada caso de teste executado no terminal.*

Ou executar os testes de apenas um dos subapps:

```bash
cd apps/conversor_distancia
mix test
```

*Executa os testes isoladamente dentro da pasta do subprojeto específico.*

## Conclusão

Neste post, criamos um projeto guarda-chuva completo com três apps Elixir. Vimos como modularizar funcionalidades com responsabilidades bem divididas, integrar subprojetos por meio de dependências locais `in_umbrella` e operar ferramentas essenciais como `iex`, `mix test`, `mix compile` e criação de tasks customizadas.

A estrutura de projetos guarda-chuva reforça a clareza e a manutenibilidade do código, permitindo que cada parte do sistema evolua com sua própria suíte de testes sem perder a coesão do ecossistema geral.

## Referências

[^1]: **Documentação oficial do Elixir** {*Elixir Lang*} ([Link](https://elixir-lang.org/))

[^2]: **Guia oficial do Mix** {*HexDocs*} ([Link](https://hexdocs.pm/mix/Mix.html))

[^3]: **Umbrella Projects** {*Elixir School*} ([Link](https://elixirschool.com/en/lessons/advanced/umbrella_projects/))

[^4]: **Testing** {*Elixir School*} ([Link](https://elixirschool.com/en/lessons/testing/basics/))

[^5]: **Custom Mix Tasks** {*Elixir School*} ([Link](https://elixirschool.com/en/lessons/intermediate/mix_tasks/))
