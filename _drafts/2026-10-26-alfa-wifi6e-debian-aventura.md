---
layout: post
title: "Wi-Fi 6E no Debian: Da Injeção de Pacotes ao RDP de 720 Mbps"
subtitle: "Como transformar a Alfa AWUS036AXML num AP veloz e descobrir que o perigo mora nas pegadinhas do silício"
author:
  - "Eduardo N. S. R."
date: 2026-10-26 17:30:00 GMT-3
permalink: /posts/alfa-wifi6e-debian-aventura/
category: Artigos
tags: [Debian, Wi-Fi 6, Redes, Hardware, nftables]
published: false
---

Quem acompanhou {% include post-ref.html slug="wifi6-debian-trixie" text="quando tentei domar o firmware da Intel no Debian" %} sabe que o subsistema sem fio do Linux tem um talento especial para nos manter humildes. Naquela tentativa, a plaquinha interna AX211 bateu o pé com travas de frequência e me empurrou para uma conexão capenga de 2.4 GHz em 20 MHz. O rádio funcionou, claro, mas com o gostinho agridoce de navegar na velocidade da banda larga de quinze anos atrás.

Desta vez, eu queria velocidade de verdade.

A meta era resolver um perrengue clássico de home office: montar um ponto de acesso dedicado ao lado da minha mesa, entregando latência de milissegundos e vazão de sobra para sessões de Remote Desktop (RDP) no notebook pessoal. Nada de disputar canal congestionado com o roteador do trabalho ou passar varal de cabo de rede em cima da mesa.

Para fugir das limitações autoritárias da Intel, fui às compras no território clássico da segurança ofensiva e escolhi uma plaquinha USB-C Alfa Network, modelo AWUS036AXML. O anúncio prometia o paraíso dos entusiastas de rede: chipset MediaTek MT7921AUN, duas antenas avantajadas e suporte completo a Wi-Fi 6E cobrindo 2.4 GHz, 5 GHz e a cobiçada faixa de 6 GHz.

No papel, parecia infalível. Na prática, a caixinha prateada me deu uma sequência cômica de tropeços: pentest frustrado, canais invisíveis, Docker derrubando tráfego e aula forçada de física sobre antenas a 90 graus.

{% include toc.html %}

## O unboxing e a nostalgia do pentest dos anos 2000

Quem mexeu com segurança ofensiva nos anos 2000 sente um quentinho imediato no peito ao ver o logotipo da Alfa Network. A carcaça prateada com duas antenas rosqueáveis traz de volta a memória de rodar o BackTrack 3 via Live-CD, espetar a lendária AWUS036H com chip RTL8187L e quebrar chaves WEP em três minutos. Naquela época, qualquer pessoa com um terminal e uma placa com antena de 9 dBi se sentia em um filme de espionagem (que o diga aqueles que ainda fizeram os experimentos com latas de Pringles e de óleo de soja).

A AWUS036AXML é a herdeira direta dessa linhagem:

| Especificação | Detalhe do Hardware |
| :--- | :--- |
| **Modelo** | Alfa Network AWUS036AXML |
| **Chipset** | MediaTek MT7921AUN (MT7921AU / MT7921U) |
| **Interface** | USB 3.2 Gen 1 (Conector Type-C na carcaça) |
| **Bandas** | Tri-band simultâneo (2.4 GHz, 5 GHz e 6 GHz) |
| **Padrões** | IEEE 802.11a/b/g/n/ac/ax (Wi-Fi 6 e Wi-Fi 6E) |
| **Largura de Canal** | 20, 40 e 80 MHz |
| **Modulação Máxima** | 1024-QAM (OFDMA + MU-MIMO 2x2) |
| **Antenas** | 2x dipolos omnidirecionais RP-SMA destacáveis (5 dBi) |

Espetei o bichinho na porta USB 3.0 do meu desktop rodando Debian 13 (Trixie). O `dmesg` foi uma surpresa agradável logo de cara:

```text
usb 2-1: New USB device found, idVendor=0e8d, idProduct=7961, bcdDevice= 1.00
usb 2-1: Product: Wireless_Device
usb 2-1: Manufacturer: MediaTek Inc.
mt7921u 2-1:1.0: HW/SW Version: 0x8a108a10, Build Time: 20240520112852a
mt7921u 2-1:1.0: firmware: direct-loading firmware mediatek/WIFI_MT7961_patch_mcu_1_2_hdr.bin
mt7921u 2-1:1.0: firmware: direct-loading firmware mediatek/WIFI_RAM_CODE_MT7961_1.bin
mt7921u 2-1:1.0: Firmware init done
```

Nada de compilar código misterioso baixado de repositório abandonado no GitHub. Nada de DKMS quebrando porque o kernel `Linux 6.12` trocou o nome de uma estrutura interna. O módulo oficial `mt7921u` da árvore `mt76` subiu sereno em dois segundos, pronto para o trabalho.

Diante de tanta facilidade, a empolgação bateu forte.

Decidi colocar o rádio à prova antes de subir qualquer serviço de rede. Subi o modo monitor no terminal:

```bash
sudo ip link set dev wlx00c0cabb1023 down
sudo iw dev wlx00c0cabb1023 set type monitor
sudo ip link set dev wlx00c0cabb1023 up
```

Subiu liso. Abri o `airodump-ng` e vi beacons pipocando nas três faixas de frequência com excelente sensibilidade de recepção.

Foi aí que a curiosidade de pentester falou mais alto: será que essa belezinha injeta pacotes como as Alfas de antigamente?

Fui rodar o clássico teste de injeção:

```bash
sudo aireplay-ng --test wlx00c0cabb1023
```

O resultado foi quase cômico de tão decepcionante:

```text
Trying broadcast probe requests...
Injection is working!
Ping (ACK) to AP's...
No Answer...
Trying directed probe requests...
wlx00c0cabb1023 - channel: 6, packets: 0/30 (0%)
```

Zero respostas. Os pacotes de desautenticação e as sondagens forçadas simplesmente sumiram no ar sem deixar sinal de vida.

Fui investigar o código-fonte do driver `mt76` no kernel para entender o que estava acontecendo. Para um adaptador transmitir quadros arbitrários em modo monitor, o driver precisa declarar expressamente a flag `IEEE80211_HW_MONITOR_TX` na sua estrutura de recursos.

O `mt7921u` não só omite essa flag, como o próprio microcódigo da MediaTek traz travas internas que descartam qualquer frame gerado fora da máquina de estados oficial do 802.11 [^1]. Se um pacote forjado chega via raw socket em modo monitor, a rotina interna do kernel chama `kfree_skb()` e despacha o quadro direto para o esquecimento na memória.

> [!NOTE] Pentest moderno sem ilusões
> Se a sua intenção ao comprar a AWUS036AXML era derrubar o Wi-Fi alheio com deauth via `aireplay-ng`, esqueça. O hardware não dispara quadros fora da associação. Por outro lado, para cenários baseados em infraestrutura real, como Rogue AP, Evil Twin corporativo e captura limpa de handshakes WPA2/WPA3 em modo Master, a placa entrega uma estabilidade formidável.

Guardei as fantasias de hacker na gaveta e voltei ao plano central: construir um ponto de acesso absurdamente veloz.

## A Anatel, o domínio regulatório e o 6 GHz adormecido

Com a interface de volta ao modo de operação gerenciado, a primeira checagem de praxe foi inspecionar as permissões de frequência do rádio. Digitei o comando regulatório no terminal:

```bash
sudo iw reg get
```

A resposta do subsistema de rede veio com a proverbial cautela germânica:

```text
global
country 00: DFS-UNSET
...
(5955 - 7115 @ 20), (N/A, 20), (N/A), DISABLED
```

Sem uma identificação de país configurada, o Linux adota o código genérico `00`, o perfil mais medroso do mundo das telecomunicações. Nesse modo ultra-conservador, toda a faixa de 6 GHz (5955 MHz a 7115 MHz) fica sumariamente desativada por precaução. Nenhuma transmissão sai do papel.

Para destravar o rádio, avisamos ao sistema onde estamos pisando:

```bash
sudo iw reg set BR
```

Uma nova consulta com `iw reg get` revelou o espectro aberto:

```text
country BR: DFS-JP
    (2402 - 2482 @ 40), (N/A, 20), (N/A)
    (5170 - 5250 @ 80), (N/A, 30), (N/A), AUTO-BW
    (5250 - 5330 @ 80), (N/A, 24), (0 ms), DFS, AUTO-BW
    (5490 - 5730 @ 160), (N/A, 24), (0 ms), DFS
    (5735 - 5835 @ 80), (N/A, 30), (N/A)
    (5945 - 6425 @ 80), (N/A, 12), (N/A)
```

No Brasil, a Anatel autorizou o uso do espectro de 6 GHz para dispositivos de baixa potência em ambientes internos (LPI - *Low Power Indoor*), cravando um limite modesto entre 12 e 14 dBm de potência irradiada [^2]. Em contrapartida, na faixa de 5 GHz os canais baixos (36 a 48) e altos (149 a 161) ganharam permissão para transmitir em até 30 dBm, o equivalente a um watt inteiro de potência pura. O hardware agora tinha permissão legal para falar.

## O hotspot em 6 GHz e o mistério do canal fantasma

A minha primeira intenção foi explorar a novidade reluzente da placa: o **Wi-Fi 6E**. Na essência, o 6E é a extensão do protocolo 802.11ax operando na frequência desimpedida de 6 GHz.

Essa faixa é livre do congestionamento típico do ambiente urbano: nada de fornos de micro-ondas vazando ruído, babás eletrônicas ou dezenas de roteadores das operadoras brigando por migalhas nos prédios vizinhos. Um verdadeiro loteamento novo no espectro.

Configurar hotspot nessa frequência pelo assistente gráfico do NetworkManager é perda de tempo, já que ele insiste em sugerir larguras estreitas de 20 MHz e modos legados. Para fazer rádio de alta performance no Linux com controle fino, a única ferramenta que fala a nossa língua é o `hostapd`.

Elaborei um arquivo de configuração enxuto para inaugurar a transmissão em 6 GHz:

```ini
interface=wlx00c0cabb1023
driver=nl80211
ssid=Rede do Dudu
hw_mode=a
channel=1
op_class=133
ieee80211n=1
ieee80211ac=1
ieee80211ax=1
he_oper_chwidth=1
he_oper_centr_freq_seg0_idx=7
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
wpa_passphrase=1 senha muito difícil çê é loko!
```

Subi o serviço no terminal:

```bash
sudo hostapd /etc/hostapd/wifi6e.conf
```

O log respondeu pontualmente com a mensagem esperada:

```text
wlx00c0cabb1023: interface state UNINITIALIZED->ENABLED
wlx00c0cabb1023: AP-ENABLED
```

O ponto de acesso subiu sereno, emitindo sinal no Canal 1 (5955 MHz). Peguei meu Galaxy S25+, que vem com suporte nativo a Wi-Fi 6E, abri o menu de redes sem fio e fiquei aguardando o SSID aparecer. Nada aconteceu.

Aproximei o aparelho a cinco centímetros da antena e reiniciei o Wi-Fi do telefone. A lista de redes continuava ignorando a existência do meu roteador caseiro.

O problema não estava no Debian e nem na placa Alfa.

O mistério morava na própria especificação física do padrão IEEE 802.11ax [^3].

### Os canais PSC e o filtro de bateria

A faixa de 6 GHz é um latifúndio: **1200 MHz contínuos**, ou **59 canais de 20 MHz**.

Se o celular precisasse varrer 59 frequências enviando sondagens ativas e esperando beacons a cada vez que sai do bolso, a bateria derreteria antes do almoço. Para evitar essa drenagem, o padrão criou os **Canais de Varredura Preferenciais (PSC - *Preferred Scanning Channels*)**: em 6 GHz, clientes ignoram o resto do espectro e concentram a busca nos canais PSC, posicionados a cada 80 MHz pela fórmula $4n + 1$:

```text
Canais PSC Oficiais: 5, 21, 37, 53, 69, 85, 101, 117, 133, 149, 165, 181, 197, 213, 229
```

Quando configurei o `hostapd` no **Canal 1** (5955 MHz), o rádio transmitiu sem erro. Só que o Canal 1 não é PSC: o telefone passou batido por ele na varredura passiva, tratando o sinal como ar vazio.

Corrigi o arquivo de configuração e mudei a rede para o **Canal 69** (6295 MHz), um canal PSC autêntico com centro de 80 MHz no índice 71 (6305 MHz):

```ini
channel=69
op_class=133
he_oper_chwidth=1
he_oper_centr_freq_seg0_idx=71
```

Reiniciei o `hostapd`. Olhei para a tela do Galaxy S25+ e o ícone piscou na hora: surgiu o símbolo de Wi-Fi trazendo um pequenino e reluzente **6 acompanhado da letra E** (`6E`). A satisfação de ver o 6E funcionando no Debian foi formidável.

A festa só durou até o primeiro teste de velocidade.

## O speedtest travado e a pegadinha do MTU

Com o celular conectado e autenticado via WPA3-SAE, fui medir a velocidade com um sorriso confiante no rosto. Abri o aplicativo Speedtest da Ookla no telefone e apertei o botão para iniciar a medição.

O velocímetro subiu aos trancos até cômicos **0,02 Mbps**, empacou ali e começou a cuspir erros de conexão expirada. Uma rede de última geração negociada em 802.11ax com largura de 80 MHz e modulação 1024-QAM apanhando feio de um modem dial-up dos anos 90.

Fui direto ao terminal do desktop acompanhar o tráfego com `tcpdump -i wlx00c0cabb1023 -n`. O diagnóstico pulou na tela imediatamente.

O aplicativo do celular havia selecionado automaticamente um servidor de testes distante, com tempo de resposta acima de 200 ms. Ao abrir as conexões TCP, os pacotes grandes tentavam trafegar com o MTU padrão de 1500 bytes. No caminho pela internet, esses pacotes exigiam fragmentação, mas roteadores intermediários descartavam os avisos ICMP do tipo *Destination Unreachable: Fragmentation Needed*.

Sem essa notificação de volta, o tráfego caiu no conhecido **Path MTU Black Hole** [^4]. O cliente dispara os dados com a flag de não-fragmentação ativada, os pacotes somem na rota e a pilha TCP fica congelada aguardando retransmissões infinitas.

A solução no Linux é consagrada e não exige malabarismos: **TCP MSS Clamping**. Adicionamos uma instrução na tabela de mangle para limitar o tamanho máximo de segmento (MSS) nas conexões TCP SYN que cruzam a interface sem fio, forçando cada pacote a caber no tamanho real da rota:

```bash
sudo nft add table ip mangle
sudo nft add chain ip mangle wifi6e_mangle '{ type filter hook forward priority -150; }'
sudo nft add rule ip mangle wifi6e_mangle tcp flags syn tcp option maxseg size set rt mtu
```

Bastou aplicar essa regra para a conexão destravar e o celular começar a baixar dados a toda velocidade.

## A convivência com o Docker: quando o firewall barra a festa

Com o rádio operando e o MSS corrigido, era hora de organizar o roteamento e o NAT (*Masquerade*) no Debian. Em pleno ano de 2026, ninguém merece continuar remendando scripts legados com comandos soltos de `iptables`.

No Debian atual, a recomendação explícita é gerenciar pacotes através do subsistema moderno do `nftables` [^5]. Criei a tabela de NAT nativa e configurei o mascaramento da sub-rede do AP (`172.31.255.0/24`) saindo pela minha placa de rede cabeada (`enxf8e43b4ad63d`):

```bash
sudo nft add table ip nat
sudo nft add chain ip nat wifi6e_nat '{ type nat hook postrouting priority 100; }'
sudo nft add rule ip nat wifi6e_nat ip saddr 172.31.255.0/24 oifname "enxf8e43b4ad63d" masquerade
```

Também ativei o repasse de pacotes no kernel:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Voltei ao celular para conferir o resultado. O aparelho conectava no Wi-Fi, recebia o IP `172.31.255.10` via DHCP, mas não carregava absolutamente nada. Nem mesmo um simples ping para o endereço `1.1.1.1` conseguia resposta.

A tabela de NAT estava criada, o repasse ativado e as placas no ar. Adivinha quem estava engolindo o tráfego?

O nosso companheiro de trabalho de todos os dias: o **Docker** (e as políticas restritivas de firewall do host).

### Quando o firewall da máquina engole o tráfego

Se você roda Docker, Podman ou qualquer firewall ativo (seja via `nftables`, `iptables`, UFW ou firewalld), a política padrão da chain de encaminhamento (`FORWARD`) do kernel quase certamente estará definida como `DROP`.

Passamos por esse perrengue: o smartphone conectava no Wi-Fi, recebia IP e DNS sem erro, mas não carregava nada porque os pacotes morriam no firewall local antes de chegar à saída de internet.

Como cada ambiente tem sua própria configuração de rede, portas e contêineres, não existe uma receita de bolo única aqui. A regra de ouro é inspecionar o seu firewall e garantir que ele autorize o encaminhamento (*forwarding*) bidirecional entre a interface sem fio (`wlx00c0cabb1023`) e a interface de saída para a internet, sem atropelar o isolamento dos seus serviços locais. Com a passagem liberada no firewall, o tráfego flui sem atritos.

## Ajustes de desempenho no Kernel: BBR, buffers e DNS em RAM

Com a rede navegando, o passo seguinte era afinar o sistema para suportar a carga de trabalho prevista. Como o objetivo final era rodar sessões de Remote Desktop com alta taxa de quadros e comandos gráficos interativos, latência imprevisível e gargalos de fila precisavam ser contornados.

Aplicamos um conjunto pontual de ajustes no kernel do Debian:

### 1. Adeus CUBIC, bem-vindo BBR
O algoritmo tradicional de controle de congestionamento TCP (CUBIC) é baseado em detecção de perda de pacotes. Ele só reduz a velocidade de envio quando os buffers da rede transbordam e pacotes começam a sumir. Em conexões sem fio, onde oscilações passageiras de sinal causam pequenas variações normais de rádio, o CUBIC se assusta com facilidade e derruba a taxa sem necessidade real.

Substituímos o controle pelo algoritmo **BBR (Bottleneck Bandwidth and RTT)** desenvolvido pelo Google [^6]:

```bash
sudo sysctl -w net.core.default_qdisc=fq
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
```

O BBR mede a largura de banda física real e o tempo mínimo de trânsito dos pacotes, entregando taxa consistente sem encher as filas de latência (*zero bufferbloat*).

### 2. Dormir jamais: blindagem contra suspensão e bloqueio de tela

Um ponto de acesso de alta performance não pode vacilar. O problema é que o Linux adota rotinas ultra-agressivas de conservação de energia. Se você se levanta da mesa, bloqueia a tela com `Super+L` ou fecha a tampa do notebook para almoçar, o sistema entra em repouso e derruba as transmissões sem aviso.

Para garantir que o ponto de acesso permaneça 100% ativo 24/7, blindamos o ambiente em três camadas independentes:

1. **Rádio sem fio sempre acordado:** Desativamos o modo de economia do protocolo 802.11, garantindo que o transmissor RF da Alfa não desligue etapas de amplificação:
   ```bash
   sudo iw dev wlx00c0cabb1023 set power_save off
   ```
2. **Desativação total do USB Autosuspend:** Além de travar o controle em `on`, forçamos o tempo de autossuspensão para `-1`, eliminando o risco do kernel desligar a porta após 2 segundos de ociosidade:
   ```bash
   for dev in /sys/bus/usb/devices/*/idProduct; do
       if [ "$(cat "$dev" 2>/dev/null)" = "7961" ]; then
           usb_dir="$(dirname "$dev")"
           echo on | sudo tee "$usb_dir/power/control" > /dev/null
           echo -1 | sudo tee "$usb_dir/power/autosuspend" > /dev/null
       fi
   done
   ```
3. **Bloqueador de Suspensão do Sistema Operacional (`systemd-inhibit`):** O golpe de mestre. Envolvemos a execução do `hostapd` com o inibidor nativo do `systemd` [^7]:
   ```bash
   systemd-inhibit --what=sleep:idle:handle-lid-switch \
       --who="Wi-Fi 6 AP" \
       --why="Mantendo Access Point ativo" \
       hostapd "$CONF_FILE"
   ```
   Com essa instrução, o GNOME e o `systemd-logind` ficam expressamente proibidos de suspender a máquina, entrar em *sleep* por inatividade ou cortar a rede mesmo se a tampa do notebook for fechada.

### 3. Fila de transmissão e buffers ampliados
A fila padrão de pacotes na interface de rede sem fio do Linux costuma vir configurada em discretos 1000 pacotes. Elevamos esse limite para 3000 pacotes e redimensionamos os buffers de recepção e envio de sockets TCP para 16 megabytes:

```bash
sudo ip link set dev wlx00c0cabb1023 txqueuelen 3000
sudo sysctl -w net.core.rmem_max=16777216
sudo sysctl -w net.core.wmem_max=16777216
```

### 4. Cache DNS em RAM e reservas DHCP desacopladas com dhcp_hosts.conf
Para distribuição de DHCP e resolução de nomes, colocamos o `dnsmasq` escutando na interface sem fio, com cache em memória RAM dimensionado para 1000 entradas (`--cache-size=1000`).

Um teste rápido com o `dig` comprovou a velocidade de resposta instantânea:

```bash
dig @172.31.255.1 google.com
```

```text
;; Query time: 0 msec
;; SERVER: 172.31.255.1#53(172.31.255.1) (UDP)
```

Zero milissegundos de espera. Mas faltava um detalhe para o conforto do dia a dia: **fixar os IPs dos aparelhos** sem precisar editar scripts na unha.

Criamos um arquivo desacoplado chamado `dhcp_hosts.conf`, onde basta listar o MAC, o IP desejado e o nome da máquina:

```text
# Formato: MAC,IP,Nome_do_Dispositivo
64:1b:2f:fd:cd:a1,172.31.255.10,S25-de-Eduardo
00:d7:6d:af:43:44,172.31.255.20,fantasma
```

Passamos a flag `--dhcp-hostsfile=dhcp_hosts.conf` e rodamos com `--user=root` para leitura limpa no Debian. O comportamento do protocolo DHCP foi um espetáculo à parte:

```text
dnsmasq-dhcp: DHCPREQUEST(wlx00c0cabb1023) 172.31.255.80 00:d7:6d:af:43:44
dnsmasq-dhcp: DHCPNAK(wlx00c0cabb1023) 172.31.255.80 00:d7:6d:af:43:44 static lease available
dnsmasq-dhcp: DHCPDISCOVER(wlx00c0cabb1023) 172.31.255.20 00:d7:6d:af:43:44
dnsmasq-dhcp: DHCPACK(wlx00c0cabb1023) 172.31.255.20 00:d7:6d:af:43:44 fantasma
```

Quando o notebook pediu para renovar o IP antigo que tinha guardado na memória (`.80`), o servidor respondeu com `DHCPNAK (static lease available)`. O cliente entendeu o recado na hora, disparou um novo Discover e recebeu pontualmente o seu IP fixo definitivo (`172.31.255.20`), enquanto o Galaxy S25+ amarrou no `172.31.255.10`.

Rodei um teste de transferência local via `iperf3` com um único fluxo TCP para validar a integridade da pilha:

```bash
iperf3 -c 172.31.255.1 -P 1
```

O resultado marcou **556 Mbps reais de transferência contínua em TCP**, com um detalhe animador: **zero retransmissões** de pacotes durante todo o teste.

Tudo parecia pronto para o grande teste com o notebook.

## A surpresa no notebook: quando a placa não enxerga 6 GHz

Com o rádio em 6 GHz configurado no canal PSC 69, velocidade validada e DNS respondendo na hora, chegou o momento culminante: conectar o notebook corporativo que seria o usuário diário do RDP.

Abri o terminal e dei uma espiada no `lspci` para confirmar o modelo exato do adaptador interno:

```text
Network controller: Intel Corporation Wi-Fi 6 AX201 160MHz (rev 20)
```

Fiquei olhando fixamente para a tela por alguns instantes. A ficha demorou alguns segundos para cair.

Para quem não acompanha de perto o catálogo confuso de adaptadores sem fio da Intel, existe uma pegadinha fundamental aqui:
* A família **AX210 / AX211** é **Wi-Fi 6E** (opera em 2.4 GHz, 5 GHz e 6 GHz).
* A família **AX200 / AX201** é **Wi-Fi 6 clássico** (opera estritamente em dual-band: 2.4 GHz e 5 GHz).

O meu notebook não tem rádio físico para a faixa de 6 GHz: ele é cego para qualquer beacon na vizinhança dos 6000 MHz.

Todo aquele capricho sintonizando canal PSC, destravando potência LPI e comemorando o ícone no Galaxy S25+ gerou uma rede sem fio invisível para o único computador que eu realmente precisava usar todo santo dia.

> [!WARNING] O plano B de quem mexe com infra
> Em vez de reclamar do hardware, o jeito é rir da ironia e recalcular a rota. A vantagem de trabalhar com padrões abertos é a flexibilidade: se o cliente principal não alcança os 6 GHz, pivotamos para 5 GHz e aproveitamos todo o restante da pilha moderna do 802.11ax.

A pergunta seguinte era inevitável: dava para ter os mesmos ganhos de velocidade operando na faixa clássica de 5 GHz?

## A virada para 5 GHz: o canal fantasma 82 e o BSS Coloring

A resposta é afirmativa. Muita gente confunde os termos: a letra "E" no Wi-Fi 6E indica apenas o acesso à nova fatia de espectro em 6 GHz.

As principais inovações técnicas do protocolo 802.11ax continuam inteiramente ativas na faixa tradicional de 5 GHz:
1. Modulação densa de **1024-QAM** (que transporta 10 bits por símbolo em vez dos 8 bits do Wi-Fi 5);
2. Canais largos de **80 MHz com 1.2 Gbps** de taxa física teórica;
3. Preâmbulo curto com Guard Interval de 0,8 microssegundos;
4. Autenticação obrigatória com o moderno **WPA3-SAE**;
5. Mecanismo de **BSS Coloring** (*Spatial Reuse*);

Há inclusive uma vantagem prática considerável. Enquanto a faixa de 6 GHz em ambientes internos no Brasil fica amarrada pelo regulamento em moderados 12 a 14 dBm de potência, em 5 GHz a legislação permite alcançar até **30 dBm (1000 mW)** nos canais autorizados. O ganho de alcance através de paredes é muito mais vantajoso.

Hora de escolher a melhor frequência em 5 GHz.

### O canal 82 e a zona restrita do radar

Abri um aplicativo analisador de Wi-Fi no smartphone para mapear as emissões no prédio. Olhando para o gráfico de 5 GHz, notei uma clareira espetacular: entre o canal 64 e o canal 100, não havia nenhum sinal vizinho.

O espaço parecia completamente limpo por volta do canal 82. Achei que tinha encontrado o canal perfeito para navegar sozinho.

Fui conferir a tabela oficial de distribuição de frequências e veio a lição de regulação: **o canal 82 de Wi-Fi simplesmente não existe em nenhum lugar do mundo**.

O trecho de radiofrequência entre 5350 MHz e 5470 MHz é uma faixa de exclusão protegida por acordos internacionais para uso governamental estrito. Ela abriga radares militares de vigilância, radares meteorológicos e satélites do Serviço de Exploração da Terra [^8]. Dispositivo civil nenhum pode emitir sinal nessa janela.

### A tentativa nos canais 132 a 144 e o erro de DFS

Olhei um pouco mais para a direita no espectro e vi outro trecho desocupado: os canais de **132 a 144**. Configurei o `hostapd` para subir no Canal 132 com largura de 80 MHz (frequência central 138 / 5690 MHz):

```bash
sudo hostapd wifi6e.conf
```

A tela cuspiu um erro categórico:

```text
wlx00c0cabb1023: DFS-CAC-START freq=5660 chan=132 sec_chan=1, width=1, seg0=138, seg1=0, cac_time=60s
DFS start_dfs_cac() failed, -1
Interface initialization failed
wlx00c0cabb1023: interface state DFS->DISABLED
wlx00c0cabb1023: AP-DISABLED
```

Mais uma descoberta sobre o comportamento do hardware. Os canais de 52 a 144 pertencem à categoria **DFS (Dynamic Frequency Selection)**.

Nessas frequências, a norma exige que o ponto de acesso execute o procedimento de CAC (*Channel Availability Check*), ficando em silêncio escutando o ar durante 60 segundos antes de transmitir, para garantir que nenhum radar meteorológico está ativo nas proximidades.

O driver `mt7921u` da MediaTek no Linux é excelente como cliente, mas **não implementa a máquina de estados de radar mestre para modo AP**. Ao receber a ordem de iniciar o CAC vinda do `hostapd`, ele responde com erro `-1` e desativa a interface.

### A saída com o Canal 36 e a inteligência do BSS Coloring

Com os canais DFS inviabilizados pelo driver, a alternativa foi retornar à faixa **Non-DFS**: o bloco que vai do canal 36 ao 48. Esses canais entram no ar de forma instantânea, sem exigir checagem de radar.

Fixamos o rádio no **Canal 36**, com largura de **80 MHz** e centro de frequência no índice **42** (5210 MHz). Mas se o canal 36 já tiver redes de vizinhos transmitindo por perto, isso não causará disputa de tráfego?

É nesse cenário que entra o recurso mais esperto que o Wi-Fi 6 trouxe: o **BSS Coloring** [^9].

Nas gerações anteriores (802.11n e 802.11ac), dois roteadores no mesmo canal compartilhavam o mesmo domínio de contenção. Se o vizinho começasse a baixar um arquivo grande, o seu computador detectava o sinal via CSMA/CA e pausava o envio, aguardando o canal desocupar para não colidir.

No Wi-Fi 6, cada rede ganha uma cor digital (um identificador numérico de 1 a 63 colocado direto no preâmbulo físico do pacote). Configuramos uma cor exclusiva no `hostapd`:

```ini
he_bss_color=13
```

Quando o notebook com a Intel AX201 capta um pacote no canal 36, o transceptor analisa a cor em frações de microssegundo:
* Se a cor for `13`, o pacote é nosso e o sistema faz a leitura normal.
* Se a cor for diferente (um vizinho transmitindo), entra em ação o **Spatial Reuse**. O rádio do notebook ignora a transmissão alheia, ajusta o limite de sensibilidade e envia os nossos dados simultaneamente, sem esperar a fila do vizinho terminar.

## A física das antenas a 90 graus: polarização, MIMO e reflexões

Frequência definida e canal sintonizado, restava um ajuste prático: como posicionar as duas antenas do adaptador Alfa? Devo deixá-las retas para cima como duas pequenas hastes ou colocá-las em ângulo?

A explicação vem da física básica da propagação de ondas eletromagnéticas [^10]. As antenas que acompanham a AWUS036AXML são dipolos omnidirecionais de meia onda.

O padrão de irradiação de uma antena dipolo não tem a forma de uma esfera perfeita, mas sim o desenho de uma rosquinha em volta da haste:

```text
       Padrão de Irradiação de um Dipolo Vertical (Vista de Cima e Lateral)

               |  (Haste da Antena)
         .---' | '---.
       /       |       \     --> O sinal se propaga com força máxima no plano
      |    <----+---->  |        horizontal em volta da haste, mas tem ganho
       \       |       /         quase ZERO diretamente acima e abaixo da ponta!
         '---. | .---'
               |
```

A solução elegante da física para isso é criar **diversidade de polarização ortogonal**, mantendo um ângulo de 90 graus entre as duas antenas.

E aqui existem duas escolas práticas:
* **Configuração em "V" (Slant ±45°):** Ambas as antenas são inclinadas simetricamente para fora a cerca de 45 graus, formando uma abertura de 90 graus entre si. É a geometria adotada pelos grandes fabricantes de roteadores: cada antena decompõe sua energia em 50% no plano vertical e 50% no plano horizontal. O sinal chega equilibrado tanto para o notebook quanto para o celular pousado na mesa, sem que nenhuma antena aponte o seu "nulo" para os aparelhos.
* **Configuração em "L" (Vertical + Horizontal):** Uma antena fica reta para o teto (90 graus) e a outra dobrada na horizontal (0 graus). O alinhamento com o notebook fica exato (uma para a tela e outra para a base), mas exige cuidado para não apontar a ponta da haste horizontal para a sua cadeira.

Para este teste de bancada, posicionei as duas antenas em **"V"**, abrindo os 90 graus entre elas. O teste em "L" ficou anotado na caderneta de campo para um comparativo futuro, mas o que o formato em V entregou já foi um assombro.

## O resultado na prática: 727 Mbps no ar e 270 Mbps através do concreto

Com os parâmetros alinhados, a configuração definitiva da rede entrou no ar:
* **SSID:** `Rede do Dudu`
* **Senha:** `1 senha muito difícil çê é loko!`
* **Banda:** 5 GHz (802.11ax em 80 MHz, Canal 36, Centro 42)
* **BSS Color:** `13`
* **Segurança:** WPA3-Personal puro (SAE com curva NIST P-256)

Fizemos duas rodadas de medições reais de transferência e latência através do Speedtest.

### Cenário 1: Notebook a meio metro da antena (visada direta)

Com o notebook repousado na mesma mesa ao lado da Alfa AWUS036AXML, a interface negociou taxa física teórica de 1201 Mbps no Linux. Disparei o teste de velocidade:

```text
==================================================================
   RESULTADO DO SPEEDTEST (LINHA DE VISADA - 0.5 METRO)
==================================================================
   Latência:       6 ms (Jitter: 0.8 ms)
   Download:       727.54 Mbps
   Upload:         380.20 Mbps
   Perda de Pcts:  0.0%
==================================================================
```

Foram **727 Mbps reais de download pelo ar**, com latência cravada em 6 milissegundos.

Para contextualizar esse número: uma porta de rede Gigabit Ethernet física cabeada entrega cerca de 940 Mbps reais após o desconto dos cabeçalhos de rede. Atingimos **mais de três quartos da velocidade de um cabo físico** operando em radiofrequência pura.

### Cenário 2: Notebook em outro cômodo (duas paredes de concreto)

Levei o computador para outro cômodo da casa, fechando a porta e colocando duas paredes espessas de alvenaria e conduítes no caminho do sinal. O nível de recepção caiu para -68 dBm, mas a modulação 802.11ax se manteve estável graças à potência regulatória de 5 GHz.

Rodei uma nova medição:

```text
==================================================================
   RESULTADO DO SPEEDTEST (DISTANTE - 2 PAREDES DE CONCRETO)
==================================================================
   Latência:       8 ms (Jitter: 1.2 ms)
   Download:       270.89 Mbps
   Upload:         195.40 Mbps
   Perda de Pcts:  0.0%
==================================================================
```

**Mais de 270 Mbps de velocidade líquida e 8 ms de latência**, mesmo com duas paredes maciças no trajeto.

Para sessões de Remote Desktop (RDP), onde um fluxo em 60 FPS com codificação H.264/AVC444 consome cerca de 30 a 50 Mbps de banda com picos ocasionais de 80 Mbps, 270 Mbps oferecem uma folga de mais de três vezes a capacidade exigida.

Ao abrir a sessão de trabalho remota, a resposta do teclado, a renderização de janelas e a rolagem no editor de código ficaram indistinguíveis de um monitor conectado diretamente na máquina. Zero atraso perceptível de digitação, zero borrões de compressão visual.

## O teste de fogo institucional: Cabo (975 Mbps) vs Wi-Fi (383 Mbps)

Com o ponto de acesso operando, abri o OpenSpeedTest na rede da universidade (UFU) para medir a entrega ponta a ponta.

No meio do caminho, nos deparamos com um gargalo curioso: a interface cabeada do próprio desktop estava negociando a apenas 100 Mbps em vez de Gigabit. O motivo foi um acidente clássico de infraestrutura: dias antes, uma tempestade com raio havia atingido o prédio e avariado a porta do switch (o chip ativou o *Ethernet Downshift* [^11], recuando discretamente para 100 Mbps nos pares sobreviventes). Bastou mudar o cabo para uma porta sã no switch para liberar o 1 Gbps real na saída e permitir que o rádio Wi-Fi mostrasse seu fôlego total.

### 1. No Desktop (Cabo Gigabit Dedicado)

O desktop cabeado simplesmente pulverizou o velocímetro:

![OpenSpeedTest no Desktop cabeado](/assets/images/posts/wifi6/speedtest-pc-cabo-gigabit.png)
*Figura 1: Teste no PC conectado diretamente via cabo ao switch Alcatel.*

Foram **975.8 Mbps de download**, **940.5 Mbps de upload**, **1 ms de ping** e **0 ms de jitter**. O limite matemático exato de uma porta Gigabit física após o desconto dos cabeçalhos Ethernet, IP e TCP.

### 2. No Notebook (Wi-Fi 6 em 5 GHz / 80 MHz)

Em seguida, disparei a mesma medição no notebook conectado ao nosso AP da Alfa Network:

![OpenSpeedTest no Notebook via Wi-Fi 6](/assets/images/posts/wifi6/speedtest-notebook-wifi.png)
*Figura 2: Teste no notebook conectado ao ponto de acesso Wi-Fi 6.*

O resultado marcou **306.6 Mbps de download**, **383.1 Mbps de upload**, com inacreditáveis **2 ms de ping** e **0.4 ms de jitter**.

### Por que o Wi-Fi entrega menos vazão que o cabo se o rádio negocia a 1.2 Gbps?

Para quem olha a taxa nominal de enlace no Linux (`1200.9 MBit/s 80MHz HE-MCS 11`), ver 380 Mbps no teste prático parece uma contradição. Mas isso se deve a três fatores fundamentais de engenharia de redes:

1. **Full-Duplex vs Half-Duplex:** O cabo de rede transmite e recebe simultaneamente sem colisão em fios separados. O ar é um meio compartilhado e estritamente *Half-Duplex*: o rádio só fala **ou** escuta. Cada transmissão exige preâmbulo RF, tempos de guarda (*Guard Intervals*), contenção CSMA/CA e envio de confirmações (*Block ACKs*). Na prática do mundo real, a vazão TCP líquida de uma rede sem fio gira tipicamente em torno de **40% a 50% da taxa PHY nominal**.
2. **A travessia de dois barramentos USB 3.0 + NAT do Kernel:** O pacote do notebook viaja pelo ar, entra na antena da Alfa pelo barramento USB 3.0 (`mt7921u`), passa pelo mascaramento NAT na CPU do Debian, desce para o hub Dell DA310 por outro barramento USB 3.0 (`r8152`) e só então alcança o cabo. Há um duplo trânsito de barramento no caminho.
3. **Divisão de Airtime (*Airtime Sharing*):** Durante a medição, tanto o notebook corporativo quanto o Galaxy S25+ estavam associados ao rádio no mesmo canal 36, compartilhando o tempo de antena.

### Destravando o freio de mão: Agregação A-MPDU, Short-GI e Beamforming

Ao investigar por que a taxa estava abaixo do que o hardware da Alfa podia entregar, fui inspecionar as capacidades brutas da interface com `iw dev wlx00c0cabb1023 info` e o relatório do rádio com `iw phy phy2 info`.

Descobrimos dois "freios de mão" puxados por padrão:

1. **Rádio operando com economia de energia oculta:** A interface sem fio subia com `Power save: on` ativado pelo subsistema do Linux, fazendo o transceptor dormir intermitentemente entre rajadas de pacotes. Desativamos isso na raiz com `iw dev wlx00c0cabb1023 set power_save off`.
2. **`hostapd` em modo ultraconservador:** O nosso arquivo de configuração inicial gerava apenas um tímido `ht_capab=[HT40+]`. Sem declarar o bloco de recursos VHT (`vht_capab`), o `hostapd` operava com agregação mínima de quadros, mantinha o intervalo de guarda longo (800 ns) e ignorava o suporte a Beamforming do chip MediaTek.

Consultamos a matriz de recursos do MT7921 e injetamos as capacidades máximas de transmissão no `hostapd`:

```ini
# Agregação máxima e preâmbulo rápido em 5 GHz
ht_capab=[HT40+][LDPC][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1][MAX-AMSDU-7935]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[MAX-MPDU-11454][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP7][RXLDPC]

# Recursos Ax avançados: Beamforming ativo e TWT
he_oper_chwidth=1
he_oper_centr_freq_seg0_idx=42
he_su_beamformer=1
he_su_beamformee=1
he_mu_beamformer=1
```

Esse ajuste mudou o jogo no ar:
* **Agregação Máxima A-MPDU (`MAX-A-MPDU-LEN-EXP7`) e A-MSDU (`7935`):** agrupa dezenas de pacotes TCP pequenos num único disparo de rádio, cortando o desperdício de tempo com confirmações (*ACKs*) no ar.
* **`SHORT-GI-80`:** reduz o intervalo entre símbolos de 800 ns para 400 ns (~11% a mais de taxa líquida).
* **`RXLDPC` e Beamforming SU/MU:** enquanto o LDPC corrige bits corrompidos por hardware sem pedir retransmissão, as duas antenas da Alfa ajustam a fase das ondas para focar o sinal direto no notebook.

Com esses ajustes aplicados, a camada de rádio saiu do modo conservador e passou a operar no limite máximo das especificações do padrão 802.11ax.

## A estrutura final dos scripts prontos e portáteis

Para transformar toda essa jornada em uma solução limpa, elegante e reutilizável, organizei os arquivos em um pacote modular autocontido:

```text
/home/eu/du/sec/wifi6/
├── wifi6e.env          # Central de variaveis operacionais e credenciais
├── dhcp_hosts.conf     # Reservas de IP estatico desacopladas (MAC -> IP)
├── wifi6e-start.sh     # Orquestrador com blindagem systemd-inhibit e power save
└── wifi6e-stop.sh      # Encerramento atomico e restauracao do NetworkManager
```

A grande sacada de engenharia aqui foi **eliminar completamente qualquer caminho absoluto (hardcoded)** nos scripts:

```bash
# Detecta a pasta real onde o script reside, nao importa de onde seja executado
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/wifi6e.env"
CONF_FILE="${SCRIPT_DIR}/wifi6e.conf"
HOSTS_FILE="${SCRIPT_DIR}/dhcp_hosts.conf"
```

Você pode mover essa pasta para `/opt/wifi6`, colocar num pen drive ou clonar em outra máquina com Debian: ao rodar `sudo ./wifi6e-start.sh`, o script orquestrador:
1. Detecta a pasta local e carrega as variáveis do `wifi6e.env`;
2. Ajusta buffers TCP BBR e desliga o autosuspend do USB (`power/control=on`, `autosuspend=-1`);
3. Desativa o power save do rádio (`iw dev ... set power_save off`);
4. Configura as regras de encaminhamento no firewall e o NAT com mascaramento dinâmico;
5. Sobe o `dnsmasq` lendo as reservas estáticas de `dhcp_hosts.conf`;
6. Envolve o `hostapd` com o `systemd-inhibit` para que a tela possa ser bloqueada sem o PC dormir;
7. Ao pressionar `Ctrl+C`, o `trap cleanup` restaura o sistema ao estado padrão e devolve a interface gerenciada ao NetworkManager.

## Conclusão: o que aprendemos domando o silício

Relembrando os obstáculos pelo caminho, motivos para desistir não faltaram:
1. A decepção de descobrir que o chip MediaTek não injeta pacotes brutos em modo monitor;
2. A surpresa do celular ignorando o Canal 1 em 6 GHz pela regra dos canais PSC;
3. O teste de velocidade congelando em 0,02 Mbps por falta de MSS Clamping;
4. O repasse de pacotes barrado pelas políticas de encaminhamento no firewall do host;
5. A descoberta cômica de que o notebook não tinha rádio para 6 GHz;
6. O driver do rádio rejeitando canais DFS por falta de rotina de checagem de radar;
7. O cabo de rede upstream limitado a 100 Mbps por uma porta avariada no switch;
8. O perigo do rádio dormir ao bloquear a tela resolvido com `systemd-inhibit`.

Qualquer aplicativo gráfico convencional teria soltado uma mensagem genérica de "Falha na conexão", deixando o usuário no escuro sem saber o que corrigir. No terminal, cada sintoma tem uma causa física ou lógica muito clara no protocolo e no kernel.

O Wi-Fi 6 em 5 GHz com BSS Coloring, agregação máxima A-MPDU e antenas a 90 graus entregou mais estabilidade, alcance e vazão prática do que a ideia original do 6 GHz de baixa potência. O ponto de acesso está pronto para a rotina diária de trabalho, oferecendo uma experiência de RDP que nenhuma rede sem fio de escritório saturada consegue igualar.

Tudo isso funcionando em Linux puro, com regras atômicas de firewall e duas antenas ortogonais posicionadas com rigor científico.

## Referências

[^1]: **MediaTek (mt76): Linux wireless driver support for MT7921/MT7922** {*Linux Wireless Documentation*} ([Link](https://wireless.docs.kernel.org/en/latest/en/users/drivers/mediatek.html))
[^2]: **Resolução nº 742/2021: Regulamento sobre Canalização e Condições de Uso de Radiofrequências na Faixa de 5.925 MHz a 7.125 MHz** {*Agência Nacional de Telecomunicações - Anatel*} ([Link](https://informacoes.anatel.gov.br/legislacao/resolucoes/2021/1517-resolucao-742))
[^3]: **IEEE Std 802.11ax-2021: Enhancements for High Efficiency WLAN** {*IEEE Standards Association*} ([Link](https://standards.ieee.org/ieee/802.11ax/6618/))
[^4]: **Path MTU Discovery and Filtering ICMP: The Black Hole Problem (RFC 2923)** {*Internet Engineering Task Force - IETF*} ([Link](https://datatracker.ietf.org/doc/html/rfc2923))
[^5]: **nftables: High performance traffic classification and Netfilter framework** {*Netfilter Project*} ([Link](https://netfilter.org/projects/nftables/))
[^6]: **BBR: Congestion-Based Congestion Control** {*ACM Queue / Neal Cardwell, Yuchung Cheng, et al.*} ([Link](https://queue.acm.org/detail.cfm?id=3022184))
[^7]: **systemd-inhibit: Inhibit system sleep, shutdown, or idle behavior** {*freedesktop.org systemd Manual*} ([Link](https://www.freedesktop.org/software/systemd/man/systemd-inhibit.html))
[^8]: **ITU-R Recommendation M.1652: Dynamic frequency selection in wireless access systems including radio local area networks in 5 GHz** {*International Telecommunication Union*} ([Link](https://www.itu.int/rec/R-REC-M.1652/en))
[^9]: **Spatial Reuse and BSS Coloring in 802.11ax: High-Efficiency Wi-Fi** {*Wi-Fi Alliance Technical Whitepaper*} ([Link](https://www.wi-fi.org/discover-wi-fi/wi-fi-certified-6))
[^10]: **Antenna Theory: Analysis and Design (4th Edition)** {*Constantine A. Balanis / Wiley*} ([Link](https://www.wiley.com/en-us/Antenna+Theory%3A+Analysis+and+Design%2C+4th+Edition-p-9781118642061))
[^11]: **IEEE Std 802.3ab-1999: Physical Layer Parameters and Specifications for 1000 Mb/s Operation over 4-Pair Category 5 Balanced Cabling** {*IEEE Standards Association*} ([Link](https://standards.ieee.org/ieee/802.3ab/1090/))
