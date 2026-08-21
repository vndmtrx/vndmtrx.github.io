---
layout: post
title: "A Catedral, o Bazar e o Jardim"
subtitle: "Como a era da inteligência artificial está transformando a criação de software em um cultivo pessoal e hiperlocal"
author:
- "Eduardo N. S. R."
date: 2026-05-17 06:43:00 GMT-3
permalink: /posts/catedral-bazar-jardim/
tags: [Programação, Análise de Sistemas, Inteligência Artificial]
---

A forma como descrevemos o desenvolvimento de software diz muito sobre como escolhemos construí-lo. Por muito tempo, tentamos nos convencer de que éramos engenheiros erguendo estruturas imutáveis de concreto e aço, seguindo plantas rígidas e previsíveis. Mas quem vive o dia a dia do código sabe que essa caixa de ferramentas não dá conta da realidade: somos, na verdade, algo muito diferente disso.

Mas o tempo passa, as IAs começam a escrever código com a gente, e as metáforas também precisam daquela atualizada. Recentemente tropecei num texto genial do *vrypan* [^1] que joga uma luz sobre essa nova era em que estamos entrando. Para ele, o desenvolvimento de software hoje deixou o bazar e passou a ter a cara de uma... cozinha. E por mais que o texto dele seja maravilhoso, na minha visão nós não fomos para os fogões. Para mim, essa mudança apenas reforça o que eu já defendia antes: de que nós somos, fundamentalmente, **Jardineiros** [^2].

## Onde as Metáforas se Encontram

Para pegar a visão, a gente precisa dar um passo atrás e lembrar do clássico do Eric S. Raymond, *"A Catedral e o Bazar"* (1997) [^3], que definiu como a gente via a criação de software:
- A **Catedral** é o desenvolvimento nos moldes tradicionais: centralizado, super planejado e ditado por um grupo seleto de arquitetos.
- O **Bazar** é a colaboração aberta e descentralizada: grandes comunidades, desenvolvimento em praça pública, esforço distribuído. É o mito fundador do movimento *open source*. Por décadas, a ideia era essa: você joga o código no mundo pra atrair gente, dividir o trabalho e construir uma infraestrutura comunitária gigante. O código bom nascia da multidão.

Mas aí veio o Desenvolvimento Guiado por IA e deu uma bela balançada nas regras do jogo.

Hoje em dia, a IA está mudando tanto a economia quanto a ergonomia por trás daquele modelo. Escrever código ficou muito barato, mas coordenar pessoas continua sendo caro. Um único desenvolvedor, equipado com boas ferramentas de IA, consegue agora desenvolver sistemas inteiros que antes exigiam um time enorme.

Ao mesmo tempo, o software está ficando incrivelmente pessoal: feito sob medida para o fluxo de trabalho, o "clima" da infraestrutura e os hábitos de uma única pessoa. Em vez de construir ferramentas genéricas para o maior público possível, os desenvolvedores criam cada vez mais coisas que enraízam perfeitamente nos seus próprios problemas. Outros ainda podem ler o código, forkear o projeto, mas a modificação local muitas vezes se torna muito mais barata do que tentar coordenar o desenvolvimento com um repositório central.

E é aqui que pegamos as ideias do *vrypan* e as trazemos de volta para a terra (literalmente): o novo modelo é o **Jardim**.

## O Software como Jardim

Todo jardim evolui ao redor dos hábitos do seu jardineiro. As ferramentas de poda ficam onde são mais convenientes. Plantas são substituídas livremente se o solo não ajudar. A rega ganha alterações no puro instinto. Duas pessoas podem começar com as mesmíssimas sementes e terminar com jardins completamente diferentes.

Diferente do Bazar, um jardim é um espaço profundamente pessoal. Nós compartilhamos mudas e sementes (o código-fonte) livremente na internet, mas os jardins raramente convergem para um padrão universal. Quem visita pode até admirar a técnica de paisagismo de outro jardineiro, mas ainda vai voltar para casa e plantar do seu próprio jeito. Nesse modelo, o *open source* deixa de parecer uma praça pública onde todos opinam e enviam suas contribuições de mudas, esterco ou sistemas de irrigação, e se aproxima mais de um cultivo compartilhado: o software como um utilitário pessoal, aberto para todos verem, infinitamente adaptável, e cada vez mais criado por indivíduos ao invés de comunidades.

No modelo do Bazar, a abertura do código era basicamente uma forma de coordenar pessoas. Você abria as portas para atrair contribuidores, dividir o esforço braçal e erguer um monumento coletivo. No Jardim, abrir as portas tem outro propósito: dar visibilidade, permitir o aprendizado e garantir independência. O valor da coisa muda de *"outros podem me ajudar a plantar isso"* para *"outros podem entender, pegar umas mudas e dicas e fazer a sua própria versão"*.

O código-fonte passa a se assemelhar muito mais a receitas e manuais de cultivo do que a projetos de construção civil. A maioria das pessoas não fica enviando *patches* de correção para o livro de plantio da Palmirinha. Ainda assim, essas anotações continuam sendo imensamente valiosas porque transferem técnica, preservam conhecimento e dão uma base para que outros adaptem aos seus próprios climas. O código é aberto não para que todos sejam coautores, mas para que qualquer um possa estudá-lo, modificá-lo e torná-lo seu.

Isso muda até o que a gente entende por *forks* (bifurcações de código). No Bazar, eles muitas vezes eram vistos como falhas de governança. No Jardim, dar *fork* é normal e saudável:
- "Adaptei essa planta pro clima do meu setup"
- "Podei as features que eu não preciso"
- "Replantei isso aqui para o meu fluxo de trabalho"

Fazer um fork vira o equivalente exato a pegar um galho do vizinho para fazer uma muda em casa. O software passa a evoluir através da adaptação local, em vez do consenso centralizado.

E claro, nesse novo mundo existe muito atrito. Vemos diariamente o debate acalorado sobre o que a comunidade chama de "Slop" (código gerado por IA em massa e sem muito critério). É a velha briga entre o artesão purista e a automação: de um lado, o jardineiro que prefere as técnicas manuais; do outro, quem usa o "trator" da IA para espalhar sementes numa velocidade absurda. Existe até quem brinque que, nessa era de *vibe coding*, não estamos mais programando, mas sim "emocionando" o software [^4], o que pode gerar tanto um jardim exuberante quanto um terreno cheio de ervas daninhas. No fim das contas, a IA é uma ferramenta poderosa, e cabe ao jardineiro (ou ao "emocionador" consciente) saber podar e guiar esse crescimento para que o resultado final tenha alma e propósito. No fim do dia, ambos estão cuidando do seu pedaço de chão.

Na verdade, muito da história da programação já funcionava assim. Pense na cultura de customização do Unix, nos scripts pessoais de shell, ou naqueles *dotfiles* que você compartilha no GitHub pra mostrar como o seu sistema é configurado (mas que quase ninguém copia linha por linha sem mudar nada). São sistemas altamente pessoais compartilhados publicamente, não produtos de engenharia colaborativa.

## Conclusão

Chegando no fim dessa reflexão, tanto a analogia da "Cozinha" do *vrypan* quanto a do "Jardim" são extremamente válidas e boas. Elas capturam bem esse novo cenário que estamos vivendo: com o desenvolvimento guiado por IA, caminhamos para um mundo com menos "grandes silos centralizados" e mais desenvolvimentos hiper-pessoais.

O código aberto continua sendo essencial porque ele preserva a nossa agência: a habilidade de inspecionar, consertar e remodelar o software independentemente do seu autor original. O resultado é um ecossistema mais pessoal, onde as ideias e técnicas circulam livremente, como pólen voando de jardim em jardim.

Nós não somos engenheiros. Somos jardineiros.

## Referências

[^1]: **The Cathedral, the Bazaar and the Kitchen** {*vrypan, Mai/2026*} ([Link](https://blog.vrypan.net/2026/05/11/the-cathedral-the-bazaar-and-the-kitchen/))

[^2]: **Você não é um Engenheiro de Software** {*Eduardo N. S. R., Ago/2023*} ([Link](/posts/jardineiro-software/))

[^3]: **The Cathedral and the Bazaar** {*Eric S. Raymond, 1997*} ([Link](http://www.catb.org/~esr/writings/cathedral-bazaar/cathedral-bazaar/))

[^4]: **Emocionador de Software** {*@usuario@instancia.org, Mar/2025*} ([Link](https://instancia.org/@usuario/116267257747033441/))
