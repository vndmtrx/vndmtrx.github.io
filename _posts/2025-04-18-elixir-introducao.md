---
layout: post
title: "Aprendendo Elixir - Introdução"
author: "Eduardo N. S. R."
date: 2025-04-18 15:09:00
permalink: /posts/elixir-introducao/
tags: [Programação, Programação Funcional, Elixir, Mix, ExUnit]
---

Este post inaugura uma série intitulada *Aprendendo Elixir*, na qual registro minha jornada de aprendizado com essa linguagem. Minha ideia aqui é descrever meu aprendizado — e escrever sobre isso é uma forma de consolidar esse processo. Ao longo dos próximos módulos, iremos construir uma base sólida em Elixir por meio de projetos práticos, cada um introduzindo novos conceitos e boas práticas da programação funcional. Espero que este conteúdo te ajude tanto quanto está me ajudando.

Sempre tive afinidade com linguagens funcionais. Meu primeiro contato foi ainda nos anos 90, em que usava AutoLisp, no AutoCAD R14. O AutoLisp me criou o interesse para o paradigma funcional de forma inesperada. Mais tarde, usei Python extensivamente, não apenas por sua clareza sintática, mas principalmente pelos recursos funcionais que ele mescla com programação imperativa e orientação a objetos. Também sempre tive bastante apreço por Java: mesmo não sendo funcional, sua estrutura e clareza sempre me pareceram convidativas à manutenção e organização do código.

Agora, com Elixir, sinto um misto desses mundos: a elegância da sintaxe, combinada com o poder do paradigma funcional. Recursos como o operador `|>` (pipe) e o pattern matching são conceitos que eu nunca havia usado diretamente em outras linguagens, e vou abordar cada um deles com calma nos próximos posts 🙂

## Entendendo o Elixir e sua proposta

💡 Antes de começarmos a codificar, vale uma breve introdução à linguagem Elixir. Elixir é uma linguagem de programação funcional, concorrente e tolerante a falhas, construída sobre a máquina virtual do Erlang (BEAM). Essa base permite que aplicações Elixir herdem características como escalabilidade massiva, alta disponibilidade e comunicação entre processos leves, o que torna a linguagem uma escolha excelente para sistemas distribuídos, aplicações em tempo real e arquiteturas resilientes.

Por ser funcional, Elixir adota conceitos como imutabilidade de dados e funções puras. Isso favorece a previsibilidade do código e simplifica testes e paralelismo. Além disso, Elixir possui uma sintaxe moderna e acessível, e integra ferramentas como o `mix` (para gerenciamento de projetos) e o `ExUnit` (para testes automatizados), o que torna o ecossistema produtivo e acolhedor para desenvolvedores iniciantes e experientes.

Neste primeiro módulo, configurei meu ambiente com ASDF, criei um projeto simples com `mix` e implementei uma função básica acompanhada de testes automatizados com `ExUnit`. Tudo isso dentro de uma estrutura clara e replicável — e todos os exemplos deste módulo estão disponíveis no item [01-saudacao](https://github.com/vndmtrx/estudo_elixir/tree/main/01-saudacao), e os demais estarão organizados no [repositório principal do projeto](https://github.com/vndmtrx/estudo_elixir) 🧰

## Instalação do ASDF e das dependências

> ⚠️ **Aviso**: este guia de instalação foi testado no Debian 12 (Bookworm). Os comandos e pacotes listados podem variar ligeiramente dependendo da sua distribuição Linux ou sistema operacional. Usuários de Arch, Fedora, macOS ou Windows podem precisar adaptar os comandos conforme seus respectivos gerenciadores de pacotes ou ambientes. A documentação oficial do ASDF fornece instruções específicas para cada sistema.

### Requisitos de sistema
Antes de iniciar, é necessário instalar bibliotecas de desenvolvimento que permitirão compilar e utilizar tanto Erlang quanto Elixir. Se estiver usando um sistema baseado em Debian (como Ubuntu), execute:

```bash
sudo apt update && sudo apt install -y git curl autoconf \
  build-essential libssl-dev libncurses-dev unzip
```

Esses pacotes incluem compiladores, bibliotecas de SSL e ferramentas necessárias para o ASDF e as linguagens que serão instaladas.

### Clonagem do ASDF e configuração de ambiente
O ASDF é um gerenciador de versões universal. Ele permite manter múltiplas versões de linguagens em paralelo, o que é especialmente útil para desenvolvimento em ambientes diversos.

```bash
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.16.7

echo '. "$HOME/.asdf/asdf.sh"' >> ~/.bashrc
source ~/.bashrc
```

Esses comandos instalam o ASDF no diretório pessoal e o tornam acessível no terminal ao iniciar novas sessões de shell.

### Instalação dos plugins Erlang e Elixir

Agora, adicionamos os plugins necessários e instalamos versões compatíveis:

```bash
asdf plugin add erlang
asdf plugin add elixir

asdf install erlang 27.3.2
asdf install elixir 1.18.3-otp-27

asdf global erlang 27.3.2
asdf global elixir 1.18.3-otp-27
```

💡 Você também pode definir versões específicas para um projeto, o que é muito útil em ambientes com múltiplas aplicações ou para garantir reprodutibilidade. No meu caso, usei os seguintes comandos dentro da pasta do projeto, o que criou um arquivo `.tool-versions` com as versões desejadas:

```bash
asdf set erlang 27.3.2
asdf set elixir 1.18.3-otp-27
```

Isso garante que, ao entrar no diretório do projeto, o ASDF carregue automaticamente as versões corretas.

## Criação do primeiro projeto Elixir

```bash
mix new saudacao
cd saudacao
```

> ⚠️ **Aviso**: O nome da pasta no repositório que estou apresentando pode divergir do apresentado aqui. No repositório usei `01-saudacao` unicamente para fins de organização visual, mas a idéia é a mesma.

O comando `mix new` cria a estrutura básica de um projeto Elixir. A pasta gerada conterá:

- `lib/saudacao.ex`: onde escreveremos nossa lógica principal;
- `test/saudacao_test.exs`: arquivo de testes automatizados com `ExUnit`;
- `mix.exs`: arquivo de configuração do projeto, contendo nome, versão, dependências, etc.

## Implementação da função principal

**Arquivo:** `lib/saudacao.ex`

```elixir
defmodule Saudacao do
  @moduledoc """
  Documentação para o módulo `Saudacao`
  - Módulo responsável por gerar saudações personalizadas
  """

  @doc """
  Retorna uma saudação com o nome informado.

  ## Exemplos

      iex> Saudacao.ola("Dudu")
      "Olá, Dudu!"

  """
  def ola(nome) when is_binary(nome) do
    "Olá, #{nome}!"
  end
end

```

Neste trecho, utilizamos dois blocos de documentação:

- `@moduledoc`: fornece uma descrição geral do módulo. É o texto que será exibido na documentação gerada com `ExDoc` ou acessado via `h Saudacao` no `iex`.
- `@doc`: documenta a função `ola/1`, incluindo um exemplo de uso interativo com `iex`. Esse bloco é especialmente útil para testes automáticos com ferramentas como `doctest`, além de facilitar a leitura da documentação.

A função `ola/1` recebe um argumento `nome` e retorna uma string interpolada com uma saudação. A cláusula `when is_binary(nome)` é um *guard* que restringe a execução dessa função apenas quando o argumento for uma string (ou seja, um binário em Elixir).

O *guard* `when is_binary(nome)` assegura que a função só será executada se o parâmetro `nome` for uma string, o que evita chamadas incorretas e reforça a expressividade do código.

### Testando no IEx

Para testar essa função de forma interativa, você pode carregar seu projeto no console do Elixir com o comando:

```bash
iex -S mix
```

Ao fazer isso a partir da raiz do projeto, o `iex` irá carregar todos os módulos e dependências definidos. Assim, você pode executar:

```elixir
Saudacao.ola("Dudu")
```

Isso é excelente para explorar a linguagem, testar funções rapidamente e experimentar variações sem recompilar tudo a cada alteração.

## Criação de testes com ExUnit

**Arquivo:** `test/saudacao_test.exs`

```elixir
defmodule SaudacaoTest do
  use ExUnit.Case, async: true
  doctest Saudacao

  describe "ola/1" do
    test "retorna uma saudação personalizada" do
      assert Saudacao.ola("Dudu") == "Olá, Dudu!"
    end

    test "retorna corretamente com nomes diferentes" do
      assert Saudacao.ola("Leitor") == "Olá, Leitor!"
    end

    test "emite erro quando o argumento não é uma string" do
      assert_raise FunctionClauseError, fn ->
        Saudacao.ola(123)
      end
    end
  end
end
```

O bloco `use ExUnit.Case, async: true` habilita a execução paralela dos testes, útil em projetos com muitos arquivos.

A linha `doctest Saudacao` é responsável por transformar os exemplos presentes na anotação `@doc` do módulo `Saudacao` em testes automatizados. Isso significa que se o exemplo `Saudacao.ola("Dudu")` presente na documentação não funcionar, o teste irá falhar — garantindo que a documentação reflita sempre o comportamento real do código.

A macro `describe` permite agrupar os testes logicamente por função ou comportamento, facilitando a leitura da saída dos testes e sua manutenção. Cada `test` representa um cenário, e usamos `assert` para garantir que o valor retornado pela função seja o esperado.

Além de testes para comportamentos esperados, vamos também testar comportamentos não esperados na nossa implementação. Por exemplo, a função `ola/1` só aceita strings — isso é garantido pelo *guard* `when is_binary(nome)`. Se tentarmos passar um inteiro, a função irá falhar com um `FunctionClauseError`. Podemos testar esse comportamento usando `assert_raise`:

Para executar os testes, basta rodar:

```bash
mix test
```

## Considerações Finais

Este primeiro módulo dá uma base mínima, mas essencial, para começar com Elixir. Dá para ter uma noção do poder da modularização, como a linguagem valoriza a clareza das funções, e como o sistema de testes é integrado desde o início. Nos próximos posts, vou expandir esse projeto e explorar novos conceitos, mantendo sempre o foco na prática.

### Referências 🔗

- [Wikipedia — Elixir (linguagem de programação)](https://pt.wikipedia.org/wiki/Elixir_(linguagem_de_programa%C3%A7%C3%A3o))
- [Documentação oficial do Elixir](https://elixir-lang.org/)
- [Guia do Mix (oficial)](https://hexdocs.pm/mix/Mix.html)
- [Guia do ExUnit (oficial)](https://hexdocs.pm/ex_unit/ExUnit.html)
- [Documentação do ASDF](https://asdf-vm.com/)

