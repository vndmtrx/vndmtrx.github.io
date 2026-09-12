---
layout: post
title: "Criando chaves SSH e GPG para o GitHub"
subtitle: "Um guia prático para gerar chaves Ed25519 e assinar seus commits com segurança"
author:
  - "Eduardo N. S. R."
date: 2025-09-11 23:13:00 GMT-3
modified_date: 2026-05-10 10:26:00 GMT-3
permalink: /posts/ssh-gpg-github/
tags: [SSH, GPG, Git, Github]
series: OpenSSH na Prática
---

Não sei se vocês passam por isso, mas frequentemente eu troco minhas chaves SSH e GPG que uso no GitHub. Às vezes por precaução, mas a maioria das vezes é por esquecimento mesmo. E todas as vezes que vou criar novas chaves é o mesmo parto. Em vista disso, resolvi resumir um pouco o trabalho que é fazer toda essa via sacra de criação. Não chega a ser complicado, mas ter esses passos resumidos em um só lugar ajuda.

## Gerando a Chave SSH

Primeiro, vamos criar a chave SSH. Hoje, a recomendação prática e padrão ouro da indústria é usar **ED25519** [^1] (curta, rápida e matematicamente robusta):

```bash
ssh-keygen -t ed25519 -a 100 -C "seu-email@exemplo.com"
```

*Gera o par de chaves ED25519 com 100 rodadas de KDF para retardar ataques de força bruta contra a passphrase.*

> [!TIP] Dica
> O parâmetro `-a 100` define o número de rodadas da função de derivação de chave (KDF). Isso aumenta significativamente o custo computacional para um atacante tentar quebrar a sua senha por força bruta caso obtenha o arquivo da chave privada.

Durante a execução, o utilitário solicitará o caminho de destino (o padrão `~/.ssh/id_ed25519` é o mais indicado) e uma *passphrase* forte.

Depois de gerada a chave, adicionamos a identidade ao `ssh-agent` local:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

*Inicializa o agente SSH em background e carrega a chave privada na memória da sessão.*

Agora basta copiar o conteúdo da chave pública e adicioná-lo à sua conta do GitHub em *Settings -> SSH and GPG keys -> New SSH key* [^2]:

```bash
cat ~/.ssh/id_ed25519.pub
```

*Exibe o conteúdo da chave pública ED25519 para cópia no clipboard.*

## Criando e Configurando a Chave GPG

Não sei vocês, mas eu gosto de assinar todos os commits que faço. Não que isso mude algo na minha vida ou na vida de alguém, mas quando você pega esse costume, é difícil depois você parar. Em vista disso, vamos mostrar como criar sua chave GPG [^3], que na verdade é bem simples:

```bash
gpg --full-generate-key
```

*Inicia o assistente interativo do GnuPG para geração de par de chaves assimétricas completas.*

Serão feitas algumas perguntas: tipo e tamanho da chave (pode manter RSA 4096 ou ECC com ED25519/CV25519), além dos seus dados de nome e e-mail. Por último, defina uma senha segura para a chave.

Para listar as chaves existentes e obter o *Key ID* de assinatura:

```bash
gpg --list-keys --keyid-format LONG
```

*Lista todas as chaves públicas cadastradas exibindo os identificadores em formato longo de 16 caracteres hexadecimais.*

Para exportar a chave pública em formato ASCII e colar no GitHub (em *Settings -> SSH and GPG keys -> New GPG key*):

```bash
gpg --armor --export XXXXXXXX
```

*Exporta a chave pública indicada pelo Key ID em bloco de texto ASCII armored.*

Substitua `XXXXXXXX` pelo identificador da chave pública (indicado na linha `pub` da saída do comando anterior).

Agora, para instruir o Git a assinar seus commits automaticamente com essa chave:

```bash
git config --global user.signingkey XXXXXXXX
git config --global commit.gpgsign true
```

*Configura a chave de assinatura global no Git e ativa a assinatura automática em todos os commits.*

Caso você utilize identidades corporativas e pessoais separadas na mesma máquina, basta omitir a flag `--global` e executar o comando na raiz de cada repositório específico.

## Alternativa: Assinando Commits com a Própria Chave SSH

Se você já vive de SSH e quer simplificar o ecossistema sem gerenciar um chaveiro GPG separado, o Git suporta nativamente a assinatura criptográfica usando a sua própria chave SSH [^4].

No GitHub, adicione sua chave pública SSH (`~/.ssh/id_ed25519.pub`) também como **Signing Key** (é uma categoria separada das chaves normais de autenticação).

Em seguida, instrua o Git a usar o formato SSH para assinatura e aponte o caminho da chave pública:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

*Define o OpenSSH como formatador de assinaturas do Git e vincula a chave pública do arquivo local.*

A partir daqui, todo `git commit` sairá assinado digitalmente com a sua chave SSH (esse recurso requer Git versão 2.34 ou superior).

Se preferir assinar manualmente apenas commits pontuais em vez de ativar a flag global, basta passar o argumento `-S`:

```bash
git commit -S -m "feat: adiciona pipeline de autenticação"
```

*Cria um novo commit assinado criptograficamente com a chave configurada.*

## Conclusão

Ter suas chaves SSH e GPG devidamente configuradas garante tanto a segurança das suas conexões quanto a autenticidade e rastreabilidade do código que você envia para o GitHub. Seja assinando via GPG tradicional ou aproveitando a simplicidade moderna das assinaturas com chaves SSH, o processo elimina qualquer dúvida sobre a autoria dos seus commits e protege a integridade do seu fluxo de trabalho.

## Referências

[^1]: **ssh-keygen(1) - Linux manual page** {*man7.org*} ([Link](https://man7.org/linux/man-pages/man1/ssh-keygen.1.html))

[^2]: **Adding a new SSH key to your GitHub account** {*GitHub Docs*} ([Link](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account))

[^3]: **The GNU Privacy Guard Manual** {*GnuPG.org*} ([Link](https://www.gnupg.org/documentation/manuals/gnupg/))

[^4]: **Signing commits with SSH keys** {*GitHub Docs*} ([Link](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification#ssh-commit-signature-verification))
