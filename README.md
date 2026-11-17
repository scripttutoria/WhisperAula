# 📄 `README.md` 

Salve o conteúdo abaixo como **`README.md`** na raiz do repositório (`scripttutoria/WhisperAula`), depois:

```bash
git add README.md
git commit -m "docs: adiciona README"
git push
```

---

```markdown
# 🎙️ WhisperAula

> Transcreve aulas em áudio **localmente** com Whisper, gerando `.txt` e `.srt` prontos para revisão e para alimentar LLMs (DeepSeek, Claude, GPT…) na criação de flashcards do Anki.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Whisper](https://img.shields.io/badge/powered%20by-OpenAI%20Whisper-purple.svg)](https://github.com/openai/whisper)

---

## 🎯 Por que este projeto existe

Aulas sem legenda são ruins para revisar: não dá para buscar um termo, pular para um trecho ou copiar uma definição. E mesmo aulas **com** legenda raramente viram material de estudo ativo.

O **WhisperAula** resolve a **primeira ponta** desse problema — transformar o áudio em texto pesquisável, com qualidade e sem depender da nuvem:

1. **Acompanhamento** — gera a transcrição completa em `.txt` (e legendas `.srt`, opcional) para ler, buscar e revisar o conteúdo.
2. **Base para estudo ativo** — o `.txt` gerado é o insumo que você leva manualmente a um LLM (DeepSeek, Claude, ChatGPT…) para produzir perguntas e respostas que viram flashcards no **Anki**.

> ⚠️ **Escopo importante:** o WhisperAula **não** se conecta ao Anki nem a APIs de IA. A geração dos flashcards é feita manualmente por você, colando o `.txt` no LLM de sua preferência. Essa separação mantém o script **simples, offline e agnóstico** — funciona com qualquer LLM, hoje ou amanhã.

Tudo roda **localmente** com o [Whisper](https://github.com/openai/whisper). Seu áudio nunca sai da sua máquina.

---

## ✨ Funcionalidades

- 🎙️ Transcrição local de áudio (MP3, WAV, M4A, FLAC, OGG…)
- 📝 Saída em `.txt` com o texto puro da aula
- 🎞️ Geração opcional de legendas `.srt` com timestamps
- 🌎 Suporte a múltiplos idiomas (padrão: `pt`)
- ⚙️ Escolha do modelo Whisper conforme o equilíbrio precisão/velocidade
- 🔒 100% offline após o download do modelo

---

## 📋 Pré-requisitos

- **Python 3.9+**
- **ffmpeg** instalado no sistema (necessário para decodificar o áudio)
- Espaço em disco para o modelo escolhido (de ~75 MB a ~2.9 GB)

---

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/scripttutoria/WhisperAula.git
cd WhisperAula
```

### 2. (Recomendado) Crie um ambiente virtual

```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate
```

### 3. Instale as dependências Python

```bash
pip install openai-whisper
```

### 4. Instale o `ffmpeg`

| Sistema | Comando |
|---|---|
| **Windows** | `choco install ffmpeg` (ou baixe em https://ffmpeg.org e adicione ao PATH) |
| **macOS** | `brew install ffmpeg` |
| **Linux (Debian/Ubuntu)** | `sudo apt install ffmpeg` |

Verifique a instalação:

```bash
ffmpeg -version
```

---

## 🚀 Uso

### Uso básico

```bash
python WhisperAula.py caminho/para/aula.mp3
```

### Com opções

```bash
python WhisperAula.py aula.mp3 --modelo medium --idioma pt --srt
```

> ⚠️ **Nomes com espaços ou caracteres especiais (`!`, `?`, `&`) precisam de aspas:**

```powershell
# PowerShell / CMD
python WhisperAula.py "O PMBOK não é um bicho de 7 cabeças!.mp3"
```

```bash
# macOS / Linux
python WhisperAula.py "Aula 03 - Gestão de Riscos.mp3"
```

### Opções disponíveis

| Argumento | Descrição | Padrão |
|---|---|---|
| `audio` | Caminho do arquivo de áudio (obrigatório) | — |
| `--modelo` | `tiny`, `base`, `small`, `medium`, `large` | `small` |
| `--idioma` | Código do idioma (`pt`, `en`, `es`…) | `pt` |
| `--srt` | Também gera legendas `.srt` com timestamps | desligado |

### Exemplo de saída no terminal

```
Carregando modelo Whisper 'small'... (pode demorar na primeira vez, baixa o modelo)
Transcrevendo 'aula.mp3'... isso pode levar alguns minutos dependendo do tamanho do áudio.
100%|████████████████████████████████| 6844/6844 [00:23<00:00, 289.23frames/s]

✅ Transcrição salva em: aula.txt
✅ Legendas salvas em: aula.srt
```

---

## 📁 Saídas geradas

Os arquivos são salvos **na mesma pasta do áudio original**, com o mesmo nome:

```
aula.mp3          → áudio original
aula.txt          → transcrição em texto puro (sempre gerada)
aula.srt          → legendas com timestamps (só com --srt)
```

---

## ⚙️ Escolha do modelo Whisper

Modelos maiores são mais precisos, mas mais lentos e pesados.

| Modelo | Tamanho | RAM aprox. | Quando usar |
|---|---|---|---|
| `tiny` | ~75 MB | ~1 GB | Teste rápido, áudio muito limpo |
| `base` | ~142 MB | ~1 GB | Rascunho rápido |
| `small` | ~466 MB | ~2 GB | **Padrão** — bom equilíbrio para PT-BR |
| `medium` | ~1.5 GB | ~5 GB | Aulas importantes, onde precisão importa |
| `large` | ~2.9 GB | ~10 GB | Máxima precisão (recomendado GPU) |

> 💡 Para **aulas em PT-BR**, `small` já entrega qualidade excelente. Use `medium` se o áudio tiver sotaque forte, ruído ou muitos termos técnicos.

---

## 💡 Fluxo recomendado: aula → transcrição → LLM → Anki

O WhisperAula cobre o **passo 1**. Os passos 2 e 3 são manuais — você escolhe o LLM e o ritmo.

```
┌──────────────┐    ┌───────────────┐    ┌─────────────────────┐    ┌─────────┐
│  aula.mp3    │ →  │  aula.txt     │ →  │  LLM (DeepSeek,     │ →  │  Anki   │
│              │    │ (WhisperAula) │    │  Claude, ChatGPT…)  │    │ (cards) │
└──────────────┘    └───────────────┘    └─────────────────────┘    └─────────┘
     passo 1              passo 2                 passo 3
```

### Passo 1 — Transcreva

```bash
python WhisperAula.py aula.mp3 --modelo small --srt
```

### Passo 2 — Gere perguntas com IA (manual)

Abra o `.txt` gerado e cole a transcrição em um LLM junto com um prompt como:

```
A partir da transcrição abaixo, gere flashcards no estilo Anki para estudo ativo.

Regras:
- Formato: cada linha é "Pergunta;Resposta".
- Uma pergunta curta e específica por card.
- Foque em: definições, listas, siglas, relações causa-efeito, diferenças entre conceitos.
- NÃO invente informação que não esteja no texto.
- Máximo 25 cards, os mais importantes primeiro.
- Responda SOMENTE com o CSV, sem cabeçalho, sem comentários.

Transcrição:
"""
[COLE AQUI O CONTEÚDO DO .txt]
"""
```

### Passo 3 — Importe no Anki (manual)

1. Salve a saída do LLM como `cards.csv`.
2. No Anki: **Arquivo → Importar** → selecione o `cards.csv`.
3. Separador: `;` — mapeie coluna 1 → **Frente**, coluna 2 → **Verso**.
4. Escolha o baralho e confirme.

> 🔎 **Revise os cards antes de estudar.** LLMs às vezes criam perguntas triviais ou distorcem conceitos sutis. 5 minutos de revisão economizam horas de revisão errada.

---

## 🩺 Problemas comuns

### `error: unrecognized arguments: PMBOK não é um bicho...`

O caminho tem **espaços** — o terminal dividiu em vários argumentos. **Coloque o caminho entre aspas:**

```powershell
python WhisperAula.py "O PMBOK não é um bicho de 7 cabeças!.mp3"
```

### `UserWarning: FP16 is not supported on CPU`

**Aviso inofensivo.** Você está em CPU; o Whisper passa a usar FP32 (mais preciso, um pouco mais lento). Só sumiria com GPU NVIDIA + CUDA.

### `ffmpeg not found` / `FileNotFoundError: ffmpeg`

O `ffmpeg` **não está no PATH**. Reinstale com o gerenciador do seu sistema ou adicione manualmente o executável ao PATH do Windows.

### `openai-whisper não está instalado`

```bash
pip install openai-whisper
```

Confirme que está usando o Python do venv correto (`where python` no Windows, `which python` no macOS/Linux).

### A transcrição está demorando muito

Você está em CPU com um modelo grande. Opções:
- Troque para `--modelo small` (ou `base`)
- Ou instale o Whisper com suporte a CUDA (GPU NVIDIA) — veja [instruções oficiais](https://github.com/openai/whisper#setup)

### Áudio do Audacity (`.aup4`)

O script **não lê** projetos do Audacity. Exporte primeiro:
**File → Export → Export as MP3 (ou WAV)** — e use o arquivo exportado.

---

## 🚫 O que o WhisperAula **não** faz (por design)

- ❌ Não se conecta à API do Anki
- ❌ Não chama APIs de LLM
- ❌ Não gera flashcards automaticamente
- ❌ Não envia áudio para a nuvem

Essas etapas são **intencionalmente manuais**. Mantêm o projeto simples, offline, auditável e independente de qualquer provedor de IA.

---

## 🗺️ Roadmap (ideias futuras)

- [ ] Exportar `.vtt` (WebVTT) além de `.srt`
- [ ] Modo `--batch` para transcrever uma pasta inteira
- [ ] Presets de prompt para geração de flashcards
- [ ] Flag opcional `--llm` para chamada de API (BYOK)
- [ ] Integração opcional via AnkiConnect

---

## 🤝 Contribuindo

Sugestões, issues e PRs são bem-vindos!

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/minha-feature`)
3. Commit suas mudanças (`git commit -m 'feat: minha feature'`)
4. Push (`git push origin feature/minha-feature`)
5. Abra um Pull Request


---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👤 Autor

**scripttutoria**
- GitHub: [@scripttutoria](https://github.com/scripttutoria)

---
