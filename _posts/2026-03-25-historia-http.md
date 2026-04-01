---
layout: post
title: "Evolução do Protocolo HTTP e da World Wide Web"
author:
- "Eduardo N. S. R."
date: 2026-03-21 21:16:00 
modified_date: 2026-03-25 14:11:00 
permalink: /posts/evolucao-http/
tags: [HTTP, Web, Internet]
---

A história do protocolo HTTP e da World Wide Web está intimamente ligada, desde a sua fundação. Originalmente desenvolvido pelos cientistas do CERN, o HTTP vem passando por várias mudanças que mantiveram sua simplicidade ao passo que melhoraram sua flexibilidade para lidar com os cenários cada vez mais completos e modernos da Web com o passar dos anos. Pensado originalmente para troca de informações automatizadas entre cientistas entre universidades, tornou-se hoje em uma estrutura capaz de carregar imagens e vídeos de alta resolução, além de ser a base de praticamente todos os protocolos de troca de dados dos Web Services, seja em REST, seja RPC ou SOAP, para citar apenas estes.

A idéia básica do WWW e do HTTP era juntar tecnologias emergentes dos computadores, redes de comunicação e hipertexto em algo poderoso e fácil de usar como sistema de troca de informações, como uma grande teia de páginas, artigos, relatórios, ligados entre si. Daí o nome World Wide Web, ou em bom português: Grande Teia Global.

## Como tudo começou?

A primeira proposta para a WWW (que na época, foi chamada inicialmente de Mesh) foi feita pelo cientista Tim Berners-Lee [^12], em março de 1989 e no fim de 1990 ele e sua equipe já tinham desenvolvido o primeiro servidor web e o primeiro navegador para consumir esse conteúdo. O primeiro site criado estava no endereço info.cern.ch [^1] e ainda pode ser acessado nos dias de hoje. Construída em cima dos novos protocolos de rede TCP e IP, a WWW consistia de 4 blocos principais:

- Uma representação textual de documentos hipertexto (_HyperText Markup Language_ - **HTML**, derivado do SGML)
- Um protocolo para o compartilhamento desses documentos (_Hypertext Transfer Protocol_ - HTTP)
- Um cliente para mostrar (e editar) esses documentos (o primeiro navegador/editor chamava WorldWideWeb)
- Um servidor para dar acesso ao documento (uma versão inicial do httpd)

Com esses quatro blocos, a equipe do CERN liderada pelo Tim Berners-Lee desenvolveu o padrão e em agosto de 1991 fez o anúncio público no newsgroup alt.hypertext [^2].

## HTTP/0.9 - Um protocolo extremamente simples

A primeira "versão" do HTTP, lançada em 1991, não tinha versionamento. Ela foi chamada de 0.9 para diferenciar das outras versões que viriam depois. O **HTTP/0.9** era extremamente simples: requisições consistiam de uma única linha:

```
GET /minha-pagina.html
```

Onde o recurso minha página poderia ser qualquer coisa disponibilizada. A resposta também era extremamente simples, e consistia em simplesmente retornar o conteúdo do arquivo:

```html
<html>Uma página de texto</html>
```

Em termos do protocolo TCP, que foi o protocolo de transporte escolhido para servir o HTTP, basicamente o que acontecia era 

```
Cliente                                     Servidor
  | ---- SYN --------------------------------> |
  | <--- SYN+ACK ----------------------------- |
  | ---- ACK --------------------------------> |  (Conexão estabelecida)
  |                                            |
  | ---- "GET /index.html" ------------------> |
  |                                            |
  | <---- "<html>Conteúdo</html>" ------------ |  (conteúdo HTML)
  |                                            |
  | <--- FIN --------------------------------- |
  | ---- ACK --------------------------------> |  (Conexão fechada)
```

E essa era toda a essência do protocolo HTTP nessa versão. Não havia outros verbos além do `GET`, não havia cabeçalhos, não havia códigos de estado e nem de erro, e o servidor fechava a conexão TCP assim que terminava de enviar o recurso. No caso de algum erro (por exemplo, um arquivo inexistente), uma página era gerada e incluía uma descrição do problema. No entanto, para a época isso era o suficiente. Considerando tudo isso, protocolo HTTP e o WWW resolviam os seguintes problemas da época:

- Uma forma padronizada de se identificar recursos (Uniform Resource Identifiers - URIs ou URLs como conhecemos hoje)
- Uma forma de organização de documentos com possibilidade de links com outros documentos - HTML
- Uma forma de disponibilizar esse recursos/documentos de forma unificada.
- Era um protocolo idempotente, pois nada da requisição era armazenado, e a repetição da requisição trazia sempre o mesmo resultado.

## HTTP/1.0 - Uma evolução bastante desejada

A recepção do HTTP/Web foi extremamente positiva. O ano de 1994 ficou conhecido como "O Ano da Web". Durante os anos seguintes à criação dos padrões da Web, foi criado o World Wide Web Consortium (W3C) para supervisionar o desenvolvimento da Web.

Entre 1991 e 1995, vários recursos começaram a serem testados, em uma abordagem do tipo trial-and-error, onde os recursos eram implementados nos servidores e clientes e a comunidade testava para ver quais desses recursos tinham maior aceitação. Problemas de interoperabilidade eram bastante comuns nessa época.

Em um esforço da W3C juntamente com a Internet Engineering Task Force (IETF), em novembro de 1996 foi criado um documento que descrevia as práticas mais comuns em relação ao HTTP. Esse documento foi conhecido como a RFC 1945 [^4] e definiu o protocolo **HTTP/1.0**

Nessa versão do protocolo, vários novos recursos foram adicionados:

A informação de versão passou a ser enviada com cada requisição GET, assim permitindo a interoperabilidade com o protocolo original, ao passo que permitia os clientes informarem o suporte às extensões adicionadas ao protocolo pela RFC 1945.

Como resposta, o servidor retornava uma linha de resposta que também era versionada, e informava o status daquela resposta.

Também foi adicionado o conceito de cabeçalhos HTTP, tanto para requisições quanto para respostas, permitindo a troca de metadados entre cliente e servidor.

Nessa época, uma requisição típica tinha a seguinte estrutura:

```http
GET /minha-pagina.html HTTP/1.0
User-Agent: NCSA_Mosaic/2.0 (Windows 3.1)
```

E o servidor responderia com uma resposta da seguinte forma:

```http
HTTP/1.0 200 OK
Date: Tue, 15 Nov 1994 08:12:31 GMT
Server: CERN/3.0 libwww/2.17
Content-Type: text/html

<HTML>Uma pagina com uma imagem <IMG SRC="/minha-imagem.gif"></HTML>
```

O cliente, após processar o arquivo HTML, iria abrir uma nova conexão e fazer o mesmo procedimento para baixar a imagem:

```http
GET /minha-imagem.gif HTTP/1.0
User-Agent: NCSA_Mosaic/2.0 (Windows 3.1)
```

E o servidor responderia com uma resposta da seguinte forma:

```http
HTTP/1.0 200 OK
Date: Tue, 15 Nov 1994 08:12:32 GMT
Server: CERN/3.0 libwww/2.17
Content-Type: image/gif

[conteúdo binário da imagem]
```

Basicamente o que o protocolo **HTTP/1.0** trouxe de melhorias foi:

- Códigos de status: 200 OK, 404 Not Found, 500 Internal Server Error
- Cabeçalhos HTTP: Permitindo adicionar metadados para sinalização para o servidor ou para o browser
- Content-Type: Um cabeçalho HTTP que permitia especificar o conteúdo do arquivo.
- Novo verbo - POST: Um verbo que permitia aos browsers enviarem informações para o servidor, que não fosse nos cabeçalhos da requisição.

### Limitações

Nessa fase de expansão dos navegadores, como NCSA Mosaic [^3], Netscape e IE, emergiram limitações claras:

Em especial, a principal limitação do **HTTP/1.0** era a forma como as conexões TCP eram gerenciadas. Ainda tínhamos uma conexão TCP para cada nova requisição que um browser fizesse para o servidor, para buscar os recursos disponíveis em um arquivo html. Inclusive, na própria definição da RFC [^4] é dito que a conexão era fechada após cada requisição respondida pelo servidor.

Outra limitação bastante marcante do **HTTP/1.0** tinha relação com a resolução de nomes de servidores na época, pois existia a possibilidade de várias entradas DNS apontarem para o mesmo endereço IP, mas o servidor não tinha como diferenciar isso.

Por último, e não menos importante, não havia nenhum mecanismo de controle de cache à época, exceto por uma definição de cabeçalho `Expires` da resposta completa, e por conta disso cada vez que uma página (com seu conteúdo relacionado) era solicitada ao servidor, todo o conteúdo era baixado novamente, trazendo ainda mais stress nos servidores que já começavam a sentir os efeitos da disseminação da Web.

É por conta disso que poucos meses após o lançamento do **HTTP/1.0** a IETF lançou uma atualização no protocolo, para atacar exatamente essas limitações identificadas na primeira RFC.

## HTTP/1.1 - O amadurecimento e padronização do protocolo

Em Janeiro de 1997, em resposta aos problemas identificados no protocolo **HTTP/1.0** e as várias tentativas de se criar extensões via cabeçalhos, levou a IETF e a W3C a mudarem o foco de "boas práticas" para a "padronização" do protocolo, culminando na RFC 2068 [^5], conhecida como **HTTP/1.1**.

Considerando o protocolo **HTTP/1.1**, uma requisição típica tinha a seguinte estrutura:

```http
GET /en-US/docs/ HTTP/1.1
Host: developer.mozilla.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:141.0) Gecko/20100101 Firefox/141.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Connection: keep-alive
```

E o servidor responderia da seguinte forma:

```http
HTTP/1.1 200 OK
accept-ranges: none
content-encoding: br
date: Tue, 01 Jul 2025 08:32:50 GMT
expires: Tue, 01 Jul 2025 09:26:50 GMT
cache-control: public, max-age=3600
age: 1926
last-modified: Sat, 28 Jun 2025 00:47:12 GMT
etag: W/"b55394ed2f274eea5d528cf6c91e1dcf"
content-type: text/html
vary: Accept-Encoding
content-length: 26178

[26178 bytes de conteúdo HTML]
```

Como é possível ver nos exemplos acima, temos várias novas funcionalidades disponíveis no protocolo, com o advento da nova versão. O **HTTP/1.1** resolveu algumas das ambiguidades existentes à época do **HTTP/1.0** e também introduziu várias melhorias:

A partir de agora, a conexão TCP pode ser reutilizada entre requisições HTTP. Não é mais necessário abrir múltiplas conexões TCP para recuperar os recursos linkados nas páginas html. Junto com a possibilidade de reutilização da conexão TCP, foi adicionado um recurso de pipeline, que permitia a requisição de outros recursos enquanto um recurso ainda está sendo enviado pelo servidor.

Adicionalmente, também foram adicionados mecanismos de cache mais poderosos, permitindo que o navegador possa indagar o servidor sobre o status de recursos baixados e salvos localmente, sem precisar baixar os recursos novamente. Além do cabeçalho `Expires`, que define um tempo de expiração absoluto, o **HTTP/1.1** passou a usar cabeçalhos como `Cache-Control`, `ETag` e `If-Modified-Since`, permitindo estratégias mais flexíveis de cache e revalidação de recursos.

E não menos importante, foi adicionada uma funcionalidade de Host, que passou a permitir que um mesmo servidor, em um mesmo IP, pudesse responder por diferentes endereços DNS.

Os dois primeiros recursos melhoraram muito a latência no carregamento completo das páginas, que nesse momento começam a ter cada vez mais recursos, como estilos CSS, scripts, imagens e frames (páginas segmentadas compostas de outras páginas). O que passamos a ter é algo parecido com o diagrama TCP abaixo:

```
Cliente                                     Servidor
  | ---- SYN --------------------------------> |
  | <--- SYN+ACK ----------------------------- |
  | ---- ACK --------------------------------> |  (Conexão estabelecida)
  |                                            |
  | ------ "GET /index.html HTTP/1.1" -------> |
  |                                            |
  | <--------- "HTTP/1.1 200 OK" ------------- |  (conteúdo HTML)
  |                                            |
  | ------ "GET /estilo.css HTTP/1.1" -------> |
  | ------ "GET /imagem.gif HTTP/1.1" -------> |
  |                                            |
  | <----- "HTTP/1.1 304 Not Modified" ------- |  (conteúdo css)
  | <--------- "HTTP/1.1 200 OK" ------------- |  (conteúdo gif)
  |                                            |
...
```

É importante falar que tudo isso só é possível por conta da possibilidade de extensão do protocolo, introduzido com o uso de cabeçalhos HTTP. Durante o ciclo de vida do **HTTP/1.1** várias extensões forma propostas, como Autenticação (RFC 7235), Semânticas de Conteúdo (RFC 7231), Downloads Parciais (RFC 7233), entre várias outras.

### Limitações

Mas, a despeito das inovações no **HTTP/1.1**, o protocolo ainda não resolvia vários problemas, e um dos principais adicionados com o pipelining de recursos era a necessidade de se enfileirar as respostas das requisições na mesma ordem, e ao fato de que se houvesse problema na conexão TCP, os recursos na pipeline ficavam esperando a conclusão da transferência. Inclusive esse problema é conhecido na literatura como _"Head-of-line blocking"_ [^6] (HOL), onde há um gargalo de desempenho quando uma fila de pacotes é retida pelo primeiro pacote da fila, mesmo que os outros já pudessem ser processados.

Em teoria, o pipelining permitia enviar múltiplas requisições sem esperar as respostas mas, na prática por causa do HOL e de problemas de implementação em proxies e servidores intermediários, o recurso nunca foi amplamente adotado em navegadores modernos.

Essa característica linerar da transferência do **HTTP/1.1** passa a ser o principal problema do protocolo, e não havia como resolver esse problema através de extensões, pois o problema maior estava na estrutura base do **HTTP/1.1**. Tanto é que os navegadores da época abriam várias conexões com o servidor, mantinham elas abertas e usavam cada conexão para acelerar a transferência, paralelizando a transferência, mas isso tornava bem mais complexo o processo, e não era previsto no protocolo, sem contar que um cliente abrir várias conexões é o principal motivo pelo qual o **HTTP/1.1** foi evoluído do **HTTP/1.0**.

Com esses casos se tornando mais comuns, a IETF definiu um novo Task Group para pensar o novo protocolo que poderia atacar esses problemas, e é nesse cenário que surge o **HTTP/2**, que trouxe mudanças bastante grandes no protocolo.

## HTTP/2 - Um novo protocolo, agora binário

Entre 1997 e 2015 (as datas do lançamento das versões 1.1 e 2 do protocolo HTTP) a Web evoliu bastante, trazendo várias mudanças massivas no ecossistema. Estamos falando de páginas web que deixaram de ser só HTML/CSS para conter scripts javascript, frameworks de layout como JQuery, páginas dinâmicas como PHP, sem contar o início do surgimento dos web services RPC, com SOAP e JSON sendo distribuídos em cima do protocolo HTTP.

Facilmente páginas começaram a possuir dezenas a centenas de recursos a serem carregados, e isso só tornou ainda mais evidente as limitações do **HTTP/1.1** para atender essas demandas sem exaurir os recursos computacionais disponíveis para esses serviços.

### SPDY - A solução do Google para os problemas correntes

É por volta de 2009 que o Google anuncia um protocolo chamado SPDY [^7] cujo objetivo é tentar acelerar o tráfego entre navegadores e servidores web. Nessa época o Google já tinha seu navegador Chrome e por conta disso começou a implementação do protocolo nos seus serviços, que ao serem acessados pelo seu navegador, utilizavam esse protocolo.

Esse protocolo tinha algumas peculiaridades em relação ao **HTTP/1.1**: ele não era mais baseado em texto e sim em formato binário e as transferências de dados entre servidor e cliente usavam uma estrutura de frames de transferência, que permitiam o envio de dados de vários recursos simultaneamente e em qualquer ordem, em um modelo de multiplexação de dados que já estava em estudo pelo W3C HTTP-NG Working Group (HTTPbis).

### A nova solução do HTTPbis

Apesar das vantagens, o protocolo SPDY era um protocolo proprietário do Google, então o HTTP Working Group decidiu em 2012, anunciar a necessidade de um novo padrão de protocolo. Eventualmente o HTTPbis decidiu por derivar o novo protocolo do SPDY e, em maio de 2015 foi apresentado o protocolo **HTTP/2** [^8] para a comunidade. Suas principais características são:

- O protocolo passa a ser um protocolo binário: Em vez de um protocolo baseado em texto. Ele não podia mais ser lido ou criado de forma manual, o que apesar da aparente desvantagem, permitia várias possibilidades de otimização.
- Todos os cabeçalhos passaram a ser enviados em um formato comprimido: Isso permitia a diminuição de informações duplicadas e do overhead dos dados a serem transmitidos.
- O protocolo passa a ser um protocolo multiplexado: Requisições paralelas além de poderem ser feitas na mesma requisição, agora podem ser respondidas em qualquer ordem e permitindo a transferência de todos os recursos concomitantemente, sem a necessidade de se esperar a transferência de um recurso para o início da transferência do próximo

```
+-----------------------------------------------+
|                 Length (24)                   |
+---------------+---------------+---------------+
|   Type (8)    |   Flags (8)   |
+-+-------------+---------------+-------------------------------+
|R|                 Stream Identifier (31)                      |
+=+=============================================================+
|                   Frame Payload (0...)                      ...
+---------------------------------------------------------------+
```

A estrutura de frames claramente trazia uma vantagem na transmissão de dados entre navegador e servidor, por identificar cada fluxo de transferência de forma individualizada, permitindo a reconstituição dos fluxos originais após passar por dentro do TCP, que passa a agir como um túnel para os fluxos estipulados entre os dois agentes.

### Evolução do Protocolo

O **HTTP/2** era uma alternativa ao **HTTP/1.1**, não o substituindo por completo mas permitindo a negociação do modo de transferência de dados entre navegador e servidor. No entanto, o **HTTP/2** teve uma rápida adoção por parte da comunidade [^9] e dos navegadores [^10], alcançando um pico de utilização de 46% dos websites.

Além das melhorias intrínsecas implementadas no novo protocolo, ainda houve espaço posteriormente para novas extensões, já que apesar das mudanças fundamentais no protocolo, ele ainda permitia extensibilidade, e logo começaram a surgir novas funcionalidades:

- Foi adicionado o suporte ao `Alt-Svc`, permitindo a dissociação de recursos como frameworks do conteúdo único fornecido, permitindo uma otimização por parte de Redes de Distribuição de Conteúdo (CDNs)
- Foi adicionado o conceito de Client Hints, que permitiam os navegadores liberarem mais informações sobre seus próprios requisitos de funcionamento para o servidor, que poderia atuar de forma diferenciada de acordo com esses requisitos

### Limitações

Curiosamente, o protocolo **HTTP/2** ainda não era totalmente livre de problemas. Apesar de todas as melhorias feitas no desempenho do protocolo, na forma de transferir dados e nos novos recursos para melhorar a distribuição de conteúdo, o **HTTP/2** ainda era suscetível ao problema original do _"Head-of-line blocking"_, e isso era devido à característica inerente do protocolo TCP, a base para o funcionamento de todas as versões do HTTP até o momento.

O problema é que a despeito do fato de que as transferências de dados entre cliente e servidor já encontravam-se multiplexadas, com possibilidade de transferência simultânea de vários recursos ao mesmo tempo, o canal de transmissão era único.

Por isso, quando ocorria uma interrupção do fluxo do TCP (ou retransmissões e ordenações de datagramas, necessários pelo protocolo), essa interrupção podia causar a pausa de todas as transmissões paralelas, já que aqui ao contrário do caso anterior em que uma pausa na transferência de um recurso travava a transferência de outros recursos, uma pausa na tranferência de um frame pausava a transferência dos outros frames enfileirados no TCP para transmissão, ou seja, o problema apesar de mais raro de acontecer, ainda acontecia.

## HTTP/3 - A revolução do QUIC

O **HTTP/3** representa a maior ruptura da história do protocolo desde a criação do **HTTP/1.1**. Assim como o **HTTP/2** antes dele, o **HTTP/3** não substitui completamente as versões anteriores e mantém as mesmas semânticas já consolidadas nesses protocolos. Ele opera em paralelo, de acordo com a necessidade do navegador.

Como sabemos, o **HTTP/2** introduziu um conceito importante, que é a multiplexação. Mas, mesmo com a multiplexação, o **HTTP/2** ainda continuava a ter o problema intrínseco do _"Head-of-line blocking"_, devido à forma como o protocolo TCP funciona.

Assim, embora o **HTTP/2** tenha resolvido muitos problemas anteriores, esse bloqueio intrínseco do TCP fazia com que, em situações de perda de pacotes ou instabilidade de rede, o desempenho geral ainda fosse prejudicado.

Para resolver esse problema em específico, não havia opção a não ser sair do protocolo TCP. Ele não era desenhado para atender essa situação de várias transferências multiplexadas em um único canal sem apresentar o problema do HOL, e por conta disso o IETF começou a analisar uma solução que o Google tinha desenvolvido anos antes para tratar desse problema, chamada _Quick UDP Internet Connections_ (QUIC).

**Como funciona:**

#### HTTP/2 sobre TCP (ANTES):
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Stream CSS   │ │ Stream JS    │ │ Stream IMG   │ ← multiplexado
├──────────────┤ ├──────────────┤ ├──────────────┤
│                  [TCP ÚNICO]                   │
└────────────────────────────────────────────────┘
```
*pacote perdido = TUDO para*

#### **HTTP/3** sobre QUIC (AGORA):
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Stream CSS   │ │ Stream JS    │ │ Stream IMG   │
├──────────────┤ ├──────────────┤ ├──────────────┤
│  UDP Stream  │ │  UDP Stream  │ │  UDP Stream  │ ← independentes!
└──────────────┘ └──────────────┘ └──────────────┘
```
*Pacote perdido = só uma stream para*

Basicamente, a solução do Google descartava o TCP e passou a usar o UDP, e implementou seus próprios protocolos de tráfego confiável (a exemplo do que o TCP faz), mas focado em permitir independência total entre os fluxos de transferência do navegador com servidor, e vice-versa.

O protocolo funcionava tão bem que a especificação foi submetida como Draft para o IETF [^13], que a própria Task Force publicou, em 2020, a RFC 9000 [^14] que cobria esse novo protocolo de transporte e, em 2022, a padronizou o **HTTP/3** como "HTTP over QUIC", através da RFC 9114 [^15].

### Melhorias do HTTP/3

O **HTTP/3** trouxe avanços fundamentais em relação aos protocolos anteriores, a saber:

- Fim do HOL no nível da camada de transporte, com a implementação de um novo protocolo de transporte confiável em cima do UDP
- Fim dos handshakes de três estágios do TCP, aumentando a responsividade das conexões
- Migração de redes e handovers sem perda efetiva de conexões (como acontece com o TCP)

Hoje o **HTTP/3** é o principal protocolo da World Wide Web, e atende a todas as exigências para funcionamento tanto de páginas web estáticas quanto dinâmicas e ainda coisas como Web Services, hoje usando tecnologias como RESTful e HATEOAS.

Além das vantagens técnicas, o protocolo hoje têm um alcance bastante alto e suporte pela grande maioria dos navegadores modernos [^16] e [^17].

## HTTPS: A Camada Invisível de Criptografia

Falamos de HTTP o tempo todo mas não mencionamos **HTTPS** ou criptografia. Por quê? Simples: o HTTPS era só uma camada extra de proteção sobre o HTTP. No fundo, o HTTP ainda funcionava exatamente igual por trás do fluxo criptografado.

### **HTTPS = HTTP + TLS (camada externa)**

```
Navegador → [Criptografia TLS] → HTTP → Servidor
```

Mesmo em HTTPS, você ainda enviava:
```
GET / HTTP/1.1
Host: vndmtrx.github.io
```

**Não abordamos HTTPS** porque:
- HTTP evoluiu independente do TLS
- HTTPS nunca mudou semântica do HTTP (GET/POST/cabeçalhos)
- Era só "HTTP tunelado em TLS"

A única mudança real veio no **HTTP/3**, onde **TLS 1.3** passa a ser integrado ao QUIC:

- **HTTP/1.1** + TLS = 4 handshakes (3 TCP + 1 TLS)
- **HTTP/2** + TLS   = 2 handshakes (1 TCP + 1 TLS)
- **HTTP/3** + QUIC  = 1 handshake (TLS embutido)

No futuro devo fazer um post só sobre TLS, para complementar esse post.

## Conclusão: Da Simplicidade à Escala Global

A evolução do HTTP reflete a maturidade da Web: de um protocolo simples para troca de documentos científicos em 1991, para uma infraestrutura multiplexada e resiliente sobre QUIC no HTTP/3, capaz de suportar apps dinâmicos, streaming e APIs em escala. Cada versão resolveu gargalos anteriores (de conexões persistentes no 1.1 a multiplexação no 2 e independência de streams no 3), mas manteve a compatibilidade semântica, garantindo transição suave.

Muito dessa informação você pode encontrar em sites como a Wikipédia [^18] como no Mozila MDN [^11] e em todas as referências espalhadas ao longo desse post.

## Referências

[^1]: **Primeiro site da Web** (*CERN*) ([https://info.cern.ch/](https://info.cern.ch/)))

[^2]: **Anúncio público da WWW** (*Tim Berners-Lee, 1991*) ([https://www.w3.org/People/Berners-Lee/1991/08/art-6484.txt](https://www.w3.org/People/Berners-Lee/1991/08/art-6484.txt))

[^3]: **NCSA Mosaic** (*história do primeiro browser popular*) ([https://web.archive.org/web/20070702183017/http://www.livinginternet.com/w/wi_mosaic.htm](https://web.archive.org/web/20070702183017/http://www.livinginternet.com/w/wi_mosaic.htm))

[^4]: **RFC 1945: HTTP/1.0** (*IETF, 1996*) ([https://datatracker.ietf.org/doc/rfc1945](https://datatracker.ietf.org/doc/rfc1945))

[^5]: **RFC 2068: HTTP/1.1** (*IETF, 1997*) ([https://datatracker.ietf.org/doc/rfc2068](https://datatracker.ietf.org/doc/rfc2068))

[^6]: **Head-of-line blocking** (*Mozilla Developer Network*) ([https://developer.mozilla.org/en-US/docs/Glossary/Head_of_line_blocking](https://developer.mozilla.org/en-US/docs/Glossary/Head_of_line_blocking))

[^7]: **SPDY Whitepaper** (*Chromium/Google*) ([https://www.chromium.org/spdy/spdy-whitepaper/](https://www.chromium.org/spdy/spdy-whitepaper/))

[^8]: **RFC 7540: HTTP/2** (*IETF, 2015*) ([https://datatracker.ietf.org/doc/rfc7540](https://datatracker.ietf.org/doc/rfc7540))

[^9]: **Uso de HTTP/2** (*estatísticas W3Techs*) ([https://w3techs.com/technologies/details/ce-http2](https://w3techs.com/technologies/details/ce-http2))

[^10]: **Suporte a HTTP/2** (*CanIUse*) ([https://caniuse.com/http2](https://caniuse.com/http2))

[^11]: **Evolution of HTTP** (*Mozilla Developer Network*) ([https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Evolution_of_HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Evolution_of_HTTP))

[^12]: **Short history of the Web** (*CERN*) ([https://home.cern/science/computing/birth-web/short-history-web](https://home.cern/science/computing/birth-web/short-history-web))

[^13]: **Draft QUIC-HTTP2 mapping** (*IETF*) ([https://datatracker.ietf.org/doc/html/draft-shade-quic-http2-mapping](https://datatracker.ietf.org/doc/html/draft-shade-quic-http2-mapping))

[^14]: **RFC 9000: QUIC** (*IETF, 2021*) ([https://datatracker.ietf.org/doc/rfc9000](https://datatracker.ietf.org/doc/rfc9000))

[^15]: **RFC 9114: HTTP/3** (*IETF, 2022*) ([https://datatracker.ietf.org/doc/rfc9114](https://datatracker.ietf.org/doc/rfc9114))

[^16]: **Uso de HTTP/3** (*W3Techs*) ([https://w3techs.com/technologies/details/ce-http3](https://w3techs.com/technologies/details/ce-http3))

[^17]: **Suporte a HTTP/3** (*CanIUse*) ([https://caniuse.com/http3](https://caniuse.com/http3))

[^18]: **HTTP** (*Wikipedia, visão geral*) ([https://en.wikipedia.org/wiki/HTTP](https://en.wikipedia.org/wiki/HTTP))
