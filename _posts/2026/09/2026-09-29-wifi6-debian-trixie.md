---
layout: post
title: "Hotspot Wi-Fi 6 no Debian: Domando o Firmware Intel"
subtitle: "Como contornar as travas LAR e NO-IR para rodar um AP 802.11ax com WPA3 e nftables"
author:
  - "Eduardo N. S. R."
date: 2026-09-29 10:38:00 GMT-3
permalink: /posts/wifi6-debian-trixie/
category: Artigos
tags: [Debian, Linux, Wi-Fi 6, hostapd, nftables]
math: true
---

Existe uma ilusão vendida pelas interfaces gráficas modernas de que transformar o computador em ponto de acesso sem fio é um clique e pronto. Você abre o painel da distribuição, clica em "Criar Hotspot", inventa uma senha qualquer e espera que funcione. Na melhor das hipóteses, sobe uma rede WPA2 capenga; na pior, a interface congela, o NetworkManager se perde sozinho e você não faz ideia do que deu errado.

Para quem só quer conectar o celular ou o notebook com um mínimo de controle e desempenho, essa automação de desktop mais atrapalha do que ajuda.

A minha dúvida era bem prática: tenho um computador rodando Debian Trixie, conectado no cabo de rede e com uma placa Intel Wi-Fi 6E AX211 sobrando ali. *Será que consigo transformar essa placa num Access Point moderno pra atender meus dispositivos móveis?* A ideia era montar algo enxuto: Wi-Fi 6 (802.11ax), WPA3-Personal puro (SAE) e regras simples de `nftables`, sem mágica de interface gráfica.

A resposta curta é sim, dá pra fazer. A resposta longa é que o processo virou uma caça aos motivos de o rádio simplesmente se recusar a emitir sinal, esbarrando em microcódigo da Intel, travas regulatórias e mensagens crípticas no `dmesg`.

<details class="toc-box" markdown="1">
  <summary><strong>Sumário & Índice de Seções (TOC)</strong></summary>
* TOC
{:toc}
</details>

## O ponto de partida: o hardware da máquina

Antes de sair chutando parâmetros de rádio no escuro, o jeito mais prático é olhar o que realmente está espetado na máquina. Tentar adivinhar configuração sem saber qual driver ou firmware está no comando é o caminho mais rápido pra perder horas sem sair do lugar.

A máquina onde fiz os testes é um desktop rodando Debian Trixie. As peças do quebra-cabeça:

| Componente | Especificação |
| :--- | :--- |
| **Sistema Operacional** | Debian GNU/Linux 13 (Trixie) |
| **Kernel** | `Linux 6.12` (Debian amd64) |
| **Placa Wi-Fi** | Intel Wi-Fi 6E AX211 160MHz (arquitetura CNVi) |
| **Driver / Módulos** | `iwlwifi` + `iwlmvm` |
| **Firmware Carregado** | `so-a0-gf-a0-89.ucode` |
| **Interface Sem Fio** | `wlp0s20f3` (Hostapd / AP) |
| **Interface Uplink** | `enp0s31f6` (Cabo Ethernet Gigabit) |
| **Softwares** | `hostapd 2.10`, `nftables 1.1.3`, `dnsmasq` |

O detalhe fundamental dessa tabela é o controlador Intel AX211 com arquitetura CNVi (*Connectivity Interface*). Diferente de adaptadores PCIe tradicionais onde o processador e o rádio moram na mesma plaquinha dedicada, no modelo CNVi a Intel resolveu dividir o casamento: o cérebro lógico do Wi-Fi fica soldado dentro do chipset da placa-mãe (PCH), enquanto o slot M.2 abriga só os transceptores analógicos de radiofrequência (CRF).

Essa intimidade profunda entre a placa-mãe e o rádio significa uma coisa bem simples: você não manda em quase nada. O microcódigo da Intel tem rédea curta sobre o que o hardware pode ou não fazer, e ele não aceita desaforo do sistema operacional.

## A ideia: separando as peças sem depender do desktop

A tentação mais comum ao criar um hotspot no Linux é deixar o NetworkManager cuidar de tudo: ele cria uma ponte virtual, sobe um `dnsmasq` temporário onde bem entender e joga um punhado de regras legadas de `iptables`.

O problema é que o NetworkManager se comporta igual àquele estagiário excessivamente proativo: você não pediu nada, mas ele vê uma interface dando sopa, assume o controle sem avisar, tenta adivinhar o que você quer e, no primeiro sinal de instabilidade, reseta o link ou decide unilateralmente que a interface virou "não gerenciável". Pra um AP que você só quer deixar quieto funcionando no canto, essa boa vontade é a receita perfeita pra dor de cabeça.

Em vez de brigar com o desktop, a saída foi chutar o NetworkManager pra longe e separar as responsabilidades em camadas simples:

```text
┌────────────────────────────────────────────────────────┐
│               PILHA DE SOFTWARE PURA (AP)              │
│                                                        │
│  [NetworkManager]  ──> Isolar interface (unmanaged)    │
│         │                                              │
│  [ifupdown / L3]   ──> Fixar IP estático no boot       │
│         │              (/etc/network/interfaces)       │
│  [dnsmasq / L7]    ──> Subir DHCP e DNS exclusivo      │
│         │              (Sub-rede 192.168.100.0/24)     │
│  [hostapd / L1-L2] ──> Subir rádio 802.11ax + WPA3     │
│         │              (Canal 13, SAE puro, CCMP)      │
│  [nftables / L3-L4]──> Forwarding e NAT Masquerade     │
│                        (Regras atômicas sem iptables)  │
└────────────────────────────────────────────────────────┘
```

Cada peça tem uma função direta:

1. **Camada L3 Estática (`ifupdown`):** Assume a interface `wlp0s20f3`, garantindo um IP fixo logo no boot sem interferência de applets de desktop.
2. **Camada de Suporte L7 (`dnsmasq`):** Entrega DHCP rápido e DNS na sub-rede sem fio, escutando estritamente nessa interface.
3. **Camada de Rádio L1/L2 (`hostapd`):** Controla a sinalização do rádio 802.11ax, os beacons e o *handshake* criptográfico em WPA3-Personal (SAE) via Netlink (`nl80211`).
4. **Camada de Encaminhamento L3/L4 (`nftables`):** Faz a filtragem de estados via `conntrack` e aplica o NAT Masquerade em direção à placa cabeada `enp0s31f6`.

Na teoria, era só subir os serviços e conectar. Na prática, o rádio tinha outros planos.

## O primeiro tropeço: por que o rádio se recusa a emitir

Com os arquivos rascunhados, iniciei os serviços pro primeiro teste. O comando `sudo systemctl start hostapd` rodou de primeira e o status parecia animador:

```text
● hostapd.service - Access point and authentication server for Wi-Fi and Ethernet
     Loaded: loaded (/usr/lib/systemd/system/hostapd.service; enabled; preset: enabled)
     Active: active (running) since Sun 2026-09-28 10:15:22 -03; 4s ago
...
Sep 28 10:15:22 debian hostapd[14205]: wlp0s20f3: interface state UNINITIALIZED->COUNTRY_UPDATE
Sep 28 10:15:22 debian hostapd[14205]: wlp0s20f3: interface state COUNTRY_UPDATE->ENABLED
Sep 28 10:15:22 debian hostapd[14205]: wlp0s20f3: AP-ENABLED
```

O `hostapd` reportava com todas as letras: `AP-ENABLED`. Na teoria, o ponto de acesso estava no ar e transmitindo.

Peguei o celular, abri o painel de redes sem fio e nada. O SSID não aparecia na lista de varredura. Esperei alguns minutos, forcei novas buscas e nada mudou. Não havia sinal sendo emitido.

Fui ao terminal investigar o estado da interface com o utilitário `ip`:

```bash
ip addr show wlp0s20f3
```

O resultado expôs a contradição:

```text
3: wlp0s20f3: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 02:00:00:00:00:01 brd ff:ff:ff:ff:ff:ff
    inet 192.168.100.1/24 brd 192.168.100.255 scope global wlp0s20f3
       valid_lft forever preferred_lft forever
```

Como é possível o `hostapd` indicar que o ponto de acesso está habilitado (`AP-ENABLED`) enquanto o kernel Linux classifica o link como `state DOWN` e com a flag `NO-CARRIER` ativa?

### O paradoxo do AP-ENABLED com interface em state DOWN

Essa discrepância entre o que o software jura que está fazendo e o que o hardware realmente entrega é a clássica divisão de mundos do Linux: o espaço de usuário (*userspace*) vive de otimismo; o kernel vive da realidade física do silício.

O `hostapd` opera em *userspace*. Para conversar com os adaptadores modernos, ele conversa via Netlink usando a família `nl80211` [^1]. Quando o serviço sobe, ele despacha mensagens pedindo a criação do BSSID lógico, aloca as estruturas em memória e avisa ao subsistema `cfg80211` que o AP está autorizado a rodar. Na cabeça do `hostapd`, o dever foi cumprido: tá autorizado, logo `AP-ENABLED`.

Só que o kernel Linux não cai em papo furado. Uma interface de rede só abandona a flag `NO-CARRIER` e atinge o estado `state UP` quando o rádio físico reporta que a portadora está ligada de verdade (`LOWER_UP`). No cabo de rede, é quando o conector detecta tensão elétrica no cobre. No Wi-Fi, é quando o chip efetivamente liga o transmissor, sintoniza a frequência e joga os primeiros *beacons* 802.11 no ar.

Se o `hostapd` comemora que o AP subiu, mas a interface continua em `NO-CARRIER` no kernel, a constatação é límpida (depois de perder um belo par de horas quebrando a cabeça): o microcódigo da Intel simplesmente puxou o freio de mão e se recusou a transmitir um mísero watt de sinal.

### A armadilha do Location Aware Regulatory e o perfil country 00

Ao investigar por que a interface teimava em não emitir sinal no início dos testes, executei o comando de auditoria regulatória do subsistema sem fio:

```bash
sudo iw reg get
```

A saída foi esclarecedora:

```text
global
country BR: DFS-FCC
    (2400 - 2483 @ 40), (N/A, 30), (N/A)
    (5150 - 5250 @ 80), (N/A, 27), (N/A), NO-OUTDOOR, AUTO-BW
    (5250 - 5350 @ 80), (N/A, 27), (0 ms), NO-OUTDOOR, DFS, AUTO-BW
    (5470 - 5725 @ 160), (N/A, 27), (0 ms), DFS, AUTO-BW
    (5725 - 5850 @ 80), (N/A, 30), (N/A), AUTO-BW
    (5925 - 7125 @ 320), (N/A, 12), (N/A), NO-OUTDOOR

phy#0 (self-managed)
country 00: DFS-UNSET
    (2402 - 2437 @ 40), (6, 22), (N/A), AUTO-BW, NO-HT40MINUS, NO-80MHZ, NO-160MHZ
    (2422 - 2462 @ 40), (6, 22), (N/A), AUTO-BW, NO-80MHZ, NO-160MHZ
    (2447 - 2482 @ 40), (6, 22), (N/A), AUTO-BW, NO-HT40PLUS, NO-80MHZ, NO-160MHZ
    (5170 - 5190 @ 160), (6, 22), (N/A), NO-OUTDOOR, AUTO-BW, IR-CONCURRENT, NO-HT40MINUS, NO-320MHZ, PASSIVE-SCAN
    (5735 - 5755 @ 160), (6, 22), (N/A), AUTO-BW, IR-CONCURRENT, NO-HT40MINUS, NO-320MHZ, PASSIVE-SCAN
```

Observe a divergência entre as duas seções da saída:

1. A seção `global` informa `country BR`, refletindo o banco de dados regulatório que o sistema operacional tentou carregar (`wireless-regdb`).
2. A seção física `phy#0` exibe a indicação `self-managed`, vinculada ao código universal `country 00: DFS-UNSET`.

Essa distinção explica uma dúvida muito comum: *por que executar `sudo iw reg set BR` altera o `global`, mas não surte efeito nenhum na placa `phy#0`?*

No subsistema sem fio do Linux (`cfg80211`), os adaptadores dividem-se em duas categorias:
* **Placas gerenciadas pelo kernel:** Em chipsets abertos como MediaTek (`mt7921e`) ou Atheros (`ath9k`), o driver repassa a autoridade regulatória diretamente para o kernel. Quando você roda `iw reg set BR`, o sistema atualiza as frequências e potências da interface física quase de imediato.
* **Placas com domínio auto-gerenciado (`self-managed`):** Os adaptadores da Intel possuem a flag interna `WIPHY_FLAG_CUSTOM_REGULATORY`. Ao carregar o módulo `iwlwifi` [^3], a placa avisa ao kernel que ela mesma manda nas próprias regras a partir de tabelas gravadas na memória OTP (*One-Time Programmable*) durante a fabricação. O microcódigo simplesmente ignora os seus palpites.

E quando há conflito entre o que o sistema operacional quer e o que a placa física declara, a regra do kernel é implacável: a restrição mais severa sempre vence. Se o sistema operacional autoriza canais abertos e potência alta no Brasil, mas a tabela gravada no silício da placa (`phy#0`) bate o pé dizendo que o canal é restrito ou passivo, não tem conversa: o hardware vence e o kernel senta e chora.

Para coroar a burocracia, os adaptadores Intel vêm equipados com o famigerado LAR (*Location Aware Regulatory*) [^4].

O LAR foi desenhado sob a premissa de mobilidade em notebooks: a placa escuta os roteadores ao redor para descobrir se você pousou em Guarulhos ou em Frankfurt antes de emitir rádio. Só tem um pequeno detalhe: o meu computador não sai da minha mesa e passa a maior parte da sua vida espetado na tomada da parede e ligado no cabo de rede. Não tem a menor chance de esse gabinete acordar subitamente na Baviera. Mas a Intel insiste em tratá-lo como se fosse um ultrabook passeando no saguão de um aeroporto internacional.

A lógica do LAR funciona em três passos:
1. Para descobrir em que canto do planeta está operando, a placa precisa conectar-se como cliente (STA) a algum ponto de acesso ou escutar passivamente anúncios periódicos de quadros 802.11d com o código do país (*Country IE*).
2. Se múltiplos roteadores vizinhos confirmarem que estão no Brasil, o próprio microcódigo da Intel valida o consenso e atualiza a tabela da placa para `BR`.
3. Mas quando tentamos usar a placa puramente como ponto de acesso autônomo (Master/AP), ela não se conecta a ninguém para herdar essa validação geográfica.

Resultado: sem o consenso de outros rádios vizinhos, a placa assume a paranoia máxima e recua para o perfil mundial de contingência: o `country 00`.

E o que dita o perfil `country 00`?
* **Faixa de 5 GHz e 6 GHz:** recebe as diretivas mandatórias `PASSIVE-SCAN` e `NO-IR` (*No Initiate Radiation*), proibindo categoricamente qualquer emissão de beacons como AP.
* **Faixa de 2.4 GHz:** a transmissão é autorizada de 2402 a 2482 MHz, mas com uma trava explícita: `NO-HT40PLUS` na faixa superior (canais agregados de 40 MHz para cima são sumariamente vetados).

Somado a isso, o NetworkManager rodando em paralelo vivia tentando assumir o controle da interface, forçando-a para baixo toda vez que o `hostapd` inicializava. Para isolar as variáveis e estabelecer um ponto de partida limpo e estável, o primeiro passo foi blindar a interface contra o NetworkManager e configurar o rádio no canal canônico mais seguro da literatura: o canal 6 (`channel=6`), com largura fixa de 20 MHz.

### A evidência no dmesg: os erros de microcódigo do firmware Intel

Durante a bateria de testes com o módulo AX211, experimentei combinações mais agressivas de parâmetros High Efficiency (HE) e canais de 40 MHz em frequências limítrofes.

A resposta do hardware foi imediata. Ao consultar o buffer de mensagens do kernel com `dmesg -T`, encontrei o registro de reinício do microcódigo:

```text
[Sun Sep 28 10:22:09 2026] iwlwifi 0000:00:14.3: Microcode SW error detected. Restarting 0x0.
[Sun Sep 28 10:22:09 2026] iwlwifi 0000:00:14.3: Loaded firmware version: 89.4d42c933.0 so-a0-gf-a0-89.ucode
[Sun Sep 28 10:22:09 2026] iwlwifi 0000:00:14.3: 0x00000084 | ADVANCED_SYSASSERT
```

O microcódigo `so-a0-gf-a0-89.ucode`, rodando no microcontrolador dedicado do AX211, encontrou uma combinação de parâmetros pedida pelo driver `iwlmvm` que violava as tabelas rígidas da sua memória.

Em vez de devolver um erro civilizado para o kernel, o firmware entrou em pânico (`ADVANCED_SYSASSERT`) e puxou a tomada do próprio chip (`Restarting 0x0`). O driver do Linux teve que recarregar o arquivo `.ucode` do zero, derrubando a interface e desconectando tudo no susto.

O recado da Intel foi direto e sem meias palavras: ou você joga pelas regras estritas do microcódigo, ou a placa vai reiniciar na sua cara toda vez que você tentar inventar moda.

### A tentação do 5 GHz na faixa UNII-3 e o veto definitivo de silício

Durante a auditoria aprofundada das tabelas de radiofrequência com `iw phy phy0 info`, uma descoberta parecia abrir uma brecha tentadora no bloqueio da Intel.

Embora toda a faixa baixa de 5 GHz (canais 36 a 144) estivesse carimbada com `no IR`, os canais altos da faixa UNII-3 (canais 149 a 165, de 5745 a 5825 MHz) exibiam uma condição diferente:

```text
Frequencies:
    * 5745.0 MHz [149] (22.0 dBm)
    * 5765.0 MHz [153] (22.0 dBm)
    * 5785.0 MHz [157] (22.0 dBm)
    * 5805.0 MHz [161] (22.0 dBm)
    * 5825.0 MHz [165] (22.0 dBm)
```

No Brasil, sob regulamentação da Anatel e em conformidade com as regras da FCC, a faixa UNII-3 não divide frequências com radares meteorológicos (dispensando o complexo mecanismo DFS) e autoriza emissão de maior potência. Como a placa havia escutado passivamente o ambiente e herdado temporariamente o código geográfico `country BR: DFS-UNSET`, a flag restritiva de `no IR` parecia ter desaparecido desses cinco canais.

A ideia era tentadora: por que me contentar com os 286 Mbps da faixa de 2.4 GHz se dava pra tentar o canal 149 com canais agregados de 80 MHz (`vht_oper_chwidth=1`, `he_oper_chwidth=1`) e buscar taxas bem mais altas no Wi-Fi 6?

Ajustei o `hostapd.conf` para operar em 5 GHz no canal 149 e reiniciei o daemon. O log de depuração (`hostapd -d`) mostrou exatamente onde o microcódigo barra a operação:

```text
wlp0s20f3: interface state UNINITIALIZED->COUNTRY_UPDATE
Previous country code BR, new country code BR 
nl80211: Regulatory information - country=00
...
nl80211: 5735-5755 @ 160 MHz 22 mBm (no IR)
Frequency 5745 (primary) not allowed for AP mode, flags: 0x20053 NO-IR
Primary frequency not allowed
wlp0s20f3: IEEE 802.11 Hardware does not support configured channel
Could not select hw_mode and channel. (-3)
wlp0s20f3: AP-DISABLED 
```

O log expõe com exatidão onde o firmware da Intel puxa o freio de mão:

1. **A ilusão da escuta passiva:** Enquanto a placa atua apenas escutando o ar em silêncio (*scan passivo*), o firmware tolera a indicação de `country BR`. Dá a falsa impressão de que a frequência alta está pronta pra uso.
2. **O bloqueio ao ligar a transmissão:** No milissegundo em que o `hostapd` tenta colocar a interface em modo Master e ligar o transmissor em 5 GHz, a memória de fábrica do chip (OTP) assume o controle. O microcódigo ignora solenemente a instrução do sistema operacional e força o perfil mundial de contingência (`country=00`).
3. **O recuo forçado:** Sob `country=00`, o canal 149 recebe a trava `0x20053 NO-IR` (proibido iniciar transmissão). O subsistema `cfg80211` do kernel acata a ordem do silício, recusa a operação e derruba a interface para `AP-DISABLED`.

O motivo dessa sabotagem é uma mistura de regulação e contenção de custos [^7]. Os adaptadores AX201 e AX211 foram homologados internacionalmente apenas como dispositivos clientes (estações móveis). Testar e certificar um transmissor para operar como ponto de acesso autônomo (Master AP) em 5 GHz e 6 GHz exige processos de homologação caríssimos e baterias de testes de conformidade de radar (DFS) que a Intel não quis pagar para placas de desktop/laptop. Para blindar os seus próprios advogados contra multas de órgãos reguladores mundo afora, a fabricante trancou o microcódigo no silício: você comprou o hardware, mas quem decide onde ele pode transmitir são os advogados da Intel.

Se o seu objetivo de vida for montar um roteador Linux moderno operando em 5 GHz ou 6 GHz a 1.200 Mbps ou 2.400 Mbps, esqueça a Intel. A saída definitiva no mundo open source é trocar o módulo M.2 por chipsets MediaTek [^8] (como o MT7921 ou MT7922). A MediaTek adotou a postura elegante de manter drivers 100% livres no kernel (`mt7921e`), sem essa palhaçada de LAR e autorizando operação Master plena em 5 GHz.

No ecossistema Intel AX, contudo, a realidade é essa: o canal de 2.4 GHz em 20 MHz é o único refúgio seguro onde o microcódigo nos deixa brincar em paz.

### A falácia do atualizar o kernel resolve tudo

Em fóruns e discussões na internet, a resposta automática para qualquer problema envolvendo drivers Wi-Fi no Linux é o clichê habitual: "compila o kernel 6.13, 6.14 ou espera o Linux 7.x nos backports que resolve".

Essa recomendação ignora a fronteira física do problema:

1. **O que não muda com kernels novos:** A trava regulatória do LAR e as restrições `NO-IR` em 5 GHz/6 GHz para modo AP residem no firmware e na memória OTP gravada no silício pela Intel. Nenhum kernel, por mais recente que seja, tem o poder de sobrepor essa verificação sem que você adulterasse o código do driver e recompilasse o microcódigo fechado da Intel.
2. **O que muda de verdade com kernels novos:** A evolução da árvore principal do kernel traz melhorias reais na sincronização de filas de transmissão concorrentes (`txqs`), redução de *race conditions* no driver `iwlwifi` quando múltiplos dispositivos comunicam-se via Wi-Fi 6 e suporte a revisões mais recentes da API de firmware (como as transições da API 80 para a 89 e 90).

No nosso caso, o kernel Debian padrão (Linux 6.12) com o firmware da série 89 provou-se totalmente estável, contanto que as restrições do rádio fossem respeitadas na camada de configuração.

## A pilha de produção: configuração limpa e determinística

Com a causa raiz compreendida e os limites do hardware devidamente mapeados, passamos à implementação da pilha de produção. Cada componente foi configurado de forma declarativa e com inicialização gerenciada pelo `systemd`.

### Isolamento e endereçamento estático no ifupdown

Para que o `hostapd` assuma a interface sem que o NetworkManager tente desconectá-la ou atribuir endereços via DHCP de terceiros, declaramos o dispositivo diretamente no `/etc/network/interfaces`.

No Debian, o NetworkManager respeita por padrão os dispositivos configurados no `ifupdown` e os coloca em modo não gerenciado (*unmanaged*):

```ini
# /etc/network/interfaces
auto wlp0s20f3
iface wlp0s20f3 inet static
    address 192.168.100.1
    netmask 255.255.255.0
```
*Configuração estática da camada L3 para o adaptador sem fio.*

Para fechar qualquer brecha onde o NetworkManager pudesse recapturar a interface após um reinício de sessão gráfica ou atualização de pacote, adicionamos uma regra de blindagem explícita no `/etc/NetworkManager/conf.d/99-unmanaged.conf`:

```ini
# /etc/NetworkManager/conf.d/99-unmanaged.conf
[keyfile]
unmanaged-devices=interface-name:wlp0s20f3
```
*Blindagem definitiva para impedir qualquer interferência de daemons de desktop.*

Essa configuração combinada garante que, durante a fase de inicialização da rede (`networking.service`), a interface `wlp0s20f3` receba imediatamente o endereço de gateway `192.168.100.1/24`, ficando totalmente invisível para os applets de bandeja do desktop.

### Serviços de suporte: DHCP e DNS com dnsmasq

Para distribuir endereços e resolver nomes com agilidade, o `dnsmasq` [^6] continua imbatível: consome meia dúzia de megabytes de RAM e responde quase instantaneamente.

O arquivo `/etc/dnsmasq.conf` foi moldado para isolar o serviço estritamente na interface sem fio, sem vazar requisições para a rede cabeada (`enp0s31f6`):

```ini
# /etc/dnsmasq.conf
interface=wlp0s20f3
listen-address=192.168.100.1
bind-dynamic
dhcp-range=192.168.100.10,192.168.100.100,255.255.255.0,12h
dhcp-option=option:dns-server,1.1.1.1,8.8.8.8
```
*Configuração do dnsmasq com amarração dinâmica na interface sem fio.*

O parâmetro `bind-dynamic` aqui é o segredo: diferente do rígido `bind-interfaces`, ele permite que o `dnsmasq` aguarde e se vincule à interface assim que ela receber o IP estático, sem capotar o serviço com erro de socket se o daemon subir alguns milissegundos antes da rede durante o boot.

### A camada de rádio: hostapd com Wi-Fi 6 e WPA3 puro

Esta é a peça central do quebra-cabeça. O `/etc/hostapd/hostapd.conf` reúne as diretivas de rádio para operar em 2.4 GHz contornando o LAR da Intel, mas ativando os recursos do padrão 802.11ax (Wi-Fi 6) [^5] e a segurança do WPA3-Personal puro (SAE):

```ini
# /etc/hostapd/hostapd.conf
interface=wlp0s20f3
driver=nl80211
ssid=Debian-Hotspot-AX

# Domínio regulatório e governança de RF
country_code=BR
ieee80211d=1

# Socket UNIX para gerência e telemetria com hostapd_cli
ctrl_interface=/run/hostapd
ctrl_interface_group=0

# Banda e Canal (2.4 GHz - Canal 13 fora do engarrafamento)
hw_mode=g
channel=13

# Otimização física: Preâmbulo Curto (96 µs vs 192 µs)
preamble=1

# Criptografia WPA3-Personal Puro (SAE) e blindagem contra timing attacks
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=2
wpa_passphrase=SuaSenhaForteAqui

# QoS e alicerce do Wi-Fi 4 (WMM obrigatório para HT/HE)
wmm_enabled=1
ieee80211n=1
ht_capab=[SHORT-GI-20][TX-STBC][RX-STBC1]

# Wi-Fi 6 (802.11ax - High Efficiency)
ieee80211ax=1
he_su_beamformer=1
he_su_beamformee=1
he_oper_chwidth=0

dtim_period=2
```
*Arquivo hostapd.conf afinado no canal 13 com WPA3-SAE, extensões 802.11ax e preâmbulo curto.*

Para entender o que cada uma dessas diretivas está orquestrando no rádio:

* **Identificação da interface e sinalização (`interface`, `driver`, `ssid`, `country_code`, `ieee80211d`):**
  * `interface=wlp0s20f3`: O nome do adaptador físico gerado pelo systemd com base no barramento PCIe/CNVi.
  * `driver=nl80211`: A interface Netlink moderna do Linux. Esqueça drivers legados como `wext`: o `nl80211` é a única pilha que conversa nativamente com as extensões 802.11n, ac e ax.
  * `country_code=BR` e `ieee80211d=1`: Injeta nos beacons periódicos o código do Brasil. Isso avisa aos clientes conectados em que país estão operando, alinhando as potências de transmissão às normas locais.
  * `ssid=Debian-Hotspot-AX`: O nome da rede que vai aparecer nos dispositivos.

* **Socket de controle local (`ctrl_interface`, `ctrl_interface_group`):**
  * `ctrl_interface=/run/hostapd`: Cria o socket UNIX para que utilitários como o `hostapd_cli` consultem métricas de sinal, modulação e estados de associação em tempo real sem precisar reiniciar o serviço.
  * `ctrl_interface_group=0`: Restringe o socket ao `root` para que nenhum processo não autorizado invente de mexer no rádio.

* **Banda, canal deserto e corte de overhead (`hw_mode`, `channel`, `preamble`):**
  * `hw_mode=g`: Define a operação na faixa de 2.4 GHz. Mesmo operando em Wi-Fi 6, o `hostapd` exige o modo base `g` para montar o mapa inicial de frequências antes de injetar as extensões modernas.
  * `channel=13`: Frequência central de 2472 MHz em 20 MHz de largura. No perfil `country 00`, a faixa alta de 2.4 GHz não possui a trava `NO-IR`. Enquanto os canais 1, 6 e 11 viviam engarrafados pelos vizinhos, o canal 13 revelou-se um refúgio totalmente limpo.
  * `preamble=1`: Força o preâmbulo curto na camada física (PLCP). O preâmbulo longo herdado do 802.11b consome 192 µs de sinalização a cada pacote; ao cortar para 96 µs, sobra mais tempo útil de ar (*airtime*) para transferir dados de verdade.

> [!WARNING]
> **O dogma do canal 13 (ou: Anatel, por favor não me processe):**
> Qualquer manual clássico de redes sem fio vai repetir como um mantra que você *só deve usar os canais 1, 6 e 11* em 2.4 GHz. Os motivos para esse pânico são bem conhecidos: primeiro, nos Estados Unidos a FCC proíbe ou limita severamente o canal 13, o que faz aparelhos importados de lá (ou configurados com código de país americano) ficarem completamente cegos sem enxergar o seu SSID; segundo, o canal 13 sobrepõe-se parcialmente ao canal 11, gerando interferência de canal adjacente em vez da contenção ordenada de mesmo canal. Mas no Brasil (sob regulação da Anatel) e na Europa, o canal 13 é perfeitamente legal e homologado. Diante de um ambiente com dezenas de roteadores se esmurrando nos canais 1, 6 e 11, e sabendo que meus aparelhos pessoais suportam o canal 13 com folga, explorar esse refúgio deserto foi a melhor decisão prática possível: saímos de um congestionamento infernal para uma pista totalmente livre.

* **WPA3-Personal puro e blindagem de enlace (`wpa`, `wpa_key_mgmt`, `rsn_pairwise`, `ieee80211w`, `sae_pwe`):**
  * `wpa_key_mgmt=SAE`: Ativa o *Simultaneous Authentication of Equals* (RFC 7664), base do WPA3. Adeus PSK tradicional: o handshake Dragonfly usa prova de conhecimento zero, tornando capturas de ar totalmente imunes a ataques de dicionário offline com Hashcat ou Aircrack-ng.
  * `sae_pwe=2`: Força o método Hash-to-Element (H2E). Isso blinda a negociação contra os ataques de canal lateral conhecidos como *Dragonblood*, que exploravam variações de tempo no método antigo de caça-e-bicagem.
  * `ieee80211w=2`: Torna os *Protected Management Frames* (PMF, 802.11w) estritamente obrigatórios. Com ele, até os quadros de gerência da rede são assinados, neutralizando aqueles ataques clássicos de derrubar clientes injetando pacotes de desautenticação (*deauth flood*).
  * *E o isolamento de clientes?* Se o seu objetivo for um hotspot para visitantes, vale adicionar a diretiva `ap_isolate=1` para impedir que os clientes se enxerguem na camada L2. Como no meu caso a rede atende exclusivamente os meus próprios aparelhos (e eu quero transferir arquivos locais entre celular e notebook sem intermediários), deixei o parâmetro de fora.

* **Wi-Fi 6 High Efficiency e QoS (`wmm_enabled`, `ieee80211n`, `ht_capab`, `ieee80211ax`, `he_*`):**
  * `wmm_enabled=1`: Habilita as filas de QoS (IEEE 802.11e). Parâmetro obrigatório: sem WMM, as especificações 802.11n e 802.11ax rebaixam compulsoriamente a conexão para o teto de 54 Mbps do jurássico 802.11g.
  * `ht_capab=[SHORT-GI-20][TX-STBC][RX-STBC1]`: Ativa o intervalo de guarda curto (400 ns) e o *Space-Time Block Coding*, que ajuda o sinal a contornar reflexões nas paredes do cômodo transmitindo cópias redundantes e ortogonais pelas antenas.
  * `ieee80211ax=1`: Aciona o motor do Wi-Fi 6 (High Efficiency), liberando o uso de subportadoras densas e a modulação 1024-QAM.
  * `he_su_beamformer=1`: Ativa a formação de feixe (*beamforming*). O AP analisa o estado do canal reportado pelo smartphone e ajusta a fase do sinal em cada antena para que as ondas se somem de forma construtiva exatamente onde o aparelho está.

### Firewall moderno e roteamento com nftables

Com o rádio transmitindo e os endereços sendo distribuídos, o passo final é garantir que os pacotes da rede sem fio cheguem à internet pela placa cabeada `enp0s31f6`.

Primeiro, habilitamos o encaminhamento de pacotes no kernel criando o arquivo de persistência no `sysctl`:

```ini
# /etc/sysctl.d/99-ip-forward.conf
net.ipv4.ip_forward=1
```
*Habilitação do roteamento IPv4 no kernel Linux.*

Para aplicar imediatamente sem reiniciar:

```bash
sudo sysctl -p /etc/sysctl.d/99-ip-forward.conf
```

Antes, eu resolvia esse roteamento com três regras clássicas e imperativas de `iptables`:

```bash
sudo iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o enp0s31f6 -j MASQUERADE
sudo iptables -A FORWARD -i wlp0s20f3 -o enp0s31f6 -j ACCEPT
sudo iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
```
*As três regras clássicas de iptables para NAT e encaminhamento de pacotes.*

Essas três linhas resolvem o básico perfeitamente. No entanto, no Debian moderno o framework padrão do Netfilter é o `nftables` [^2]. Em vez de manter comandos soltos em scripts de inicialização ou depender de pacotes legados de persistência (`iptables-persistent`), o caminho mais limpo é consolidar essa tradução direta de forma declarativa e atômica no `/etc/nftables.conf`:

```nft
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority filter; policy accept;
    }
    chain forward {
        type filter hook forward priority filter; policy drop;
        ct state { established, related } accept
        iifname "wlp0s20f3" oifname "enp0s31f6" accept
    }
    chain output {
        type filter hook output priority filter; policy accept;
    }
}

table ip nat {
    chain postrouting {
        type nat hook postrouting priority srcnat; policy accept;
        ip saddr 192.168.100.0/24 oifname "enp0s31f6" masquerade
    }
}
```
*Regras nativas do nftables com correspondência direta às três regras de iptables.*

Note como a tradução entre os dois modelos é direta e sem rodeios:
1. `ct state { established, related } accept`: Substitui exatamente o `-m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT`, permitindo que respostas de pacotes que saíram voltem sem impedimentos.
2. `iifname "wlp0s20f3" oifname "enp0s31f6" accept`: É a tradução de `-i wlp0s20f3 -o enp0s31f6 -j ACCEPT`, autorizando os pacotes que chegam pelo Wi-Fi a cruzarem em direção à interface cabeada. No `nftables`, a política padrão do chain `forward` foi definida como `drop`, fechando o encaminhamento para qualquer outro sentido.
3. `ip saddr 192.168.100.0/24 oifname "enp0s31f6" masquerade`: Faz exatamente o mesmo papel do `-t nat -A POSTROUTING -s 192.168.100.0/24 -o enp0s31f6 -j MASQUERADE`, reescrevendo o IP de origem dos pacotes para o IP da interface cabeada.

> [!TIP]
> **Isolamento de portas locais para redes de visitantes:**
> Como o objetivo principal aqui é um ambiente de desenvolvimento (onde costumo subir serviços locais no computador e testá-los no notebook ou no celular pela rede sem fio), mantemos o chain `input` com `policy accept;`. Se o seu caso for um hotspot estritamente para visitantes ou dispositivos não confiáveis, vale a pena restringir o tráfego que entra pela interface sem fio apenas a portas essenciais como DNS (`udp/tcp 53`) e DHCP (`udp 67`), descartando as demais conexões ao host com regras específicas de `drop`.

Para carregar o conjunto de regras e garantir persistência nos próximos boots:

```bash
sudo systemctl enable --now nftables
```

## Telemetria real: 286 Mbps, 1024-QAM e WPA3 em 2.4 GHz

Com a pilha completa rodando, conectei um smartphone com suporte a Wi-Fi 6 à rede recém-criada. O aparelho associou-se no mesmo instante, exibindo o ícone de rede segura com o numeral 6 ao lado das barrinhas de sinal.

A ironia do momento é deliciosa: compramos uma placa batizada com pompa de Wi-Fi 6E, com suporte teórico a 6 GHz, canais nababescos de 160 MHz e promessa de gigabits por segundo, para no final do dia comemorar 286 Mbps cravados em 2.4 GHz no canal 13. É o equivalente exato a comprar uma Ferrari para rodar na primeira marcha em estrada de terra de condomínio rural. Mas hey: é uma Ferrari perfeitamente regulada, com WPA3 puro e sem bater na lataria dos vizinhos.

Para auditar o que estava acontecendo na camada física do rádio, consultei o subsistema de rede com a ferramenta `iw`:

```bash
sudo iw dev wlp0s20f3 station dump
```

A telemetria coletada no host confirmou a negociação das taxas:

```text
Station 22:39:6c:xx:xx:xx (on wlp0s20f3)
    inactive time:  3448 ms
    rx bytes:       1442331
    rx packets:     8110
    tx bytes:       733731
    tx packets:     2580
    signal:         -29 [-29, -42] dBm
    tx bitrate:     286.7 MBit/s HE-MCS 11 HE-NSS 2 HE-GI 0 HE-DCM 0
    authorized:     yes
    authenticated:  yes
    associated:     yes
    preamble:       short
    WMM/WME:        yes
    MFP:            yes
    DTIM period:    2
    short preamble: yes
    connected time: 573 seconds
```

Os dados dessa captura merecem uma leitura honesta:

* **Taxa de transferência teórica vs. prática:** O link cravou em 286.7 MBit/s de TX. Na norma IEEE 802.11ax, um canal de 20 MHz com modulação 1024-QAM (MCS 11) e Guard Interval curto (0.8 µs) entrega 143.38 Mbps por stream. Multiplicado por dois fluxos espaciais (`HE-NSS 2`), batemos no teto físico absoluto de 286.8 Mbps. Só não confunda taxa física (PHY) com milagre: descontando o overhead de pacotes, colisões e confirmações do CSMA/CA, a vazão real utilizável (*goodput* em TCP medido via `iperf3`) fica na casa dos 180 a 200 Mbps. Para navegar no celular e rodar vídeos em 4K, é mais do que sobra.
* **Preâmbulo curto ativo (`preamble: short`):** A diretiva `preamble=1` negociada com a estação poupou 96 µs de sinalização a cada pacote transmitido.
* **Modulação no talo (HE-MCS 11):** O rádio sustentou a modulação mais densa da norma: 1024-QAM, empacotando 10 bits por símbolo sob um sinal cristalino de -29 dBm.
* **Proteção de quadros confirmada (`MFP: yes`):** O hardware atestou o *Management Frame Protection*, garantindo que ninguém derruba o link com ataques bobos de desautenticação.

Para fechar o diagnóstico de segurança, consultei o estado da associação através do socket do `hostapd_cli`:

```bash
sudo hostapd_cli all_sta
```

O relatório retornou os detalhes da negociação criptográfica:

```text
22:39:6c:xx:xx:xx
flags=[AUTH][ASSOC][AUTHORIZED][SHORT_PREAMBLE][WMM][MFP][HT][HE]
dot11RSNAStatsSelectedPairwiseCipher=00-0f-ac-4 (CCMP-128)
AKMSuiteSelector=00-0f-ac-8 (SAE / WPA3-Personal)
sae_group=19 (NIST P-256 Curve)
```

A negociação WPA3-Personal foi concluída com sucesso: o seletor AKM foi definido em `00-0f-ac-8` (SAE puro), com a curva elíptica NIST P-256 (`sae_group=19`) e cifras CCMP-128 para os dados em trânsito.

### Conferindo o espectro com o WiFiman no celular

Para verificar o comportamento da rede do ponto de vista de quem está na ponta, abri o aplicativo WiFiman no próprio smartphone para auditar o espectro de radiofrequência ao redor.

A inspeção em campo trouxe resultados ainda mais interessantes:

* **O oásis no espectro:** No gráfico de densidade de radiofrequência, os canais 1, 6 e 11 aparecem tomados por uma sobreposição caótica de redes institucionais e corporativas competindo pelo meio (dezenas de SSIDs disputando espaço entre -50 dBm e -80 dBm). O canal 13 aparece como um platô isolado na borda direita (operando entre 2462 e 2482 MHz, com pico em 2472 MHz), registrando sinal estável de -30 dBm a -36 dBm sem qualquer outra rede sobreposta.
* **Latência e estabilidade:** No monitor de desempenho em tempo real, a latência do cliente até o gateway local (`192.168.100.1`) ficou em 8 ms (e 67 ms para a internet em `8.8.8.8`), com 0% de perda de pacotes. Fugir da disputa de meio dos canais saturados praticamente zerou as filas de contenção.
* **Simetria física em 286 Mbps:** O monitor de enlace do aparelho registrou velocidade física simétrica: 286 Mbps de download e 286 Mbps de upload no enlace PHY do Wi-Fi 6 (MIMO 2x2 em 20 MHz).
* **Proteção mandatória (`MFPR`):** O smartphone identificou a rede como Wi-Fi 6 (802.11ax) com fabricante Intel Corporate e as flags `[RSN-SAE-CCMP-128][ESS][MFPR][MFPC][SAE]`. A presença da flag `MFPR` (*Management Frame Protection Required*) atesta que o aparelho móvel assumiu o modo estrito de segurança, descartando qualquer pacote não autenticado.

## Exercícios

Para fixar a dinâmica de diagnóstico de adaptadores sem fio e auditoria de rádio no Linux, execute os desafios práticos abaixo no seu terminal.

**1. Auditoria de capacidades de emissão e restrições regulatórias do adaptador**

Como você pode inspecionar diretamente pelo kernel se o seu adaptador sem fio possui suporte oficial ao modo AP e quais frequências estão livres da trava `NO-IR`?

<details markdown="1">
<summary>Ver resposta</summary>

Para verificar os modos suportados pela interface física e inspecionar as frequências autorizadas para transmissão ativa, execute:

```bash
# 1. Verificar se a interface aceita operar como Access Point (modo AP)
iw phy phy0 info | grep -A 8 "Supported interface modes"

# 2. Listar frequências autorizadas e filtrar bloqueios de emissão ativa (NO-IR)
iw phy phy0 info | grep -E "Frequencies:|disabled|NO-IR"
```

*Se a saída de modos contiver `AP`, a placa possui suporte via nl80211. Frequências marcadas com `NO-IR` só podem ser utilizadas para escuta passiva ou conexão como cliente (STA).*

</details>

**2. Inspeção de telemetria e estado de clientes em tempo real**

Como você pode monitorar clientes associados ao seu ponto de acesso em tempo real sem derrubar o serviço ou consultar logs estáticos?

<details markdown="1">
<summary>Ver resposta</summary>

Utilize o socket de controle do `hostapd_cli` em modo interativo ou passe comandos diretos no terminal:

```bash
# Listar todos os clientes associados e suas flags de capacidades
sudo hostapd_cli all_sta

# Alternativamente, consultar a camada física do subsistema de rádio no kernel
sudo iw dev wlp0s20f3 station dump
```

*A saída do `station dump` revela a modulação real (MCS), o número de fluxos espaciais (NSS) e a intensidade do sinal em dBm da estação conectada.*

</details>

## Conclusão: no fim das contas, valeu a pena?

O que começou como uma simples curiosidade prática, querendo saber se dava pra subir um ponto de acesso Wi-Fi 6 no Debian pro celular sem depender de mágicas quebradas de interface gráfica, acabou virando uma expedição arqueológica pelo subsistema de rede do Linux e pelas idiossincrasias do microcódigo da Intel.

Por trás da promessa sedutora do "criar hotspot em um clique", existe um abismo de detalhes. Os adaptadores da Intel foram paridos com a premissa de serem apenas clientes; tentar forçar a placa a virar um roteador 5 GHz autônomo sem entender o que a fabricante fez no silício só resulta em mensagens crípticas de assertiva no `dmesg` e muita frustração.

Mas jogando pelas regras do jogo e aproveitando a brecha limpa do canal 13 em 2.4 GHz, o resultado compensou: conexão estável como rocha, WPA3 moderno com SAE puro, preâmbulo curto e velocidade real de sobra pros meus aparelhos, tudo orquestrado de forma declarativa e atômica.

Agora, se formos honestos na ponta do lápis (e a nossa fatura de energia elétrica exige essa honestidade): vale a pena manter um computador desktop de 80W ligado direto na tomada só pra servir Wi-Fi pro celular? *Por favor, não faça isso.* Se você quer apenas internet estável sem inventar moda, compre um roteador Wi-Fi 6 dedicado de duzentos reais que consome 5W e vá viver a sua vida em paz. Mas se o seu objetivo era o prazer sádico de domar o hardware, entender como o rádio do Linux opera por baixo do capô e não deixar a Intel decidir o que você pode ou não rodar na sua própria máquina: aí sim, cada linha de log valeu a pena.

## Referências

[^1]: **hostapd: IEEE 802.11 AP, IEEE 802.1X/WPA/WPA2/EAP/RADIUS Authenticator** {*w1.fi*} ([Link](https://w1.fi/hostapd/))
[^2]: **nftables: High performance traffic classification** {*Netfilter Project*} ([Link](https://netfilter.org/projects/nftables/))
[^3]: **Intel Wireless WiFi Drivers (iwlwifi)** {*Linux Wireless Documentation*} ([Link](https://wireless.wiki.kernel.org/en/users/drivers/iwlwifi))
[^4]: **Location Aware Regulatory (LAR) in Linux Wireless** {*Kernel.org cfg80211*} ([Link](https://wireless.docs.kernel.org/en/latest/en/developers/regulatory/processing_rules.html))
[^5]: **802.11ax (Wi-Fi 6) High Efficiency Physical Layer Overview** {*IEEE Standards Association*} ([Link](https://standards.ieee.org/ieee/802.11ax/6618/))
[^6]: **dnsmasq: A lightweight DHCP and caching DNS server** {*Simon Kelley / The Kape*} ([Link](https://thekelleys.org.uk/dnsmasq/doc.html))
[^7]: **Intel Wi-Fi on Linux: The LAR Nightmare** {*Tildearrow*} ([Link](https://tildearrow.org/?p=post&mid=72))
[^8]: **MediaTek (mt76): Linux wireless driver support for MT7921/MT7922** {*Linux Wireless Documentation*} ([Link](https://wireless.docs.kernel.org/en/latest/en/users/drivers/mediatek.html))
