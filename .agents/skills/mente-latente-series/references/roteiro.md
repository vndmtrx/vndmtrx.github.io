# Roteiro — Série Mente Latente (98 Capítulos + 9 Extras)

## Objetivo e Setup Geral da Série

A série **Mente Latente** existe para construir, de forma lenta, orgânica e sem saltos mágicos, o entendimento prático do **Aprendizado de Máquina e da Inteligência Artificial moderna usando PyTorch** — dos primeiros tensores e do Perceptron de Rosenblatt até CNNs, Modelos Generativos, Aprendizado por Reforço, Modelos Fundacionais e nossa própria Mini-LLM.

Em vez de focar em deduções matemáticas formais de livro-texto, o enfoque matemático puro é deixado de lado em prol do **aprendizado por experimentação**: o objetivo é entender o problema que cada tecnologia resolve, abrir as simplificações práticas antes de compactá-las e seguir o construcionismo de Seymour Papert (*Construir -> Quebrar -> Consertar -> Construir*). A matemática formal aparece apenas quando estritamente necessária para destravar o código ou indicada em referências para aprofundamento.

Cada capítulo é um módulo Python importável (`cap_XX_<nome>/`) contendo `exploracao.ipynb` (bancada interativa no Jupyter), `codigo.py` + `__init__.py` (tijolos reutilizáveis pelos capítulos seguintes) e `test_cap_XX.py` (validação via `pytest`), além de exercícios práticos de exploração de parâmetros.

---

## Post 0 — Panorama Histórico

### Post 0 — A História do Aprendizado de Máquina (`_posts/2026/11/2026-11-25-ml-historia-aprendizado-de-maquina.md`)
- **Problema:** Dar contexto histórico progressivo antes da primeira linha de código, conectando cada onda e *breakthrough* às 13 Fases + 9 Extras da série.
- **Conteúdo:** 6 ondas cronológicas (1943 a 2026): do neurônio lógico de McCulloch & Pitts, Turing, Rosenblatt e Muro do XOR até Backpropagation, LeNet, RL (Sutton & Barto), AlexNet, Word2Vec, VAE, ResNet, Atenção, Transformers, Modelos Fundacionais, Difusão, RLHF, LoRA, Double Descent, Grokking, Mamba, SAEs e GRPO.

---

## Fase 1 — A Base Numérica (PyTorch como Motor Tensorial)

### Cap 01 — Introdução ao PyTorch, Laboratório e Hello World (`cap_01_introducao`)
- **Problema:** O que o PyTorch resolve e como montar uma bancada limpa e testável.
- **Conteúdo:** Papel do PyTorch, `matplotlib`, `numpy`, `jupyter` e `pytest`; escolha do `uv` como gerenciador de ambiente/dependências (orientando o leitor a instalá-lo no seu sistema/distro); apresentação da **imagem Docker oficial PyTorch + Jupyter pronta** (`quay.io/jupyter/pytorch-notebook:latest`) e passo a passo de como subir o laboratório com `docker compose up` / `docker run`; Hello World tensorial (CPU/GPU), primeiro gráfico e primeiro `pytest` verde.

### Cap 02 — Tensores no PyTorch: Criação, `shape` e `dtype` (`cap_02_tensores_basico`)
- **Problema:** Por que não usar apenas listas Python ou NumPy puro?
- **Conteúdo:** Tipos numéricos (`float32`, `int64`), dimensões (`ndim`, `shape`), criação (`tensor`, `zeros`, `randn`) e operações elementares.

### Cap 03 — Indexação, *Slicing* e *Broadcasting* (`cap_03_broadcasting`)
- **Problema:** Operar tensores de tamanhos diferentes sem escrever laços `for`.
- **Conteúdo:** Fatiamento, máscaras booleanas e regras de *broadcasting* abertas passo a passo no Jupyter (e armadilhas silenciosas).

### Cap 04 — Memória e Hardware: `view`, `reshape`, `contiguous` e GPU (`cap_04_memoria_hardware`)
- **Problema:** Entender quando uma operação copia memória ou só muda a "visão" dos dados.
- **Conteúdo:** `stride`, `view` vs `reshape`, `contiguous()`, movimentação `.to(device)` e benchmark simples CPU vs GPU.

---

## Fase 2 — Os Primórdios e o Aprendizado Linear

### Cap 05 — O Perceptron de Rosenblatt (`cap_05_perceptron`)
- **Problema:** Como ensinar uma máquina a traçar uma fronteira linear entre duas classes?
- **Conteúdo:** Função degrau (limiar), regra de atualização clássica em loop explícito e visualização da reta separadora 2D.

### Cap 06 — O Neurônio como Vetor e o Truque do $w_0$ (`cap_06_neuronio_vetor`)
- **Problema:** Sair de laços somando peso por peso para uma única operação vetorial.
- **Conteúdo:** Produto escalar (`torch.dot`) e absorção do *bias* como $w_0$ multiplicado por entrada fixa $x_0 = 1$, abrindo passo a passo antes de compactar.

### Cap 07 — Regressão Linear e MSE (`cap_07_regressao_mse`)
- **Problema:** Prever valores contínuos e medir o quão errado o modelo está.
- **Conteúdo:** Modelo linear contínuo, Erro Quadrático Médio (`mse_loss`) construído na mão e superfície de erro.

### Cap 08 — Gradiente Descendente (`cap_08_gradiente_descendente`)
- **Problema:** Como ajustar pesos automaticamente sem chutar na mão?
- **Conteúdo:** Analogia do sistema de freio/montanha, dedução empírica do passo crítico ($\eta > 1/2$ no caso quadrático), *overshoot* e regimes de convergência/oscilação/explosão.

### Cap 09 — Gradiente em Lotes: Batch, Stochastic e Mini-Batch (`cap_09_gradiente_lotes`)
- **Problema:** Calcular o gradiente no dataset inteiro de uma vez não escala.
- **Conteúdo:** Comparação prática entre Batch GD, SGD puro (1 exemplo) e Mini-Batch GD.

### Cap 10 — Probabilidade Mínima (MLE) (`cap_10_mle`)
- **Problema:** De onde vêm as fórmulas de perda?
- **Conteúdo:** Máxima Verossimilhança (MLE) sem formalismo pesado, mostrando por que MSE e Cross-Entropy nascem da mesma raiz probabilística.

### Cap 11 — Classificação Binária com Sigmoid e BCE (`cap_11_sigmoid_bce`)
- **Problema:** Transformar saída contínua em probabilidade $(0, 1)$ — e por que MSE falha na classificação.
- **Conteúdo:** Função Sigmoid e Entropia Cruzada Binária (`bce_loss`) implementadas do zero.

### Cap 12 — O Muro do XOR (`cap_12_muro_xor`)
- **Problema:** O limite histórico de Minsky & Papert (1969).
- **Conteúdo:** Tentando treinar modelos lineares na porta lógica XOR e provando visualmente que uma única reta nunca separa as classes.

---

## Fase 3 — Redes Neurais Clássicas (MLPs Rasas)

### Cap 13 — `torch.autograd` e o Grafo Computacional (`cap_13_autograd`)
- **Problema:** Calcular derivadas na mão para arquiteturas maiores não escala.
- **Conteúdo:** `requires_grad=True`, grafo dinâmico, `.backward()`, `.grad`, `zero_grad()` e `torch.no_grad()`.

### Cap 14 — Backpropagation por Dentro (`cap_14_backprop`)
- **Problema:** Desmistificar a "mágica" do `.backward()`.
- **Conteúdo:** Regra da cadeia manual (analogia das molas / Lei de Hooke) comparada lado a lado com `loss.backward()`.

### Cap 15 — Tanh e Saturação (`cap_15_tanh_saturacao`)
- **Problema:** Como melhorar a Sigmoid em camadas ocultas e onde ela ainda trava.
- **Conteúdo:** Tangente hiperbólica centrada em zero, demonstração prática de como a escala da entrada decide a saturação.

### Cap 16 — Camadas como Matrizes e Batches em Paralelo (`cap_16_camadas_matrizes`)
- **Problema:** Processar vários neurônios e vários exemplos simultaneamente.
- **Conteúdo:** Empilhando vetores em matriz $W$, o porquê explícito de $X W^T + b$ (`@`), *shapes* `(batch, features)` e retorno do `bias` separado.

### Cap 17 — A Primeira MLP: Quebrando o XOR (`cap_17_mlp_xor`)
- **Problema:** Atravessar o muro do Capítulo 12.
- **Conteúdo:** Juntando camadas lineares + Tanh + `autograd` para dobrar o espaço e resolver o XOR.

### Cap 18 — One-Hot Encoding vs Saída Escalar (`cap_18_one_hot`)
- **Problema:** A "falácia métrica" de tentar prever classes `0..9` com um único neurônio escalar.
- **Conteúdo:** Por que saída escalar assume que `9 > 1` e que a média entre `2` e `4` é `3`; formalização em $\mathbb{R}^K$.

### Cap 19 — Softmax e Cross-Entropy Multiclasse (`cap_19_softmax_ce`)
- **Problema:** Classificar $K$ classes sem explosão numérica.
- **Conteúdo:** De *logits* para probabilidades, truque `log-sum-exp`, eliminação do one-hot explícito e **a armadilha do Softmax duplo** (`F.softmax()` antes de `nn.CrossEntropyLoss()`).

### Cap 20 — `nn.Module`, `nn.Parameter` e o Muro da Profundidade (`cap_20_nn_module`)
- **Problema:** Organizar blocos reutilizáveis — e descobrir por que empilhar 10 camadas de Sigmoid/Tanh trava.
- **Conteúdo:** Anatomia de `nn.Module` e demonstração prática do *vanishing gradient* em redes fundas clássicas.

---

## Fase 4 — O Motor do Deep Learning

### Cap 21 — ReLU e *Dying ReLU* (`cap_21_relu`)
- **Problema:** Destravar o fluxo de gradiente em redes profundas.
- **Conteúdo:** ReLU do zero, diferença entre **neurônio morto (ReLU)** e **neurônio saturado (Sigmoid/Tanh)**, e colapso por *Dying ReLU* com $\eta$ alto.

### Cap 22 — GELU (`cap_22_gelu`)
- **Problema:** A ativação suave padrão em arquiteturas modernas.
- **Conteúdo:** Comparando ReLU vs GELU na prática.

### Cap 23 — Inicialização de Pesos: Xavier e Kaiming/He (`cap_23_inicializacao`)
- **Problema:** Redes profundas explodem ou morrem na época 0 se os pesos iniciais tiverem escala errada.
- **Conteúdo:** Variância das ativações camada a camada; Xavier/Glorot (Tanh) vs Kaiming/He (ReLU).

### Cap 24 — SGD com Momentum e Nesterov (`cap_24_momentum`)
- **Problema:** SGD puro oscila em vales estreitos e trava em platôs.
- **Conteúdo:** Inércia implementada manualmente e comparada com `torch.optim.SGD(..., momentum=0.9)`.

### Cap 25 — RMSProp (`cap_25_rmsprop`)
- **Problema:** Parâmetros diferentes precisam de passos de tamanhos diferentes.
- **Conteúdo:** Média móvel exponencial do quadrado dos gradientes.

### Cap 26 — Adam e AdamW (`cap_26_adamw`)
- **Problema:** Combinar inércia com adaptação por parâmetro sem quebrar a regularização.
- **Conteúdo:** Adam passo a passo e por que *weight decay* desacoplado (`AdamW`) venceu.

### Cap 27 — Learning Rate Schedulers (`cap_27_schedulers`)
- **Problema:** Um $\eta$ fixo é grande demais no começo ou no fim do treino.
- **Conteúdo:** *Warmup* linear e *Cosine Annealing* na prática.

### Cap 28 — Viés vs Variância e *Weight Decay* (`cap_28_weight_decay`)
- **Problema:** Quando a rede decora o treino em vez de generalizar.
- **Conteúdo:** Penalidade L2 (efeito mola puxando pesos para zero) e equilíbrio viés/variância.

### Cap 29 — Dropout (`cap_29_dropout`)
- **Problema:** Co-adaptação frágil entre neurônios.
- **Conteúdo:** Implementação manual com máscara Bernoulli + escalonamento invertido e diferença `.train()` vs `.eval()`.

---

## Fase 5 — Dados no Mundo Real, Rigor Experimental e Debugging

### Cap 30 — `Dataset` Customizado (`cap_30_dataset`)
- **Problema:** Padronizar o acesso a qualquer fonte de dados.
- **Conteúdo:** Protocolo `__len__` e `__getitem__`.

### Cap 31 — `DataLoader` e Gargalos de CPU (`cap_31_dataloader`)
- **Problema:** Carregar *mini-batches* sem transformar o disco/CPU no gargalo do treino.
- **Conteúdo:** `MiniDataLoader` didático, `shuffle`, `num_workers` e *profiling* real: `TensorDataset` em RAM vs leitura item a item.

### Cap 32 — Saneamento e Engenharia de Features (`cap_32_engenharia_features`)
- **Problema:** Dados reais vêm sujos e com variáveis cíclicas ou redundantes.
- **Conteúdo:** Lixo de sensor (`-9999` no Jena Climate), decomposição vetorial do vento ($\sin/\cos$) e seleção de features ortogonais pela Matriz de Correlação.

### Cap 33 — Normalização e *Data Leakage* (`cap_33_normalizacao_leakage`)
- **Problema:** Escalas diferentes distorcem o gradiente — mas normalizar errado invalida o experimento.
- **Conteúdo:** Min-Max vs Z-Score, cálculo estrito só no treino e significado físico de $\mu \approx 0.1307$ no MNIST.

### Cap 34 — Splits, *Lookahead Bias* e *Early Stopping* (`cap_34_splits_early_stopping`)
- **Problema:** Como saber se o modelo generaliza sem vazar informação do futuro ou do teste.
- **Conteúdo:** As 3 caixas (Treino/Validação/Teste), por que séries temporais proíbem `shuffle=True` (*lookahead bias*) e critério de parada (*Early Stopping*).

### Cap 35 — Métricas Além da Acurácia (`cap_35_metricas`)
- **Problema:** Acurácia alta engana em classes desbalanceadas; MSE e MAE têm físicas diferentes.
- **Conteúdo:** Matriz de Confusão, Precision, Recall, F1-Score, e MSE (média) vs MAE (mediana).

### Cap 36 — Validar Contra o Quê? Baselines e Filosofia (`cap_36_baselines`)
- **Problema:** "Validar o modelo" é vago se não há referência contra um chute ingênuo.
- **Conteúdo:** `DummyBaseline` (classe majoritária, aleatório, persistência em séries temporais) e a descoberta de que **menor *loss* vs maior acurácia muda o ranking**.

### Cap 37 — Debugging em PyTorch (`cap_37_debugging`)
- **Problema:** "Minha *loss* virou `NaN`, e agora?"
- **Conteúdo:** Checklist de caça a bugs: `zero_grad()` esquecido, `.eval()`, Softmax duplo, *shapes* silenciosos e inspeção com `torch.isnan`.

### Cap 38 — Checkpointing (`state_dict`) (`cap_38_checkpointing`)
- **Problema:** Salvar o melhor modelo e retomar treinos longos sem perder estado.
- **Conteúdo:** `state_dict` do modelo e do otimizador, `torch.save` e `torch.load`.

### Cap 39 — Reprodutibilidade e Diagnóstico (`cap_39_reprodutibilidade`)
- **Problema:** Experimentos que mudam a cada execução.
- **Conteúdo:** Fixando *seeds*, leitura de curvas de perda (*underfitting* vs *overfitting*).

### Cap 40 — Dados Tabulares e Desbalanceados (`cap_40_dados_tabulares`)
- **Problema:** Lidar com tabelas de escalas misturadas, valores faltantes e classes raras antes do treino.
- **Conteúdo:** Tensores `(N, features)`, análise de desbalanceamento e exploração de **Sintéticos 2D** + **Tabular desbalanceado**.

### Cap 41 — Dados de Imagem e Áudio como Espectrogramas (`cap_41_dados_imagem_audio`)
- **Problema:** Organizar canais, resoluções e transformar som em representação visual 2D.
- **Conteúdo:** Tensores `(N, C, H, W)`, `(H, W, C)` vs `(C, H, W)`, **MNIST**, **Fashion-MNIST**, **CIFAR-10**, **FER-2013**, **Oxford-IIIT Pets** e **SpeechCommands** (áudio como espectrograma).

### Cap 42 — Dados de Séries Temporais (`cap_42_dados_series`)
- **Problema:** Preservar a ordem cronológica e lidar com sujeira de sensores contínuos.
- **Conteúdo:** Tensores `(N, T, F)`, lixo de sensor (`-9999`), sazonalidade e *lookahead bias* no **Jena Climate**.

### Cap 43 — Dados de Texto (`cap_43_dados_texto`)
- **Problema:** Preparar sequências discretas de comprimentos variados e vocabulários desbalanceados.
- **Conteúdo:** Tensores `(N, T)`, limpeza de corpus, Lei de Zipf e exploração de **Machado de Assis / TinyStories**, **`dair-ai/emotion` / B2W Reviews** e pares **SFT/DPO**.

---

## Fase 6 — Visão Computacional (Evolução das CNNs)

### Cap 44 — O Limite da MLP em Imagens (`cap_44_mlp_mnist`)
- **Problema:** Achatar uma imagem 28×28 destrói a topologia espacial.
- **Conteúdo:** Experimento com MLP no MNIST, contagem de parâmetros e sensibilidade a deslocamentos.

### Cap 45 — Convolução 2D: Filtros e Bordas (`cap_45_conv2d`)
- **Problema:** Detectar padrões locais independentemente da posição.
- **Conteúdo:** Filtros deslizantes, *kernels* manuais de borda e visualização de mapas de características.

### Cap 46 — Stride, Padding e Canais 3D (`cap_46_stride_padding_canais`)
- **Problema:** Controlar dimensões espaciais e entender múltiplos canais.
- **Conteúdo:** Respondendo *"o filtro da 2ª camada não tem só 25 pesos?"* — geometria 3D de entrada/saída.

### Cap 47 — Pooling e LeNet no MNIST (`cap_47_lenet`)
- **Problema:** Reduzir dimensão espacial preservando informação relevante.
- **Conteúdo:** Respondendo *"MaxPool joga 75% dos dados no lixo?"* + confronto direto MLP vs LeNet no MNIST.

### Cap 48 — Blocos Profundos (estilo VGG) (`cap_48_vgg_blocos`)
- **Problema:** Empilhar filtros menores (3×3) para ganhar profundidade.
- **Conteúdo:** Arquitetura em blocos repetíveis e o reaparecimento da dificuldade de treinar muito fundo.

### Cap 49 — Data Augmentation em Visão (`cap_49_data_augmentation`)
- **Problema:** Aumentar robustez sem coletar novas imagens.
- **Conteúdo:** Rotações, recortes, espelhamento e cuidado com rótulos (ex.: `6` vs `9` no MNIST!).

### Cap 50 — Batch Normalization (`cap_50_batchnorm`)
- **Problema:** Ativações internas mudando de escala ao longo das camadas.
- **Conteúdo:** Normalização por *batch* (`gamma`, `beta`, `running_mean`, `running_var`) e `.train()` vs `.eval()`.

### Cap 51 — Conexões Residuais (ResNet) e Transfer Learning (`cap_51_resnet_transfer`)
- **Problema:** Por que empilhar mais camadas degrada até o erro de treino.
- **Conteúdo:** Atalho `x + F(x)` permitindo fluxo direto de gradiente + *fine-tuning* com `torchvision.models`.

---

## Fase 7 — Representação e Espaço Latente

### Cap 52 — Autoencoders: Comprimindo o Mundo (`cap_52_autoencoder`)
- **Problema:** Aprender representações compactas sem rótulos.
- **Conteúdo:** Encoder, gargalo (*bottleneck*) e Decoder reconstruindo o MNIST.

### Cap 53 — Denoising Autoencoders (`cap_53_denoising_ae`)
- **Problema:** Evitar que o Autoencoder aprenda apenas a copiar a entrada.
- **Conteúdo:** Injetando ruído na entrada e reconstruindo a imagem limpa.

### Cap 54 — Navegando e Visualizando o Espaço Latente (`cap_54_espaco_latente`)
- **Problema:** O que a rede realmente organizou dentro do gargalo?
- **Conteúdo:** Interpolação linear entre dígitos e projeção 2D de alta dimensão (PCA / t-SNE) para enxergar clusters.

### Cap 55 — Embeddings: Tabela de Consulta e Geometria (`cap_55_embeddings`)
- **Problema:** One-hot explode em vocabulários grandes e não mede similaridade.
- **Conteúdo:** `nn.Embedding` como tabela de consulta treinável e similaridade de cosseno.

### Cap 56 — Hipótese Distribucional e Word2Vec (`cap_56_word2vec`)
- **Problema:** Como vetores aprendem significado ("rei - homem + mulher ≈ rainha") sem um dicionário humano?
- **Conteúdo:** Skip-Gram na prática: aprendendo embeddings pelo contexto de vizinhança.

### Cap 57 — Embeddings Estáticos vs Contextuais (`cap_57_embeddings_contextuais`)
- **Problema:** `"banco"` (praça) e `"banco"` (dinheiro) têm o mesmo vetor em tabelas estáticas.
- **Conteúdo:** Limite do `nn.Embedding` isolado e a ponte para representações dependentes de contexto.

### Cap 58 — Aprendizado Contrastivo: Triplet Loss e InfoNCE (`cap_58_aprendizado_contrastivo`)
- **Problema:** Organizar o espaço latente aproximando pares semelhantes e afastando diferentes sem rótulos fixos.
- **Conteúdo:** *Triplet Loss* e *InfoNCE* em PyTorch (a base para reconhecimento facial e modelos multimodais).

---

## Fase 8 — Modelos Generativos

### Cap 59 — VAE (Parte 1): Espaço Probabilístico e KL-Divergence (`cap_59_vae_parte1`)
- **Problema:** Espaço latente com "buracos" não gera amostras novas válidas.
- **Conteúdo:** Mapeando para média $\mu$ e variância $\sigma^2$ + regularização pela *KL-Divergence*.

### Cap 60 — VAE (Parte 2): Reparametrização e Geração (`cap_60_vae_parte2`)
- **Problema:** Não dá para passar gradiente através de uma amostragem aleatória pura.
- **Conteúdo:** Truque da reparametrização aberto passo a passo e geração de dígitos inéditos no MNIST.

### Cap 61 — Difusão / DDPM (Parte 1): O Processo *Forward* (`cap_61_difusao_forward`)
- **Problema:** Como transformar geração de imagens em um problema de remoção gradual de ruído.
- **Conteúdo:** Cronograma de ruído (*noise schedule*) destruindo imagens passo a passo.

### Cap 62 — Difusão / DDPM (Parte 2): *Denoising* e Geração (`cap_62_difusao_reverse`)
- **Problema:** Reverter o ruído passo a passo para criar imagens do zero.
- **Conteúdo:** Rede prevendo o ruído adicionado e amostragem reversa no MNIST.

---

## Fase 9 — Sequências, Texto e Memória

### Cap 63 — Tokenização: Caractere, Palavra e Subpalavra (BPE) (`cap_63_tokenizacao`)
- **Problema:** Redes neurais não leem strings — leem inteiros.
- **Conteúdo:** Tokenizador por caractere, por palavra e implementação didática de *Byte Pair Encoding* (BPE).

### Cap 64 — Janelas Temporais no Jena Climate (`cap_64_janelas_temporais`)
- **Problema:** Transformar uma série contínua em pares entrada/alvo sem vazamento.
- **Conteúdo:** *Sliding windows*, *lookback* e horizonte de previsão $m$.

### Cap 65 — RNNs Simples e BPTT (`cap_65_rnn`)
- **Problema:** Modelos *feedforward* não têm memória do passo anterior.
- **Conteúdo:** Recorrência passo a passo (`h_t`) e *Backpropagation Through Time*.

### Cap 66 — *Vanishing/Exploding Gradients* e *Gradient Clipping* (`cap_66_gradient_clipping`)
- **Problema:** Por que a RNN simples esquece o início de sequências longas ou explode.
- **Conteúdo:** Experimento de decaimento do gradiente no tempo e `clip_grad_norm_`.

### Cap 67 — LSTMs: Portas de Memória (`cap_67_lstm`)
- **Problema:** Proteger informações relevantes ao longo de dezenas de passos.
- **Conteúdo:** Portões de esquecimento, entrada e saída implementados e inspecionados.

### Cap 68 — GRUs e RNNs Bidirecionais (`cap_68_gru_bidirecional`)
- **Problema:** Simplificar a LSTM — e encarar o gargalo sequencial que ainda sobra.
- **Conteúdo:** GRU, leitura nos dois sentidos e o limite de paralelização temporal.

---

## Fase 10 — Atenção e Arquitetura Transformer

### Cap 69 — Seq2Seq Clássico (`cap_69_seq2seq`)
- **Problema:** Comprimir uma sequência inteira em um único vetor final é um gargalo.
- **Conteúdo:** Encoder-Decoder recorrente e queda de qualidade em sequências longas.

### Cap 70 — Atenção como Busca Suave (Cross-Attention) (`cap_70_atencao_busca`)
- **Problema:** Permitir que o modelo consulte diretamente qualquer posição do passado.
- **Conteúdo:** Intuição de consulta suave em dicionário (Nadaraya-Watson / Bahdanau).

### Cap 71 — Similaridade Vetorial e Projeções `Q, K, V` (`cap_71_qkv_matematica`)
- **Problema:** Entender exatamente por que `Q @ K.T / sqrt(d_k)` funciona.
- **Conteúdo:** Produto escalar como alinhamento geométrico, projeções independentes e por que $\sqrt{d_k}$ evita saturação do `Softmax`.

### Cap 72 — Self-Attention em PyTorch Puro (`cap_72_self_attention`)
- **Problema:** Implementar a autoatenção linha a linha sem caixa preta.
- **Conteúdo:** Módulo `SelfAttention` do zero + visualização de mapas de calor de atenção.

### Cap 73 — Multi-Head Attention (`cap_73_multihead`)
- **Problema:** Uma única cabeça de atenção olha apenas um tipo de relação por vez.
- **Conteúdo:** Dividindo em múltiplas cabeças em paralelo e concatenando resultados.

### Cap 74 — Positional Encoding (`cap_74_positional_encoding`)
- **Problema:** Sem recorrência, a atenção é cega à ordem dos tokens.
- **Conteúdo:** A falácia do escalar 1D, a analogia do **Calendário Maia / engrenagens de frequências** (Senoidal), Aprendido e intuição de RoPE.

### Cap 75 — LayerNorm vs BatchNorm e FFN (`cap_75_layernorm_ffn`)
- **Problema:** Por que `BatchNorm` falha em sequências e qual o papel da FFN após a atenção.
- **Conteúdo:** Normalização por token (`LayerNorm`) e bloco *Feed-Forward*.

### Cap 76 — Transformer Encoder Completo no Jena Climate (`cap_76_transformer_encoder`)
- **Problema:** Previsão multivariada em série climática real.
- **Conteúdo:** Bloco Encoder completo, **Âncora Residual** (`x_ultimo + delta`) e estudo de **Interferência Negativa (*Negative Transfer*)** nos alvos.

---

## Fase 11 — Aprendizado por Reforço (Sutton & Barto em PyTorch)

### Cap 77 — Multi-Armed Bandits (`cap_77_bandits`)
- **Problema:** O dilema fundamental entre **Exploração vs Explotação**.
- **Conteúdo:** $\epsilon$-greedy e UCB em ambiente simples.

### Cap 78 — MDPs: Estados, Ações, Recompensas e $\gamma$ (`cap_78_mdp`)
- **Problema:** Quando cada ação muda o estado futuro do mundo.
- **Conteúdo:** Processos de Decisão de Markov, retorno descontado e função de valor.

### Cap 79 — Q-Learning Tabular (`cap_79_q_learning`)
- **Problema:** Aprender a agir otimamente sem conhecer as regras do ambiente.
- **Conteúdo:** Equação de Bellman na prática e tabela $Q(s, a)$ em ambiente discreto.

### Cap 80 — Deep Q-Networks / DQN (`cap_80_dqn`)
- **Problema:** Estados contínuos não cabem em uma tabela.
- **Conteúdo:** Rede neural em PyTorch aproximando $Q(s, a)$, *Experience Replay* e *Target Network*.

### Cap 81 — Policy Gradients / REINFORCE (`cap_81_reinforce`)
- **Problema:** Aprender diretamente uma política estocástica em espaços contínuos.
- **Conteúdo:** Gradiente da política com PyTorch e redução de variância com *baseline*.

### Cap 82 — Actor-Critic e PPO (`cap_82_ppo`)
- **Problema:** Estabilizar atualizações de política sem passos destrutivos.
- **Conteúdo:** Ator + Crítico e *clipping* de razão de probabilidades (a base usada no RLHF).

---

## Fase 12 — Modelos Fundacionais

### Cap 83 — O Paradigma Fundacional (`cap_83_paradigma_fundacional`)
- **Problema:** Sair de "1 modelo treinado do zero por tarefa" para "1 base geral adaptável".
- **Conteúdo:** Pré-treino em escala + adaptação *downstream*.

### Cap 84 — Pré-Treino Autossupervisionado (`cap_84_pretreino_ssl`)
- **Problema:** Aprender estrutura sem depender de rótulos humanos caros.
- **Conteúdo:** *Next-Token Prediction* (causal) vs *Masked Language Modeling* (estilo BERT).

### Cap 85 — Leis de Escala (*Scaling Laws*) e Emergência (`cap_85_scaling_laws`)
- **Problema:** Como prever o ganho de desempenho ao aumentar dados, parâmetros e computação.
- **Conteúdo:** Relação empírica de escala (Chinchilla) e capacidades que emergem com o tamanho.

### Cap 86 — Multimodalidade Fundacional / CLIP (`cap_86_clip`)
- **Problema:** Conectar visão e linguagem em um único espaço vetorial.
- **Conteúdo:** Perda contrastiva (*InfoNCE*) alinhando pares imagem-texto (conectando com o Cap 58).

---

## Fase 13 — LLMs, Fine-Tuning e a Fronteira Atual

### Cap 87 — Corpus de Linguagem, *Next-Token Prediction* e *Weight Tying* (`cap_87_next_token_corpus`)
- **Problema:** Preparar texto em blocos `(x, y)` deslocados para treinar um modelo de linguagem.
- **Conteúdo:** *Context length*, `x[1:]` como alvo e compartilhamento de pesos (*Weight Tying*) entre Embedding e saída.

### Cap 88 — Transformer Decoder (estilo GPT) e Máscara Causal (`cap_88_gpt_decoder`)
- **Problema:** Gerar texto token a token sem deixar o modelo espiar o futuro.
- **Conteúdo:** Máscara triangular inferior (`-inf` antes do `Softmax`) e arquitetura completa do nosso MiniGPT.

### Cap 89 — Projeto Integrador: Treinando Nossa Mini-LLM (`cap_89_treinando_mini_llm`)
- **Problema:** Juntar todos os tijolos anteriores em um treino real de ponta a ponta.
- **Conteúdo:** Treinando o MiniGPT em corpus em português (ex.: Machado de Assis), acompanhando a evolução da geração da época 0 até frases coerentes.

### Cap 90 — Estratégias de *Sampling* (`cap_90_sampling`)
- **Problema:** Escolher sempre o token mais provável gera texto repetitivo.
- **Conteúdo:** Greedy, Temperatura, Top-K e Top-P (*Nucleus Sampling*).

### Cap 91 — Como Testar o que Não Tem Gabarito Único? (`cap_91_avaliacao_generativa`)
- **Problema:** Reflexão metodológica sobre avaliar modelos criativos e abertos.
- **Conteúdo:** Contaminação de benchmarks, métricas proxy e avaliação por pares.

### Cap 92 — Perplexidade na Prática (`cap_92_perplexidade`)
- **Problema:** Medir objetivamente o quão "surpreso" um modelo de linguagem fica com texto real.
- **Conteúdo:** Cálculo de perplexidade ($e^{\text{CrossEntropy}}$) e comparação entre checkpoints.

### Cap 93 — *In-Context Learning*: Zero-Shot e Few-Shot (`cap_93_in_context_learning`)
- **Problema:** Resolver tarefas novas sem atualizar um único peso da rede.
- **Conteúdo:** Como exemplos no *prompt* condicionam a atenção.

### Cap 94 — *Linear Probing*, *Full Fine-Tuning* e Esquecimento Catastrófico (`cap_94_fine_tuning_riscos`)
- **Problema:** Adaptar modelos pré-treinados sem destruir o conhecimento que eles já tinham.
- **Conteúdo:** Congelar tronco vs treinar tudo com $\eta$ baixo e demonstração prática do *Catastrophic Forgetting*.

### Cap 95 — SFT (*Supervised Fine-Tuning*): De Base Model a Assistente (`cap_95_sft_chat`)
- **Problema:** Um modelo base só continua texto; ele não responde instruções no formato de chat.
- **Conteúdo:** Formato `<usuario> ... <assistente> ...` e *loss masking* (penalizando só a resposta).

### Cap 96 — Alinhamento: RLHF e DPO (`cap_96_rlhf_dpo`)
- **Problema:** Alinhar o assistente a preferências humanas e segurança.
- **Conteúdo:** Conectando a Fase 11 (PPO) ao RLHF e sua simplificação direta via DPO.

### Cap 97 — PEFT, LoRA e QLoRA (`cap_97_peft_lora`)
- **Problema:** Fazer *fine-tuning* sem precisar de GPUs gigantes.
- **Conteúdo:** *Adapters*, decomposição de baixo posto (**LoRA**: $W + BA$) em PyTorch puro e noção de QLoRA.

### Cap 98 — Escala e Inferência: *Mixed Precision*, *Gradient Accumulation* e Quantização (`cap_98_escala_quantizacao`)
- **Problema:** Rodar treinos e inferência de modelos maiores em hardware comum.
- **Conteúdo:** `bf16`/`fp16`, acumulação de gradientes e quantização (`int8`/`int4`).

---

## Extras — Tópicos de Fronteira e Pesquisa (`E1`–`E9`)

- **E1 — *Double Descent*:** quebrando o dogma da curva clássica em U.
- **E2 — *Grokking*:** memorização vs generalização tardia em aritmética modular ($a + b \pmod p$) com *Weight Decay*.
- **E3 — Anatomia LLaMA/Qwen:** `RMSNorm`, `SwiGLU` e `RoPE`.
- **E4 — `KV Cache` na Prática:** acelerando geração autoregressiva de $O(n^2)$ para $O(n)$ por passo.
- **E5 — *Mixture of Experts* (MoE):** roteamento esparso escolhendo especialistas por token.
- **E6 — Além da Atenção Quadrática:** *State Space Models* (SSMs / intuição do Mamba).
- **E7 — Interpretabilidade Mecanística:** *Sparse Autoencoders* (SAEs) abrindo a caixa-preta de Transformers.
- **E8 — Pós-Treino e Raciocínio:** *Test-Time Compute* e GRPO.
- **E9 — Busca Semântica e RAG em PyTorch Puro:** conectando Embeddings (Fase 7) com LLMs (Fase 13).
