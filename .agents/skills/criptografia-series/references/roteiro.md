# Roteiro Detalhado: Série Criptografia na Prática

> [!TIP] Eficiência de Tokens
> **NÃO leia o arquivo inteiro.** Ao redigir ou revisar uma parte específica, consulte exclusivamente o bloco correspondente utilizando `view_file` com slice (`StartLine`/`EndLine`).

---

## Parte 1 — Fundamentos: X.509, ASN.1 e a Cadeia de Confiança

- **Arquivo:** `_posts/2026/10/2026-10-24-pki-fundamentos.md`
- **Permalink:** `/posts/pki-fundamentos/`
- **Data:** `2026-10-24 10:00:00 GMT-3`
- **Título:** "PKI com OpenSSL, Parte 1 - Fundamentos: X.509, ASN.1 e a Cadeia de Confiança"
- **Subtitle:** "Tudo aquilo que o certificado SSH deixou de fora: a sopa de letrinhas finalmente explicada"
- **Categoria:** `Tutoriais`
- **Tags:** `[Criptografia, Segurança, PKI, OpenSSL]`
- **Mermaid:** `true`
- **Objetivo Técnico:** O leitor compreende exatamente por que cada campo e extensão X.509 existe, disseca qualquer saída de `openssl x509 -text` linha a linha e entende detalhadamente o algoritmo de validação de caminho (RFC 5280).
- **Referências Indicadas:** R01, R02, R07, R08, R09, R10, R11, R12, R20, R21, R22, R23, R24, R31, R32, R33, R40, R43, R46, R47, R49, R70, R71, R72, R81.

### Estrutura de Seções:
1. **Introdução:**
   - Gancho com o post `certificados-ssh` ("certificados SSH não são X.509... respire fundo"). Assumir o compromisso de pagar essa dívida técnica.
   - Contexto da série e sumário via `{% raw %}{% include toc.html %}{% endraw %}` posicionado antes do primeiro `##`.
   - *Atenção:* Sem footnotes no primeiro parágrafo.
2. **O Problema que Ninguém Resolve com Matemática Pura:**
   - Criptografia assimétrica resolve sigilo e integridade, mas não autenticidade ("De quem é esta chave pública?").
   - O ataque clássico de Man-in-the-Middle (MITM).
   - Revisão precisa das primitivas: hash criptográfico, assinatura digital (desmistificar o mito "assinar é cifrar com a privada", válido apenas para RSA de livro escolar e incorreto para esquemas modernos como ECDSA/Ed25519) e troca de chaves Diffie-Hellman efêmera.
3. **Três Modelos de Confiança para a Mesma Pergunta:**
   - TOFU (*Trust On First Use* do SSH `known_hosts`).
   - Hierárquico (X.509/PKI; CA SSH também opera como hierarquia de 1 nível).
   - Teia de Confiança / Descentralizado (*Web of Trust* do OpenPGP).
   - Diagrama Mermaid comparando os três modelos.
   - Opinião firme: nenhum modelo é inerentemente superior; cada um foi desenhado para resolver um trade-off operacional distinto.
4. **O que é, de fato, uma PKI:**
   - Desmistificar: PKI não é "um arquivo de certificado", mas um ecossistema de pessoas, políticas, hardware e software.
   - Papéis operacionais: CA (Autoridade Certificadora), RA (Autoridade de Registro), VA (Autoridade de Validação), Repositório, *Subscriber* e *Relying Party*.
   - CP e CPS (RFC 3647).
   - O modelo público global: Web PKI, CA/Browser Forum (Baseline Requirements) e os Root Programs dos principais mantenedores (Mozilla NSS, Google Chrome, Apple, Microsoft).
5. **Anatomia de um Certificado X.509 v3:**
   - Análise baseada em certificado real inspecionado via `openssl s_client -connect example.com:443 -showcerts`.
   - Dissecação da estrutura: `tbsCertificate`, `signatureAlgorithm`, `signatureValue`.
   - Campos essenciais: Version, Serial Number, Signature, Issuer, Validity (notBefore / notAfter), Subject, Subject Public Key Info.
6. **ASN.1, DER, PEM e o Zoológico de Formatos:**
   - ASN.1 como notação abstrata e DER como codificação binária estrita TLV (Tag-Length-Value).
   - Inspeção estrutural com `openssl asn1parse -i`.
   - PEM como envelope Base64 com cabeçalhos textuais padronizados (RFC 7468).
   - Tabela definitiva de extensões e formatos: `.pem`, `.crt`, `.cer`, `.der`, `.key`, `.csr`, `.p12`/`.pfx`, `.p7b`.
   - Chaves privadas: PKCS#1 (`BEGIN RSA PRIVATE KEY`) vs SEC1 (`BEGIN EC PRIVATE KEY`) vs PKCS#8 (`BEGIN PRIVATE KEY` / `BEGIN ENCRYPTED PRIVATE KEY`).
   - Callout: `.crt` vs `.pem` é convenção de nomenclatura; o cabeçalho interno e a codificação definem o formato real.
7. **Distinguished Names e o Fim do Common Name:**
   - O padrão X.500: C, ST, L, O, OU, CN.
   - Por que o `Common Name` (CN) foi aposentado para validação de hostnames (RFC 6125/9525, depreciação nos navegadores a partir de 2017) e o SAN virou obrigatório.
   - Contraponto de infraestrutura: onde o CN/O ainda tem valor semântico (como identidades de usuários e grupos para RBAC no Kubernetes).
8. **Extensões X.509: Onde Mora a Política:**
   - `basicConstraints`: flag CA e controle de profundidade `pathlen`.
   - `keyUsage`: propósitos criptográficos básicos (`digitalSignature`, `keyCertSign`, `cRLSign`) e por que omitir `keyEncipherment` em curvas elípticas modernas (ECDHE).
   - `extendedKeyUsage` (EKU): propósitos de aplicação (`serverAuth`, `clientAuth`, `codeSigning`). Decisão recente de 2025/2026: Let's Encrypt removeu `clientAuth` de certificados públicos, tornando a PKI privada indispensável para mTLS.
   - `subjectAltName` (SAN): DNS names, IP addresses, emails, URIs.
   - `subjectKeyIdentifier` (SKI) e `authorityKeyIdentifier` (AKI): como os elos da cadeia se correlacionam deterministicamente.
   - `nameConstraints`: restrição de escopo de emissão de CAs subordinadas.
   - `cRLDistributionPoints` e `authorityInfoAccess` (AIA): publicação de listas de revogação e endpoints OCSP.
   - O conceito de extensão crítica (`critical`): se o validador não compreender a extensão, o certificado DEVE ser rejeitado. Comparação direta com as *Critical Options* dos certificados SSH.
9. **A Cadeia de Confiança e a Validação de Caminho:**
   - Trust Anchors e o processo de *Path Building* versus *Path Validation* (RFC 5280 §6).
   - Por que a assinatura da Root é autoatestada e irrelevante matematicamente: confiança decorre da presença na Trust Store.
   - Trust stores nos sistemas operacionais: `ca-certificates` no Debian (`/etc/ssl/certs`), Mozilla NSS, Chrome Root Store.
   - Diagrama Mermaid do algoritmo de validação passo a passo com causas de aborto.
10. **Algoritmos Criptográficos: RSA, ECDSA e o Paradoxo do Ed25519:**
    - Comparativo de tamanhos de chave, performance e níveis de segurança equivalentes (NIST SP 800-57).
    - As regras do CA/B Forum: RSA (mínimo 2048 bits) e ECDSA (P-256 / P-384).
    - O paradoxo: por que recomendamos Ed25519 no SSH, mas adotamos ECDSA P-384/P-256 no X.509? O ecossistema público de TLS ainda não suporta amplamente certificados Ed25519 (RFC 8410), restringindo Ed25519 a PKIs estritamente privadas.
11. **X.509 vs Certificados SSH vs OpenPGP:**
    - Tabela comparativa ampla (modelo de confiança, formato, identidade, permissões, validade, revogação, trust store, ecossistema).
    - Mapeamento direto com as flags de `ssh-keygen` do post anterior (`-n` principals ~ SAN, `-h` ~ EKU, `-V` ~ validity, `-I` ~ Subject/serial, KRL ~ CRL).
    - Gancho para OpenPGP: como a teia de confiança descentralizada descarta CAs.
12. **Diagnóstico e Troubleshooting:**
    - Comandos reais com `openssl s_client`, `openssl x509`, `openssl asn1parse`, `openssl verify` e `trust list`.
    - Comparação de inspeção de certificados SSH (`ssh-keygen -L`) e X.509 lado a lado.
13. **Exercícios:**
    - 5 exercícios conceituais e práticos de inspeção, dissecação DER, análise de ASN.1 e mapeamento com o SSH.
14. **Conclusão:**
    - Fechamento da teoria e preparação do cenário para o laboratório hands-on da Parte 2.
15. **Referências:**
    - Citações canônicas formatadas estritamente em notas de rodapé `[^n]`.

---

## Parte 2 — Laboratório: Construindo uma CA de Duas Camadas

- **Arquivo:** `_posts/2026/11/2026-11-07-pki-laboratorio-openssl.md`
- **Permalink:** `/posts/pki-laboratorio-openssl/`
- **Data:** `2026-11-07 10:00:00 GMT-3`
- **Título:** "PKI com OpenSSL, Parte 2 - Laboratório: Construindo uma CA de Duas Camadas"
- **Subtitle:** "Root offline, intermediária com rédea curta e mTLS de verdade, tudo no braço com openssl ca"
- **Categoria:** `Tutoriais`
- **Tags:** `[Criptografia, Segurança, OpenSSL, Linux]`
- **Mermaid:** `true`
- **Objetivo Técnico:** O leitor monta uma Autoridade Certificadora completa em duas camadas (Root offline + Intermediária com restrições rígidas), emite certificados de servidor e cliente com OpenSSL puro, configura e valida mTLS e reproduz erros reais de verificação.
- **Referências Indicadas:** R13, R14, R15, R20, R21, R24, R25, R26, R30, R40, R41, R42, R43, R44, R45, R70.

### Estrutura de Seções:
1. **Introdução:**
   - A necessidade real de PKI privada (o fim do suporte a `clientAuth` na Web pública).
   - Por que usar `openssl ca` (com base de dados `index.txt` e seriais) em vez de simples `openssl x509 -req`.
   - Aviso de realismo: ferramentas como Vault, step-ca ou cfssl para produção vs a importância de entender o mecanismo subjacente com OpenSSL.
2. **Arquitetura de Diretórios e os Arquivos `openssl.cnf`:**
   - Estrutura física isolada: `~/pki-lab/{root,intermediate}/{certs,crl,csr,newcerts,private}`.
   - Arquivos de estado: `index.txt`, `serial`, `crlnumber`.
   - Permissões estritas: `chmod 700 private`.
   - Anatomia comentada dos arquivos de configuração: `[ca]`, `[CA_default]`, políticas `policy_strict` vs `policy_loose`, extensões `v3_root_ca`, `v3_intermediate_ca`, `server_cert`, `client_cert`.
   - Análise de segurança da diretiva `copy_extensions` (por que `copyall` é extremamente perigoso).
3. **A Root CA (Camada Raiz):**
   - Geração da chave privada ECDSA P-384 cifrada com AES-256 (`openssl genpkey`).
   - Emissão do certificado raiz autoassinado (validade de 10 anos) com `basicConstraints = critical, CA:true`.
   - Inspeção detalhada do certificado raiz.
   - Procedimentos de segurança: cerimônia de chave, guarda offline em mídia isolada e backups redundantes.
4. **A Intermediate CA (Camada Intermediária Operacional):**
   - Criação da chave privada ECDSA P-384 e CSR da subordinada.
   - Assinatura com `openssl ca -config root.cnf` aplicando `v3_intermediate_ca`.
   - Aplicação prática de `pathlen:0` (impedindo a criação de sub-CAs) e `nameConstraints = critical, permitted;DNS:.example.com`.
   - Montagem correta do bundle de cadeia `ca-chain.pem` (ordem: intermediária seguida da raiz).
5. **Emissão de Certificados de Servidor:**
   - Geração de CSR com Subject Alternative Names (SAN) para `php-01.example.com` e `db-01.example.com`.
   - Assinatura pela intermediária com validação estrita das extensões de servidor.
   - Criação do bundle `fullchain.pem` do servidor (certificado de folha + intermediária).
6. **Emissão de Certificados de Cliente (mTLS):**
   - Emissão de certificados para os operadores: `joao@example.com`, `maria@example.com` e `antonio@example.com` (`extendedKeyUsage = clientAuth`).
   - Exportação para contêiner PKCS#12 (`.p12`) protegido por senha para importação em navegadores e ferramentas cliente (`openssl pkcs12 -export`).
7. **Instalação e Confiança nos Clientes:**
   - Instalação da Root CA no Debian via `/usr/local/share/ca-certificates/` e `update-ca-certificates`.
   - Configuração de confiança no Firefox e teste de clientes CLI com `curl --cacert`.
   - Comparativo direto com a diretiva `@cert-authority` do `known_hosts` do SSH.
8. **mTLS na Prática (Hands-on):**
   - Simulação de servidor mTLS com `openssl s_server -accept 8443 -cert ... -key ... -CAfile ca-chain.pem -Verify 2`.
   - Conexão autenticada mútua com `openssl s_client -cert joao.crt -key joao.key`.
   - Teste automatizado com `curl --cert joao.crt --key joao.key --cacert root.crt`.
   - Configuração de referência para Nginx (`ssl_verify_client on`) e autorização baseada em `$ssl_client_s_dn` (paralelo com `AuthorizedPrincipalsFile` do SSH).
9. **Cenários Reais de Quebra (Simulação de Erros):**
   - Erro 1: Cadeia incompleta (falta da intermediária pelo servidor).
   - Erro 2: Hostname mismatch (acesso a nome ausente no SAN com `-verify_hostname`).
   - Erro 3: Inversão de papéis de EKU (usar certificado de cliente como servidor e vice-versa).
   - Erro 4: Violação de `nameConstraints` (tentativa da intermediária emitir para `malicious.org`).
   - Erro 5: Certificado expirado (simulação temporal com `-attime`).
   - Erro 6: Antônio tentando conexão mTLS com certificado emitido por CA não autorizada (autoassinado).
   - Tabela diagnóstica completa: Código de erro do OpenSSL -> Causa raiz -> Solução.
10. **Diagnóstico e Troubleshooting:**
    - Verificação de cadeias com `openssl verify -show_chain -CAfile ... -untrusted ...`.
    - Comparação determinística de par de chaves: SHA-256 do módulo/chave pública do CSR, chave privada e certificado.
11. **Exercícios:**
    - 5 exercícios práticos de emissão com validade curta (estilo `-V +1d`), testes de limite de `pathlen` e validação de restrições.
12. **Conclusão:**
    - Fechamento com o gancho: "O Antônio vazou seu certificado de cliente. Como revogamos esse acesso sem derrubar a PKI?".
13. **Referências.**

---

## Parte 3 — Operação: Revogação, Rotação, Transparência e o Pós-Quântico

- **Arquivo:** `_posts/2026/11/2026-11-21-pki-operacao.md`
- **Permalink:** `/posts/pki-operacao/`
- **Data:** `2026-11-21 10:00:00 GMT-3`
- **Título:** "PKI com OpenSSL, Parte 3 - Operação: Revogação, Rotação, Transparência e o Pós-Quântico"
- **Subtitle:** "Emitir é fácil; o difícil é desfazer, trocar e provar que ninguém emitiu escondido"
- **Categoria:** `Tutoriais`
- **Tags:** `[Criptografia, Segurança, PKI, OpenSSL]`
- **Mermaid:** `true`
- **Objetivo Técnico:** O leitor domina os ciclos de vida operacionais de uma PKI: revogação via CRL e OCSP, transição para validade ultracurta, automação com ACME, rotação com cross-signing, monitoramento com Certificate Transparency e preparação para criptografia pós-quântica (PQC) com OpenSSL 3.5.
- **Referências Indicadas:** R03, R04, R05, R06, R14, R15, R16, R17, R18, R19, R23, R24, R26, R27, R28, R29, R30, R34, R35, R36, R37, R38, R46, R47, R48, R49, R60, R61, R70, R73, R80, R81.

### Estrutura de Seções:
1. **Introdução:**
   - O incidente fictício: Antônio comprometeu sua chave privada.
   - O contraste entre revogação no SSH (KRL estático e enxuto) e o desafio distribuído da revogação em PKI X.509.
2. **Listas de Revogação de Certificados (CRL):**
   - Revogação formal com `openssl ca -revoke` com justificativa `-crl_reason keyCompromise`.
   - Geração e publicação de CRL com `openssl ca -gencrl`.
   - Inspeção de CRL (`openssl crl -text -noout`).
   - A extensão `cRLDistributionPoints` nos certificados.
   - Verificação com checagem de CRL ativa via `openssl verify -crl_check`.
   - Limitações clássicas de CRL: tamanho crescente, latência de download e janela de vulnerabilidade.
3. **Online Certificate Status Protocol (OCSP):**
   - Criação de certificado de responder OCSP dedicado (`extendedKeyUsage = OCSPSigning`, `noCheck`).
   - Execução do responder OCSP nativo com `openssl ocsp -index index.txt -port 2560 ...`.
   - Consulta e validação de clientes com `openssl ocsp -issuer ... -cert ... -url ... -resp_text`.
   - OCSP Stapling no TLS e verificação com `openssl s_client -status`.
   - O declínio do OCSP: vazamento de privacidade do usuário, disponibilidade como vetor de DoS (soft-fail nos navegadores), Ballot SC-063 do CA/B Forum e encerramento do serviço OCSP pelo Let's Encrypt em agosto de 2025.
   - Estratégias modernas dos navegadores: CRLSets e CRLite. Recomendação para PKI privada: CRL bem dimensionada + validade curta.
4. **Validade Curta como a Melhor Forma de Revogação:**
   - O cronograma de redução de validade do CA/B Forum (Ballot SC081v3: transição para 200 dias em 2026, 100 dias em 2027 e 47 dias em 2029; reuso de DCV caindo para 10 dias).
   - Paralelo com os certificados temporários do SSH (`-V +12w`) e a validade de 30 dias adotada no laboratório do k8sbox.
   - Conclusão inevitável: a gestão manual de certificados tornou-se operacionalmente inviável.
5. **Automação de Ciclo de Vida: O Protocolo ACME:**
   - Arquitetura da RFC 8555: validação de controle por desafios `HTTP-01` e `DNS-01`.
   - Clientes de automação (`certbot`, `lego`).
   - ACME em redes privadas: servidores internos (step-ca) para emissão automatizada de certificados corporativos.
6. **Estratégias de Rotação de Chaves e Certificados:**
   - Rotação de certificados de folha (trivial via ACME).
   - Rotação de CAs intermediárias (janela de sobreposição / overlap com duas intermediárias ativas simultaneamente).
   - Rotação de CAs Raiz: o desafio das trust stores legadas.
   - Mecanismo de *Cross-Signing*: análise histórica da expiração da DST Root CA X3 e a transição da ISRG Root X1 do Let's Encrypt em setembro de 2021.
   - Demonstração prática no OpenSSL: assinatura cruzada de uma nova raiz.
7. **Certificate Transparency (CT): Provas Criptográficas Públicas:**
   - Contexto histórico: incidentes DigiNotar (2011) e Symantec (2017-2018).
   - Estrutura de logs públicos append-only baseados em árvores de Merkle.
   - Signed Certificate Timestamps (SCTs) embutidos via extensão X.509 ou handshake TLS.
   - Pré-certificados e a extensão de envenenamento (*poison extension*).
   - Monitoramento ativo de domínios corporativos com `crt.sh`.
   - Paralelo: CT como auditoria pública global vs a teia social do PGP.
8. **Proteção Física e Lógica das Chaves da CA:**
   - Módulos de Segurança de Hardware (HSM) e especificação PKCS#11.
   - Integração com OpenSSL 3 através do `pkcs11-provider`.
   - Uso prático de YubiKey PIV para chaves de CAs intermediárias.
   - Boas práticas de cerimônia e guarda da chave privada da Root offline.
9. **Superfície de Ataque e Vulnerabilidades em Parsers ASN.1:**
   - Análise de vulnerabilidade: CVE-2022-3602 e CVE-2022-3786 (buffer overflows no parser de punycode ao processar restrições de nomes de email `nameConstraints` no OpenSSL 3.0.0 a 3.0.6).
   - Lições arquiteturais: a complexidade intrínseca do ASN.1 como vetor de risco constante.
10. **A Era da Criptografia Pós-Quântica (PQC):**
    - Suporte no OpenSSL 3.5 LTS: FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) e FIPS 205 (SLH-DSA).
    - O cenário "Harvest Now, Decrypt Later" e a adoção do algoritmo híbrido `X25519MLKEM768` como padrão no TLS 1.3.
    - O desafio dos certificados de assinatura pós-quânticos: overhead de tamanho de chaves e assinaturas ML-DSA comparados a ECDSA.
    - Demonstração prática no OpenSSL 3.5.7:
      - Listagem de algoritmos pós-quânticos disponíveis.
      - Geração de par de chaves e certificados raiz/folha com ML-DSA-65.
      - Comparativo quantitativo de bytes entre certificados ECDSA P-384 e ML-DSA.
11. **Ponte para a Série OpenPGP:**
    - O utilitário `gpgsm`: o lado X.509 do ecossistema GnuPG.
    - Importação e validação da nossa CA do laboratório no chaveiro do `gpgsm`.
    - Contraste final de modelos de confiança: autoridade hierárquica centralizada (X.509) versus reputação entre pares (OpenPGP).
12. **Diagnóstico e Troubleshooting Operacional:**
    - Comandos de validação de revogação, OCSP, conferência de SCTs e handshake TLS com grupos PQC híbridos.
13. **Exercícios:**
    - 5 exercícios de fixação: revogação do Antônio com teste de recusa mTLS, simulação de responder OCSP local, overlap de CAs intermediárias, consulta a logs de CT e negociação pós-quântica local.
14. **Conclusão:**
    - Fechamento da trilogia OpenSSL e apresentação da Parte 4 (CFSSL: Automação Declarativa).
15. **Referências.**

---

## Parte 4 (Futura) — PKI com CFSSL: Automação Declarativa e API

- **Arquivo Previsto:** `_posts/2026/12/2026-12-05-pki-automacao-cfssl.md`
- **Título Provisório:** "PKI com CFSSL, Parte 4 - Automação Declarativa e API"
- **Subtitle:** "Adeus arquivos INI: construindo CAs com JSON, profiles e assinatura via REST API"
- **Tema:** Transição do OpenSSL para CFSSL, JSON profiles (`ca-config.json`, `ca-csr.json`), modo daemon (`cfssl serve`), integração com CI/CD e Kubernetes, e `cfssl bundle`.

---

## Parte 5 (Futura) — OpenPGP e GnuPG: A Teia de Confiança

- **Arquivo Previsto:** `_posts/2026/12/2026-12-19-openpgp-gnupg-teia-confianca.md`
- **Título Provisório:** "OpenPGP e GnuPG, Parte 5 - A Teia de Confiança Descentralizada"
- **Tema:** Modelo de confiança peer-to-peer sem CAs, assinatura de chaves, ownertrust vs validity, subchaves offline, keyservers verificantes (WKD/keys.openpgp.org), YubiKey OpenPGP e assinatura digital de código.
