---
name: mente-latente-series
description: >
  Convenções, princípios pedagógicos ("Castelo de Tijolos") e roteiro da série "Mente Latente" (41 capítulos de ML com PyTorch) no blog vndmtrx.github.io. Ative ao escrever, rascunhar, planejar ou revisar posts desta série.
---

# Skill: Série Mente Latente

Herda integralmente voz, antipadrões, ritmo, invariantes e validação (`scripts/lint_post.py`) de [blog-posts](../blog-posts/SKILL.md).

---

## 1. Convenções da Série

- **Front Matter Obrigatório:**
  ```yaml
  category: Tutoriais
  series: Mente Latente
  title: "ML :: [Título do Post]"
  subtitle: "[Tagline técnica marcante]"
  tags: [TagEspecifica1, TagEspecifica2, Machine Learning, Inteligência Artificial]
  math: true # Sempre que houver fórmulas KaTeX
  mermaid: true # Sempre que houver diagramas Mermaid
  ```
- **Trilha e Repositório:** Página em `tutoriais/mente-latente.md` (`/tutoriais/mente-latente/`), metadados em `_data/series.yml` e repositório parceiro [vndmtrx/mente_latente](https://github.com/vndmtrx/mente_latente), onde cada post é um módulo Python importável (`cap_01_introducao/`, `cap_02_tensores_basico/`, ...).
- **Callout de Abertura (na introdução, sempre APÓS o 1º parágrafo para não poluir o `post.excerpt` do Jekyll, e antes do primeiro `##`):**
  ```markdown
  > [!NOTE] Nota da Série
  > Este post faz parte da série **Mente Latente**, onde construímos Aprendizado de Máquina tijolo por tijolo com **PyTorch**, dos primeiros tensores e do Perceptron até Transformers. Os notebooks de exploração, módulos reutilizáveis e testes `pytest` de cada capítulo estão no repositório parceiro [vndmtrx/mente_latente](https://github.com/vndmtrx/mente_latente).
  ```
- **Override de Exercícios (Obrigatório):** Todo post exige `## Exercícios` focado em exploração prática de parâmetros e experimentos no Jupyter (variar `eta`, trocar ativações, testar limites), seguindo [formatacao-avancada.md](../blog-posts/references/formatacao-avancada.md).
- **Diagramas Mermaid:** Seguir [formatacao-avancada.md](../blog-posts/references/formatacao-avancada.md).
- **Meta de Extensão:** Média de **2.500 a 3.500 palavras** por post, calibrada pela densidade do capítulo.

---

## 2. Princípios Pedagógicos ("Castelo de Tijolos")

1. **Construcionismo (Construir -> Quebrar -> Consertar -> Construir):** Use o Jupyter Notebook e o módulo PyTorch como "objeto para pensar com". Construa uma peça funcional, quebre-a intencionalmente nos testes de limite e exercícios (ex.: subir `eta` até divergir, remover não linearidade no XOR, provocar *data leakage*), diagnostique pelo *debugging* e consolide um tijolo mais sólido.
2. **Zero Saltos Mágicos:** Nunca pule simplificações algébricas ou idiomatismos como se fossem óbvios. Toda compressão (absorver o bias como $w_0 \cdot 1$, usar $X W^T$, `log-sum-exp`, `/ sqrt(d_k)` ou reparametrização) deve ser aberta passo a passo no Jupyter antes da forma compacta.
3. **Um Problema por Post:** Não misture conceitos grandes (Softmax e Gradiente Descendente têm posts próprios). Priorize **o porquê da tecnologia** sobre dedução formal de livro-texto; matemática entra apenas quando destrava a implementação em PyTorch.
4. **Imutabilidade dos Tijolos Assentados:** Módulos de capítulos já publicados (`cap_XX_...`) são estáveis. Não quebre assinaturas antigas retroativamente; versões evoluídas nascem no capítulo novo.
5. **Fluxo Jupyter -> Módulo -> `pytest`:** Experimente célula a célula em `exploracao.ipynb`, consolide em `codigo.py` (exposto via `__init__.py` para importação nos capítulos seguintes) e valide invariantes e shapes em `test_cap_XX.py` via `pytest`.

---

## 3. Roteiro sob Demanda

O roteiro completo (7 fases, 41 capítulos) está em [references/roteiro.md](references/roteiro.md).

> [!TIP] Eficiência de Tokens e Anti-Bleed
> **Não leia o roteiro inteiro.** Inspecione apenas o intervalo de linhas do Capítulo X em `references/roteiro.md` e transforme os tópicos do roteiro em prosa natural (sem copiar listas simétricas para o post).
