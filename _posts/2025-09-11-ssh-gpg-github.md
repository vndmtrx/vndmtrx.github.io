---
title: Criando chaves SSH e GPG para o Github
date: 2025-09-11 23:13:00
permalink: /posts/ssh-gpg-github/
tags: Git, Github, DevOps
---

Não sei se vocês passam por isso, mas frequentemente eu troco minhas chaves SSH e GPG que uso no GitHub. Às vezes por precaução, mas a maioria das vezes é por esquecimento mesmo. E todas as vezes que vou criar novas chaves é o mesmo parto. Em vista disso, resolvi resumir um pouco o trabalho que é fazer toda essa via sacra de criação. Não chega a ser complicado, mas ter esses passos resumidos em um só lugar ajuda.

### Chave SSH

Primeiro, vamos criar a chave SSH. Hoje, a recomendação prática é usar **ed25519** (curta, segura e rápida):

```bash
ssh-keygen -t ed25519 -a 100 -C "seu-email@exemplo.com"
```

> O `-a 100` dá uma temperada na proteção da sua chave privada.

Isso irá criar sua chave. Nas próximas telas, será perguntado o caminho onde será criada a chave. Eu geralmente uso o caminho padrão `~/.ssh/id_ed25519` que é fornecido.

Depois de criada a chave SSH, é hora de adicionar a mesma no `ssh-agent`.

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Agora é só copiar a chave pública (arquivo `~/.ssh/id_ed25519.pub`) e adicionar na sua conta do GitHub em *Settings -> SSH and GPG keys -> New SSH key*.

Se preferir um atalho na CLI, o comando abaixo exibe a chave pública:

```bash
cat ~/.ssh/id_ed25519.pub
```

### Chave GPG

Não sei vocês, mas eu gosto de assinar todos os commits que faço. Não que isso mude algo na minha vida ou na vida de alguém, mas quando você pega esse costume, é difícil depois você parar. Em vista disso, vamos mostrar como criar sua chave GPG, que na verdade é bem simples:

```
gpg --full-generate-key
```

Serão feitas algumas perguntas: tipo e tamanho da chave (pode manter RSA 4096 se quiser, mas ECC com ed25519/cv25519 também é comum), além dos seus dados. Por último, defina uma senha para a chave (não esqueça dela pelamordideos).

Para listar as chaves e pegar o Key ID:

```
gpg --list-keys --keyid-format LONG
```

Para exportar a pública e colar no GitHub (em *Settings → SSH and GPG keys → New GPG key*):

```
gpg --armor --export XXXXXXXX
```

Onde XXXXXXXX é o identificador da chave pública da sua chave GPG (indicado pelo sinal pub no comando anterior). O retorno desse comando é sua chave pública que você irá adicionar no github, na seção *GPG Keys*.

Agora, para assinar seus commits, você precisará setar sua chave pública como chave de assinatura:

```
git config --global user.signingkey XXXXXXXX
git config --global commit.gpgsign true
```

Aqui o identificador é o mesmo do comando anterior, que foi a chave gerada por você. Esse comando informará o git que todas as vezes que você for assinar um commit, ele irá usar essa chave. Caso você use diferentes usuários, você pode remover a opção `--global` do comando e configurar uma chave de assinatura para cada projeto que você desenvolve.

### Opção extra: Assinar commits com SSH

Se você já vive de SSH e quer simplificar, dá para assinar commits e tags com sua própria chave SSH.

No GitHub, adicione sua SSH pública também como Signing key (é uma entrada separada das chaves de autenticação; se for a mesma chave, suba duas vezes).

Feito isso, no Git, troque o formato de assinatura para SSH e aponte sua chave pública:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Pronto. A partir daqui, git commit já sai assinado (ou use `-S` se você não ativar o `commit.gpgsign`). 

Importante citar que esse recurso requer Git 2.34+. 

Feito isso, seja por GPG ou por SSH, para assinar seu commit, é simples. É só adicionar o parâmetro `-S` no seu comando de commit, como abaixo:

```
git commit -S -m "Mensagem de commit bonitinha"
```

---

Bom, é isso. Fica aqui o passo a passo centralizado para quando você trocar de máquina (ou de cabeça).
