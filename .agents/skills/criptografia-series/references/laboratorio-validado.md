# Laboratório Validado: Arquitetura PKI com OpenSSL 3.5.7

Registro dos comandos executados, arquivos de configuração integrais e saídas reais de terminal coletadas no ambiente local (**OpenSSL 3.5.7**, Debian GNU/Linux, arquitetura x86_64).

> [!IMPORTANT] Fidelidade às Saídas Reais
> Qualquer redação dos posts da trilogia PKI (especialmente Parte 2 e Parte 3) **DEVE** utilizar exclusivamente os comandos, parâmetros e mensagens de erro deste documento. Não inventar ou alterar códigos numéricos de erro ou saídas de diagnóstico.

---

## 1. Arquivos de Configuração Completos

### `root.cnf` (Root CA — Offline, ECDSA P-384, Validade 10 Anos)

```ini
[ ca ]
default_ca = CA_default

[ CA_default ]
dir               = ./root
certs             = $dir/certs
crl_dir           = $dir/crl
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
RANDFILE          = $dir/private/.rand

private_key       = $dir/private/root.key
certificate       = $dir/certs/root.crt

crlnumber         = $dir/crlnumber
crl               = $dir/crl/root.crl
crl_extensions    = crl_ext
default_crl_days  = 30

default_md        = sha384
name_opt          = ca_default
cert_opt          = ca_default
default_days      = 3650
preserve          = no
policy            = policy_strict

[ policy_strict ]
countryName             = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[ req ]
default_bits        = 384
default_md          = sha384
string_mask         = utf8only
utf8                = yes
distinguished_name  = req_distinguished_name
prompt              = no

[ req_distinguished_name ]
countryName                     = BR
organizationName                = Example Corp
commonName                      = Example Root CA

[ v3_root_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[ v3_intermediate_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
nameConstraints = critical, permitted;DNS:.example.com, permitted;DNS:example.com, permitted;email:example.com, permitted;email:.example.com

[ crl_ext ]
authorityKeyIdentifier=keyid:always
```

### `intermediate.cnf` (Intermediate CA — Online, ECDSA P-384, Validade 3 Anos)

```ini
[ ca ]
default_ca = CA_default

[ CA_default ]
dir               = ./intermediate
certs             = $dir/certs
crl_dir           = $dir/crl
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
RANDFILE          = $dir/private/.rand

private_key       = $dir/private/intermediate.key
certificate       = $dir/certs/intermediate.crt

crlnumber         = $dir/crlnumber
crl               = $dir/crl/intermediate.crl
crl_extensions    = crl_ext
default_crl_days  = 30

default_md        = sha384
name_opt          = ca_default
cert_opt          = ca_default
default_days      = 90
preserve          = no
policy            = policy_loose
copy_extensions   = copy

[ policy_loose ]
countryName             = optional
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[ req ]
default_bits        = 384
default_md          = sha384
string_mask         = utf8only
utf8                = yes
distinguished_name  = req_distinguished_name
prompt              = no

[ req_distinguished_name ]
countryName                     = BR
organizationName                = Example Corp
commonName                      = Example Intermediate CA

[ server_cert ]
basicConstraints = critical, CA:FALSE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, digitalSignature
extendedKeyUsage = critical, serverAuth
crlDistributionPoints = URI:http://crl.example.com/intermediate.crl
authorityInfoAccess = OCSP;URI:http://ocsp.example.com:2560

[ client_cert ]
basicConstraints = critical, CA:FALSE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, digitalSignature
extendedKeyUsage = critical, clientAuth
crlDistributionPoints = URI:http://crl.example.com/intermediate.crl
authorityInfoAccess = OCSP;URI:http://ocsp.example.com:2560

[ ocsp_cert ]
basicConstraints = critical, CA:FALSE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, digitalSignature
extendedKeyUsage = critical, OCSPSigning
noCheck = yes

[ crl_ext ]
authorityKeyIdentifier=keyid:always
```

---

## 2. Passo a Passo Validado: Criação da Infraestrutura de CA

### 2.1 Estrutura de Diretórios e Base de Estado
```bash
mkdir -p root/certs root/crl root/newcerts root/private
mkdir -p intermediate/certs intermediate/crl intermediate/csr intermediate/newcerts intermediate/private
chmod 700 root/private intermediate/private

touch root/index.txt intermediate/index.txt
echo 1000 > root/serial
echo 2000 > intermediate/serial
echo 1000 > root/crlnumber
echo 2000 > intermediate/crlnumber
```

### 2.2 Geração e Emissão da Root CA (ECDSA P-384, SHA-384, 10 anos)
```bash
# Geração da chave privada cifrada com AES-256
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -aes-256-cbc \
    -out root/private/root.key -pass pass:rootsecret

# Emissão do certificado autoassinado raiz
openssl req -config root.cnf -key root/private/root.key -new -x509 -days 3650 -sha384 \
    -extensions v3_root_ca -out root/certs/root.crt \
    -subj '/C=BR/O=Example Corp/CN=Example Root CA' -passin pass:rootsecret
```

**Saída de inspeção (`openssl x509 -in root/certs/root.crt -noout -text`):**
```text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            55:51:f4:60:a3:c9:d8:99:8e:77:14:40:58:50:93:cb:6d:01:1e:63
        Signature Algorithm: ecdsa-with-SHA384
        Issuer: C=BR, O=Example Corp, CN=Example Root CA
        Validity
            Not Before: Oct 17 20:14:16 2026 GMT
            Not After : Oct 14 20:14:16 2036 GMT
        Subject: C=BR, O=Example Corp, CN=Example Root CA
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (384 bit)
                pub:
                    04:b4:c7:21:8b:f4:4a:1e:fa:78:11:d5:91:68:07:
                    0f:31:23:e7:70:0e:91:5b:2e:e4:1e:cf:68:d7:6d:
                    58:64:19:ee:4b:f9:2a:0c:68:64:89:2a:00:e8:d2:
                    80:ea:b0:d7:9b:fa:43:b7:58:95:5a:8a:95:7e:58:
                    2f:1b:26:b5:9e:f2:a7:5f:c2:85:06:5d:ed:d8:38:
                    d5:8c:83:7d:e5:d4:68:59:4c:48:38:13:49:72:c7:
                    f9:f7:f9:b6:a8:e0:5d
                ASN1 OID: secp384r1
                NIST CURVE: P-384
        X509v3 extensions:
            X509v3 Subject Key Identifier: 
                B9:B2:52:84:AA:AB:FF:A2:B1:08:46:D1:43:67:3A:F1:3C:AF:4D:07
            X509v3 Authority Key Identifier: 
                B9:B2:52:84:AA:AB:FF:A2:B1:08:46:D1:43:67:3A:F1:3C:AF:4D:07
            X509v3 Basic Constraints: critical
                CA:TRUE
            X509v3 Key Usage: critical
                Digital Signature, Certificate Sign, CRL Sign
    Signature Algorithm: ecdsa-with-SHA384
```

### 2.3 Geração e Emissão da Intermediate CA (ECDSA P-384, pathlen:0, nameConstraints)
```bash
# Geração da chave intermediária
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-384 -aes-256-cbc \
    -out intermediate/private/intermediate.key -pass pass:intsecret

# Geração do CSR
openssl req -config intermediate.cnf -new -sha384 -key intermediate/private/intermediate.key \
    -out intermediate/csr/intermediate.csr \
    -subj '/C=BR/O=Example Corp/CN=Example Intermediate CA' -passin pass:intsecret

# Assinatura pela Root CA aplicando restrições v3_intermediate_ca
openssl ca -config root.cnf -extensions v3_intermediate_ca -days 1095 -notext -md sha384 \
    -in intermediate/csr/intermediate.csr -out intermediate/certs/intermediate.crt \
    -batch -passin pass:rootsecret

# Montagem do bundle de cadeia
cat intermediate/certs/intermediate.crt root/certs/root.crt > intermediate/certs/ca-chain.pem
```

**Inspeção das extensões da Intermediate CA:**
```text
X509v3 extensions:
    X509v3 Subject Key Identifier: 
        15:D3:66:1C:FC:6F:F7:22:16:C6:90:41:29:A0:02:E7:E4:AB:00:06
    X509v3 Authority Key Identifier: 
        B9:B2:52:84:AA:AB:FF:A2:B1:08:46:D1:43:67:3A:F1:3C:AF:4D:07
    X509v3 Basic Constraints: critical
        CA:TRUE, pathlen:0
    X509v3 Key Usage: critical
        Digital Signature, Certificate Sign, CRL Sign
    X509v3 Name Constraints: critical
        Permitted:
          DNS:.example.com
          DNS:example.com
          email:example.com
          email:.example.com
```

---

## 3. Emissão de Folhas (Servidores e Clientes mTLS)

### 3.1 Servidor `php-01.example.com`
```bash
# Chave ECDSA P-256
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out intermediate/private/php-01.key

# CSR com SAN (DNS e IP)
openssl req -new -key intermediate/private/php-01.key -out intermediate/csr/php-01.csr \
    -subj '/C=BR/O=Example Corp/CN=php-01.example.com' \
    -addext 'subjectAltName = DNS:php-01.example.com, IP:10.0.0.10'

# Emissão com perfil server_cert
openssl ca -config intermediate.cnf -extensions server_cert -days 90 -notext -md sha384 \
    -in intermediate/csr/php-01.csr -out intermediate/certs/php-01.crt -batch -passin pass:intsecret
```

**Inspeção de extensões do `php-01`:**
```text
X509v3 extensions:
    X509v3 Basic Constraints: critical
        CA:FALSE
    X509v3 Subject Key Identifier: 
        8A:73:90:74:95:9F:C9:80:61:A8:12:F6:41:FD:A5:6C:54:F3:D5:F1
    X509v3 Authority Key Identifier: 
        15:D3:66:1C:FC:6F:F7:22:16:C6:90:41:29:A0:02:E7:E4:AB:00:06
    X509v3 Key Usage: critical
        Digital Signature
    X509v3 Extended Key Usage: critical
        TLS Web Server Authentication
    X509v3 CRL Distribution Points: 
        Full Name:
          URI:http://crl.example.com/intermediate.crl
    Authority Information Access: 
        OCSP - URI:http://ocsp.example.com:2560
    X509v3 Subject Alternative Name: 
        DNS:php-01.example.com, IP Address:10.0.0.10
```

### 3.2 Clientes mTLS (`joao`, `maria`, `antonio`)
```bash
# João
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out intermediate/private/joao.key
openssl req -new -key intermediate/private/joao.key -out intermediate/csr/joao.csr \
    -subj '/C=BR/O=Example Corp/CN=joao' -addext 'subjectAltName = email:joao@example.com'
openssl ca -config intermediate.cnf -extensions client_cert -days 30 -notext -md sha384 \
    -in intermediate/csr/joao.csr -out intermediate/certs/joao.crt -batch -passin pass:intsecret

# Export PKCS#12 para João
openssl pkcs12 -export -out intermediate/certs/joao.p12 -inkey intermediate/private/joao.key \
    -in intermediate/certs/joao.crt -certfile intermediate/certs/ca-chain.pem -passout pass:joaosecret
```

---

## 4. Validação Bem-Sucedida de Cadeia

```bash
$ openssl verify -show_chain -CAfile root/certs/root.crt -untrusted intermediate/certs/intermediate.crt intermediate/certs/php-01.crt
```
```text
intermediate/certs/php-01.crt: OK
Chain:
depth=0: C=BR, O=Example Corp, CN=php-01.example.com (untrusted)
depth=1: C=BR, O=Example Corp, CN=Example Intermediate CA (untrusted)
depth=2: C=BR, O=Example Corp, CN=Example Root CA
```

```bash
$ openssl verify -CAfile root/certs/root.crt -untrusted intermediate/certs/intermediate.crt -verify_hostname php-01.example.com intermediate/certs/php-01.crt
intermediate/certs/php-01.crt: OK
```

```bash
$ openssl verify -CAfile root/certs/root.crt -untrusted intermediate/certs/intermediate.crt -verify_ip 10.0.0.10 intermediate/certs/php-01.crt
intermediate/certs/php-01.crt: OK
```

---

## 5. Tabela de Falhas Reais e Diagnósticos (OpenSSL Verify)

| Cenário de Teste | Comando Executado | Mensagem Real do OpenSSL | Código de Erro / Retorno |
|---|---|---|---|
| **Cadeia Incompleta** (sem a intermediária fornecida) | `openssl verify -CAfile root/certs/root.crt intermediate/certs/php-01.crt` | `error 20 at 0 depth lookup: unable to get local issuer certificate` | `20` (exit 2) |
| **Hostname Mismatch** | `openssl verify -CAfile root/certs/root.crt -untrusted intermediate/certs/intermediate.crt -verify_hostname evil.example.com intermediate/certs/php-01.crt` | `error 62 at 0 depth lookup: hostname mismatch` | `62` (exit 2) |
| **Inversão de Propósito** (usar cert clientAuth para validar serviço TLS) | `openssl verify -CAfile root/certs/root.crt -untrusted intermediate/certs/intermediate.crt -purpose sslserver intermediate/certs/joao.crt` | `error 26 at 0 depth lookup: unsuitable certificate purpose` | `26` (exit 2) |
| **Violação de `nameConstraints`** (intermediária tentando emitir para `evil.com`) | `openssl verify -CAfile root/certs/root.crt -untrusted intermediate/certs/intermediate.crt intermediate/certs/evil.crt` | `error 47 at 0 depth lookup: permitted subtree violation` | `47` (exit 2) |
| **Certificado Expirado** (avanço temporal simulado) | `openssl verify -CAfile root/certs/root.crt -untrusted intermediate/certs/intermediate.crt -attime 1850000000 intermediate/certs/php-01.crt` | `error 10 at 0 depth lookup: certificate has expired` | `10` (exit 2) |
| **Certificado Revogado via CRL** | `openssl verify -CAfile root/certs/root.crt -untrusted intermediate/certs/intermediate.crt -CRLfile intermediate/crl/intermediate.crl -crl_check intermediate/certs/antonio.crt` | `error 23 at 0 depth lookup: certificate revoked` | `23` (exit 2) |

---

## 6. Operação: Revogação, CRL e OCSP

### 6.1 Revogação do Antônio no Banco de Dados
```bash
$ openssl ca -config intermediate.cnf -revoke intermediate/certs/antonio.crt -crl_reason keyCompromise -passin pass:intsecret
Using configuration from intermediate.cnf
Revoking Certificate 2004.
Database updated
```

**Estado do `index.txt`:**
```text
V	270115201416Z		2000	unknown	/C=BR/O=Example Corp/CN=php-01.example.com
V	270115201416Z		2001	unknown	/C=BR/O=Example Corp/CN=db-01.example.com
V	261116201416Z		2002	unknown	/C=BR/O=Example Corp/CN=joao
V	261116201416Z		2003	unknown	/C=BR/O=Example Corp/CN=maria
R	261116201417Z	261017201417Z,keyCompromise	2004	unknown	/C=BR/O=Example Corp/CN=antonio
```

### 6.2 Geração e Inspeção de CRL
```bash
openssl ca -config intermediate.cnf -gencrl -out intermediate/crl/intermediate.crl -passin pass:intsecret
openssl crl -in intermediate/crl/intermediate.crl -text -noout
```

```text
Certificate Revocation List (CRL):
        Version 2 (0x1)
        Signature Algorithm: ecdsa-with-SHA384
        Issuer: C=BR, O=Example Corp, CN=Example Intermediate CA
        Last Update: Oct 17 20:14:17 2026 GMT
        Next Update: Nov 16 20:14:17 2026 GMT
        CRL extensions:
            X509v3 Authority Key Identifier: 
                15:D3:66:1C:FC:6F:F7:22:16:C6:90:41:29:A0:02:E7:E4:AB:00:06
            X509v3 CRL Number: 
                8192
Revoked Certificates:
    Serial Number: 2004
        Revocation Date: Oct 17 20:14:17 2026 GMT
        CRL entry extensions:
            X509v3 CRL Reason Code: 
                Key Compromise
```

### 6.3 Responder OCSP Local
```bash
# Geração do responder
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out intermediate/private/ocsp.key
openssl req -new -key intermediate/private/ocsp.key -out intermediate/csr/ocsp.csr \
    -subj '/C=BR/O=Example Corp/CN=Example OCSP Responder'
openssl ca -config intermediate.cnf -extensions ocsp_cert -days 365 -notext -md sha384 \
    -in intermediate/csr/ocsp.csr -out intermediate/certs/ocsp.crt -batch -passin pass:intsecret

# Consulta para o João (Válido)
openssl ocsp -issuer intermediate/certs/intermediate.crt -cert intermediate/certs/joao.crt -reqout joao_ocsp_req.bin
openssl ocsp -index intermediate/index.txt -CA intermediate/certs/ca-chain.pem \
    -rsigner intermediate/certs/ocsp.crt -rkey intermediate/private/ocsp.key \
    -reqin joao_ocsp_req.bin -resp_text | grep -A 3 'Cert Status:'
```
```text
    Cert Status: good
    This Update: Oct 17 20:14:17 2026 GMT
```

```bash
# Consulta para o Antônio (Revogado)
openssl ocsp -issuer intermediate/certs/intermediate.crt -cert intermediate/certs/antonio.crt -reqout antonio_ocsp_req.bin
openssl ocsp -index intermediate/index.txt -CA intermediate/certs/ca-chain.pem \
    -rsigner intermediate/certs/ocsp.crt -rkey intermediate/private/ocsp.key \
    -reqin antonio_ocsp_req.bin -resp_text | grep -A 4 'Cert Status:'
```
```text
    Cert Status: revoked
    Revocation Time: Oct 17 20:14:17 2026 GMT
    Revocation Reason: keyCompromise (0x1)
    This Update: Oct 17 20:14:17 2026 GMT
```

---

## 7. Criptografia Pós-Quântica (PQC) no OpenSSL 3.5.7

### 7.1 Algoritmos de Assinatura Disponíveis
```bash
$ openssl list -signature-algorithms | grep -E 'ML-DSA|SLH-DSA'
```
```text
  { 2.16.840.1.101.3.4.3.17, id-ml-dsa-44, ML-DSA-44, MLDSA44 } @ default
  { 2.16.840.1.101.3.4.3.18, id-ml-dsa-65, ML-DSA-65, MLDSA65 } @ default
  { 2.16.840.1.101.3.4.3.19, id-ml-dsa-87, ML-DSA-87, MLDSA87 } @ default
  { 2.16.840.1.101.3.4.3.20, id-slh-dsa-sha2-128s, SLH-DSA-SHA2-128s } @ default
  { 2.16.840.1.101.3.4.3.21, id-slh-dsa-sha2-128f, SLH-DSA-SHA2-128f } @ default
  { 2.16.840.1.101.3.4.3.22, id-slh-dsa-sha2-192s, SLH-DSA-SHA2-192s } @ default
  { 2.16.840.1.101.3.4.3.23, id-slh-dsa-sha2-192f, SLH-DSA-SHA2-192f } @ default
  { 2.16.840.1.101.3.4.3.24, id-slh-dsa-sha2-256s, SLH-DSA-SHA2-256s } @ default
  { 2.16.840.1.101.3.4.3.25, id-slh-dsa-sha2-256f, SLH-DSA-SHA2-256f } @ default
  { 2.16.840.1.101.3.4.3.26, id-slh-dsa-shake-128s, SLH-DSA-SHAKE-128s } @ default
  { 2.16.840.1.101.3.4.3.27, id-slh-dsa-shake-128f, SLH-DSA-SHAKE-128f } @ default
  { 2.16.840.1.101.3.4.3.28, id-slh-dsa-shake-192s, SLH-DSA-SHAKE-192s } @ default
  { 2.16.840.1.101.3.4.3.29, id-slh-dsa-shake-192f, SLH-DSA-SHAKE-192f } @ default
  { 2.16.840.1.101.3.4.3.30, id-slh-dsa-shake-256s, SLH-DSA-SHAKE-256s } @ default
  { 2.16.840.1.101.3.4.3.31, id-slh-dsa-shake-256f, SLH-DSA-SHAKE-256f } @ default
```

### 7.2 Emissão com ML-DSA-65 (FIPS 204)
```bash
openssl genpkey -algorithm ML-DSA-65 -out pqc/mldsa65_root.key
openssl req -new -x509 -key pqc/mldsa65_root.key -out pqc/mldsa65_root.crt -days 3650 \
    -subj '/C=BR/O=Example Corp/CN=Example PQC Root CA'
```

### 7.3 Discrepância de Tamanho (O Desafio Operacional do PQC)
Comparativo real gerado por `ls -l`:

```text
7643 bytes - pqc/mldsa65_root.crt
5604 bytes - pqc/mldsa65_root.key
 794 bytes - root/certs/root.crt
 477 bytes - root/private/root.key
```

- **Chave Privada:** 477 bytes (ECDSA P-384) vs 5.604 bytes (ML-DSA-65) -> **~11,7x maior**
- **Certificado X.509:** 794 bytes (ECDSA P-384) vs 7.643 bytes (ML-DSA-65) -> **~9,6x maior**

### 7.4 Grupos KEM Híbridos Suportados no TLS 1.3
```bash
$ openssl list -kem-algorithms | grep -E 'ML-KEM|MLKEM'
```
```text
  { 2.16.840.1.101.3.4.4.1, id-alg-ml-kem-512, ML-KEM-512, MLKEM512 } @ default
  { 2.16.840.1.101.3.4.4.2, id-alg-ml-kem-768, ML-KEM-768, MLKEM768 } @ default
  { 2.16.840.1.101.3.4.4.3, id-alg-ml-kem-1024, ML-KEM-1024, MLKEM1024 } @ default
  X25519MLKEM768 @ default
  X448MLKEM1024 @ default
  SecP256r1MLKEM768 @ default
  SecP384r1MLKEM1024 @ default
```
