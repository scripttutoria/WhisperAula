#!/usr/bin/env python3
"""
Transcreve áudio para texto usando o Whisper (OpenAI), rodando localmente.

INSTALAÇÃO (rode no terminal, uma vez só):
    pip install openai-whisper
    # O whisper também precisa do ffmpeg instalado no sistema:
    #   Windows: choco install ffmpeg   (ou baixe em https://ffmpeg.org e adicione ao PATH)
    #   Mac:     brew install ffmpeg
    #   Linux:   sudo apt install ffmpeg

USO:
    python transcrever_audio.py caminho/para/audio.mp3
    python transcrever_audio.py caminho/para/audio.wav --modelo medium --idioma pt

    Isso gera um arquivo .txt (e opcionalmente .srt com legendas) na mesma pasta do áudio.

MODELOS DISPONÍVEIS (do mais rápido/impreciso ao mais lento/preciso):
    tiny, base, small, medium, large
    - "base" ou "small": bom equilíbrio para aulas/podcasts em PT-BR
    - "medium": mais preciso, mas mais lento (recomendado se sua máquina aguentar)
    - "large": máxima precisão, exige mais RAM/GPU e é bem mais lento em CPU

DICA: se seu arquivo for .aup4 (projeto do Audacity), primeiro exporte o áudio
pelo Audacity: File > Export > Export as MP3 (ou WAV), e use o arquivo exportado aqui.
"""

import argparse
import sys
from pathlib import Path


def transcrever(caminho_audio: str, modelo: str = "small", idioma: str = "pt", gerar_srt: bool = False):
    try:
        import whisper
    except ImportError:
        print("ERRO: o pacote 'openai-whisper' não está instalado.")
        print("Instale com:  pip install openai-whisper")
        sys.exit(1)

    audio_path = Path(caminho_audio)
    if not audio_path.exists():
        print(f"ERRO: arquivo não encontrado: {audio_path}")
        sys.exit(1)

    print(f"Carregando modelo Whisper '{modelo}'... (pode demorar na primeira vez, baixa o modelo)")
    model = whisper.load_model(modelo)

    print(f"Transcrevendo '{audio_path.name}'... isso pode levar alguns minutos dependendo do tamanho do áudio.")
    resultado = model.transcribe(str(audio_path), language=idioma, verbose=False)

    # Salva o texto puro
    txt_path = audio_path.with_suffix(".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(resultado["text"].strip())
    print(f"\n✅ Transcrição salva em: {txt_path}")

    # Opcionalmente salva legendas .srt com timestamps
    if gerar_srt:
        srt_path = audio_path.with_suffix(".srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segmento in enumerate(resultado["segments"], start=1):
                inicio = formatar_timestamp(segmento["start"])
                fim = formatar_timestamp(segmento["end"])
                texto = segmento["text"].strip()
                f.write(f"{i}\n{inicio} --> {fim}\n{texto}\n\n")
        print(f"✅ Legendas salvas em: {srt_path}")

    return resultado["text"]


def formatar_timestamp(segundos: float) -> str:
    """Formata segundos para o formato SRT: HH:MM:SS,mmm"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = int(segundos % 60)
    milissegundos = int((segundos - int(segundos)) * 1000)
    return f"{horas:02d}:{minutos:02d}:{segs:02d},{milissegundos:03d}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcreve áudio para texto usando Whisper")
    parser.add_argument("audio", help="Caminho do arquivo de áudio (mp3, wav, m4a, etc.)")
    parser.add_argument(
        "--modelo",
        default="small",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Tamanho do modelo Whisper (padrão: small)",
    )
    parser.add_argument("--idioma", default="pt", help="Código do idioma (padrão: pt)")
    parser.add_argument("--srt", action="store_true", help="Também gerar arquivo de legendas .srt com timestamps")

    args = parser.parse_args()
    transcrever(args.audio, modelo=args.modelo, idioma=args.idioma, gerar_srt=args.srt)