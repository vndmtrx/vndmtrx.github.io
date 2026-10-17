# Catálogo de Referências Canônicas: Criptografia na Prática

Legenda de status:
- ✅ **Verificada**: URL testada, ativa e acessível.
- 📚 **Canônica**: Padrão de URL estável de RFC, man page ou documentação oficial de longo prazo.
- ⚠️ **Atenção**: Confirmar URL, numeração ou draft exato no momento da citação.

---

## 1. Normas e Especificações (IETF, ITU-T, NIST)

| ID | Referência | URL | Status | Partes |
|---|---|---|---|---|
| R01 | RFC 5280: Internet X.509 PKI Certificate and CRL Profile | https://datatracker.ietf.org/doc/html/rfc5280 | 📚 | 1, 2, 3 |
| R02 | ITU-T X.690: ASN.1 encoding rules (BER/CER/DER) | https://www.itu.int/rec/T-REC-X.690 | 📚 | 1 |
| R03 | RFC 6960: X.509 Internet PKI Online Certificate Status Protocol - OCSP | https://datatracker.ietf.org/doc/html/rfc6960 | 📚 | 3 |
| R04 | RFC 6962: Certificate Transparency | https://datatracker.ietf.org/doc/html/rfc6962 | 📚 | 3 |
| R05 | RFC 9162: Certificate Transparency v2.0 | https://datatracker.ietf.org/doc/html/rfc9162 | 📚 | 3 |
| R06 | RFC 8555: ACME Protocol | https://datatracker.ietf.org/doc/html/rfc8555 | 📚 | 3 |
| R07 | RFC 2986: PKCS #10 - Certification Request Syntax Specification | https://datatracker.ietf.org/doc/html/rfc2986 | 📚 | 1, 2 |
| R08 | RFC 7468: Textual Encodings of PKIX, PKCS, and CMS Structures (PEM) | https://datatracker.ietf.org/doc/html/rfc7468 | 📚 | 1 |
| R09 | RFC 5958: Asymmetric Key Packages (PKCS #8) | https://datatracker.ietf.org/doc/html/rfc5958 | 📚 | 1 |
| R10 | RFC 9525: Service Identity in TLS (substitui RFC 6125) | https://datatracker.ietf.org/doc/html/rfc9525 | 📚 | 1 |
| R11 | RFC 8410: Algorithm Identifiers for Ed25519, Ed448, X25519, X448 for X.509 | https://datatracker.ietf.org/doc/html/rfc8410 | 📚 | 1, 2 |
| R12 | RFC 3647: Internet X.509 PKI Certificate Policy and Certification Practices Framework | https://datatracker.ietf.org/doc/html/rfc3647 | 📚 | 1 |
| R13 | RFC 7292: PKCS #12 - Personal Information Exchange Syntax | https://datatracker.ietf.org/doc/html/rfc7292 | 📚 | 2 |
| R14 | RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3 | https://datatracker.ietf.org/doc/html/rfc8446 | 📚 | 2, 3 |
| R15 | NIST SP 800-57 Part 1 Rev. 5: Recommendation for Key Management | https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final | 📚 | 2, 3 |
| R16 | FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) | https://csrc.nist.gov/pubs/fips/203/final | 📚 | 3 |
| R17 | FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA) | https://csrc.nist.gov/pubs/fips/204/final | 📚 | 3 |
| R18 | FIPS 205: Stateless Hash-Based Digital Signature Standard (SLH-DSA) | https://csrc.nist.gov/pubs/fips/205/final | 📚 | 3 |
| R19 | IETF LAMPS: draft-ietf-lamps-dilithium-certificates (ML-DSA em X.509) | https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/ | ⚠️ | 3 |

---

## 2. Documentação Oficial do OpenSSL 3.5

| ID | Referência | URL | Status | Partes |
|---|---|---|---|---|
| R20 | OpenSSL: x509v3_config(5) | https://docs.openssl.org/3.5/man5/x509v3_config/ | ✅ | 1, 2 |
| R21 | OpenSSL: openssl-x509(1) | https://docs.openssl.org/3.5/man1/openssl-x509/ | 📚 | 1, 2 |
| R22 | OpenSSL: openssl-asn1parse(1) | https://docs.openssl.org/3.5/man1/openssl-asn1parse/ | 📚 | 1 |
| R23 | OpenSSL: openssl-s_client(1) | https://docs.openssl.org/3.5/man1/openssl-s_client/ | 📚 | 1, 2, 3 |
| R24 | OpenSSL: openssl-verification-options(1) / openssl-verify(1) | https://docs.openssl.org/3.5/man1/openssl-verification-options/ | 📚 | 1, 2, 3 |
| R25 | OpenSSL: openssl-req(1) | https://docs.openssl.org/3.5/man1/openssl-req/ | 📚 | 2 |
| R26 | OpenSSL: openssl-ca(1) | https://docs.openssl.org/3.5/man1/openssl-ca/ | 📚 | 2, 3 |
| R27 | OpenSSL: openssl-crl(1) | https://docs.openssl.org/3.5/man1/openssl-crl/ | 📚 | 3 |
| R28 | OpenSSL: openssl-ocsp(1) | https://docs.openssl.org/3.5/man1/openssl-ocsp/ | 📚 | 3 |
| R29 | OpenSSL 3.5 Final Release: Suporte PQC, X25519MLKEM768 padrão | https://openssl-library.org/post/2025-04-08-openssl-35-final-release/ | ✅ | 3 |
| R30 | OpenSSL: openssl-genpkey(1) / openssl-pkcs12(1) | https://docs.openssl.org/3.5/man1/openssl-genpkey/ | 📚 | 2, 3 |

---

## 3. Guias e Artigos Técnicos de Referência

| ID | Referência | URL | Status | Partes |
|---|---|---|---|---|
| R31 | Let's Encrypt: A Warm Welcome to ASN.1 and DER | https://letsencrypt.org/docs/a-warm-welcome-to-asn1-and-der/ | ✅ | 1 |
| R32 | Smallstep: Everything you should know about certificates and PKI | https://smallstep.com/blog/everything-pki/ | ✅ | 1, 2 |
| R33 | Peter Gutmann: X.509 Style Guide | https://www.cs.auckland.ac.nz/~pgut001/pubs/x509guide.txt | 📚 | 1 |
| R34 | Let's Encrypt: Ending OCSP Support in 2025 | https://letsencrypt.org/2024/12/05/ending-ocsp/ | ✅ | 3 |
| R35 | Let's Encrypt: OCSP Service Has Reached End of Life | https://letsencrypt.org/2025/08/06/ocsp-service-has-reached-end-of-life/ | ✅ | 3 |
| R36 | CA/B Forum Ballot SC081v3: Redução de validade e períodos de reuso de dados | https://cabforum.org/2025/04/11/ballot-sc081v3-introduce-schedule-of-reducing-validity-and-data-reuse-periods/ | ✅ | 3 |
| R37 | Let's Encrypt: DST Root CA X3 Expiration (Set/2021) | https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/ | 📚 | 3 |
| R38 | crt.sh: Certificate Search (Logs de Certificate Transparency) | https://crt.sh/ | 📚 | 3 |
| R40 | Let's Encrypt: Ending TLS Client Authentication Certificate Support | https://letsencrypt.org/2025/05/14/ending-tls-client-authentication/ | ✅ | 1, 2 |
| R41 | Jamie Nguyen: OpenSSL Certificate Authority | https://jamielinux.com/docs/openssl-certificate-authority/ | ✅ | 2 |
| R42 | Stefan H. Holek: OpenSSL PKI Tutorial v2.0 | https://pki-tutorial.readthedocs.io/en/latest/ | ✅ | 2 |
| R43 | Ivan Ristić: OpenSSL Cookbook (Feisty Duck) | https://www.feistyduck.com/library/openssl-cookbook/ | ⚠️ | 1, 2 |
| R44 | Debian Manpages: update-ca-certificates(8) | https://manpages.debian.org/trixie/ca-certificates/update-ca-certificates.8.en.html | ⚠️ | 2 |
| R45 | Kubernetes Documentation: PKI certificates and requirements | https://kubernetes.io/docs/setup/best-practices/certificates/ | 📚 | 2 |
| R46 | Mozilla Root Store Policy | https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/ | 📚 | 1, 3 |
| R47 | Chrome Root Program Policy | https://www.chromium.org/Home/chromium-security/root-ca-policy/ | 📚 | 1, 3 |
| R48 | Google Security Blog: Chrome's Plan to Distrust Symantec Certificates (2017) | https://security.googleblog.com/2017/09/chromes-plan-to-distrust-symantec.html | 📚 | 3 |
| R49 | CA/Browser Forum: Baseline Requirements for Server Certificates | https://cabforum.org/working-groups/server/baseline-requirements/documents/ | ⚠️ | 1, 3 |

---

## 4. Incidentes de Segurança e Casos Históricos

| ID | Referência | URL | Status | Partes |
|---|---|---|---|---|
| R60 | OpenSSL Security Advisory: CVE-2022-3602 / CVE-2022-3786 (NameConstraints Buffer Overflows) | https://openssl-library.org/news/secadv/20221101.txt | ✅ | 3 |
| R61 | Fox-IT / Incident DigiNotar: "Black Tulip" Report Summary | https://en.wikipedia.org/wiki/DigiNotar | ⚠️ | 1, 3 |
| R62 | Heartbleed Bug (CVE-2014-0160) | https://heartbleed.com/ | 📚 | 3 |

---

## 5. Pontes com SSH e OpenPGP

| ID | Referência | URL | Status | Partes |
|---|---|---|---|---|
| R70 | vndmtrx blog: OpenSSH na Prática, Parte 3 - Certificados SSH | {% raw %}{% include post-ref.html slug="certificados-ssh" %}{% endraw %} | ✅ | 1, 2, 3 |
| R71 | IETF draft-miller-ssh-cert: SSH Certificate Format | https://datatracker.ietf.org/doc/draft-miller-ssh-cert/ | ✅ | 1 |
| R72 | OpenBSD Manpages: ssh-keygen(1) (CERTIFICATES) | https://man.openbsd.org/ssh-keygen.1#CERTIFICATES | 📚 | 1 |
| R73 | vndmtrx blog: Gerenciando Chaves SSH e GPG para o GitHub | {% raw %}{% include post-ref.html slug="ssh-gpg-github" %}{% endraw %} | ✅ | 3, 4 |
| R80 | GnuPG Manual: Invoking GPGSM (X.509 / S/MIME) | https://www.gnupg.org/documentation/manuals/gnupg/Invoking-GPGSM.html | ✅ | 3, 4 |
| R81 | RFC 9580: OpenPGP | https://datatracker.ietf.org/doc/html/rfc9580 | 📚 | 1, 4 |
| R82 | The GNU Privacy Handbook | https://www.gnupg.org/gph/en/manual.html | 📚 | 4 |
| R83 | Robert J. Hansen: SKS Keyserver Network Under Attack (2019) | https://gist.github.com/rjhansen/67ab921ffb4084c865b3618d6955275f | ⚠️ | 4 |
| R84 | keys.openpgp.org: Sobre o Servidor de Chaves Verificante | https://keys.openpgp.org/about | 📚 | 4 |
