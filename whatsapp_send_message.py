#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Módulo para enviar mensagens WhatsApp via Evolution API

Uso:
    # Enviar mensagem de texto
    python whatsapp_send_message.py --telefone_destino=5598999999999 --text="Olá!"
    
    # Enviar arquivo/imagem
    python whatsapp_send_message.py --telefone_destino=5598999999999 --file=/caminho/arquivo1.jpg
    python whatsapp_send_message.py --telefone_destino=5598999999999 --file=/caminho/arquivo1.jpg --file=/caminho/arquivo2.pdf
"""

import argparse
import os
import sys
import requests
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv


class WhatsAppEvolutionAPI:
    """Cliente para enviar mensagens WhatsApp via Evolution API"""
    
    def __init__(self):
        """Inicializa o cliente com credenciais das variáveis de ambiente"""
        # Carregar variáveis de ambiente do arquivo .env
        load_dotenv()
        
        self.api_key = os.getenv("EVOLUTION_API_KEY")
        self.base_url = os.getenv("EVOLUTION_API_URL")
        self.instance = os.getenv("EVOLUTION_INSTANCE")
        
        # Validar credenciais
        if not self.api_key:
            raise ValueError("Variável de ambiente EVOLUTION_API_KEY não configurada")
        if not self.base_url:
            raise ValueError("Variável de ambiente EVOLUTION_API_URL não configurada")
        if not self.instance:
            raise ValueError("Variável de ambiente EVOLUTION_INSTANCE não configurada")
        
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }
    
    def send_text(self, number: str, text: str) -> Dict[str, Any]:
        """
        Envia mensagem de texto via Evolution API
        
        Args:
            number: Número de telefone em formato internacional (ex: 5598999999999)
            text: Texto da mensagem
        
        Returns:
            Resposta da API
        """
        url = f"{self.base_url}/message/sendText/{self.instance}"
        
        payload = {
            "number": number,
            "text": text
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Erro ao enviar mensagem de texto: {str(e)}")
    
    def send_media(self, number: str, file_path: str, caption: str = "") -> Dict[str, Any]:
        """
        Envia arquivo/mídia via Evolution API
        
        Args:
            number: Número de telefone em formato internacional
            file_path: Caminho do arquivo local
            caption: Legenda (opcional)
        
        Returns:
            Resposta da API
        """
        # Validar arquivo
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        # Ler arquivo e converter para base64
        import base64
        
        with open(file_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode("utf-8")
        
        # Determinar tipo de mídia
        suffix = file_path_obj.suffix.lower()
        media_type = self._get_media_type(suffix)
        
        url = f"{self.base_url}/message/sendMedia/{self.instance}"
        
        payload = {
            "number": number,
            "mediatype": media_type,
            "fileName": file_path_obj.name,
            "caption": caption,
            "media": file_data
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Erro ao enviar arquivo: {str(e)}")
    
    @staticmethod
    def _get_media_type(file_extension: str) -> str:
        """Determina o tipo de mídia baseado na extensão do arquivo
        
        Tipos aceitos: image, document, video, audio
        """
        media_types = {
            # Imagens
            ".jpg": "image",
            ".jpeg": "image",
            ".png": "image",
            ".gif": "image",
            ".webp": "image",
            # Vídeos
            ".mp4": "video",
            ".avi": "video",
            ".mov": "video",
            ".mkv": "video",
            ".flv": "video",
            ".wmv": "video",
            # Áudio
            ".mp3": "audio",
            ".wav": "audio",
            ".m4a": "audio",
            ".ogg": "audio",
            ".aac": "audio",
            ".flac": "audio",
            # Documentos
            ".pdf": "document",
            ".doc": "document",
            ".docx": "document",
            ".txt": "document",
            ".xlsx": "document",
            ".xls": "document",
            ".ppt": "document",
            ".pptx": "document",
            ".zip": "document",
            ".rar": "document",
            ".7z": "document",
        }
        return media_types.get(file_extension, "document")
    
    @staticmethod
    def _get_mime_type(file_extension: str) -> str:
        """Retorna o tipo MIME baseado na extensão do arquivo"""
        mime_types = {
            # Imagens
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
            # Vídeos
            ".mp4": "video/mp4",
            ".avi": "video/x-msvideo",
            ".mov": "video/quicktime",
            ".mkv": "video/x-matroska",
            ".flv": "video/x-flv",
            ".wmv": "video/x-ms-wmv",
            # Áudio
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".m4a": "audio/mp4",
            ".ogg": "audio/ogg",
            ".aac": "audio/aac",
            ".flac": "audio/flac",
            # Documentos
            ".pdf": "application/pdf",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".txt": "text/plain",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xls": "application/vnd.ms-excel",
            ".ppt": "application/vnd.ms-powerpoint",
            ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            ".zip": "application/zip",
            ".rar": "application/vnd.rar",
            ".7z": "application/x-7z-compressed",
        }
        return mime_types.get(file_extension, "application/octet-stream")


def validate_arguments(args) -> bool:
    """
    Valida que --text e --file são mutamente excludentes
    
    Args:
        args: Argumentos parseados
    
    Returns:
        True se válido, lança exceção caso contrário
    """
    has_text = args.text is not None
    has_files = args.file is not None and len(args.file) > 0
    
    if has_text and has_files:
        raise ValueError("Erro: --text e --file são mutamente excludentes. Use um ou outro.")
    
    if not has_text and not has_files:
        raise ValueError("Erro: Forneça --text OU --file")
    
    return True


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Enviar mensagens WhatsApp via Evolution API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Enviar mensagem de texto
  python whatsapp_send_message.py --telefone_destino=5595981234444 --text="Olá!"
  
  # Enviar arquivo único
  python whatsapp_send_message.py --telefone_destino=5595981234444 --file=/caminho/arquivo.jpg
  
  # Enviar múltiplos arquivos
  python whatsapp_send_message.py --telefone_destino=5595981234444 --file=/caminho/arquivo1.jpg --file=/caminho/arquivo2.pdf
        """
    )
    
    parser.add_argument(
        "--telefone_destino",
        required=True,
        help="Número de telefone em formato internacional (ex: 5595981234444)"
    )
    
    parser.add_argument(
        "--text",
        help="Mensagem de texto a enviar"
    )
    
    parser.add_argument(
        "--file",
        action="append",
        help="Caminho do arquivo a enviar. Pode ser usado múltiplas vezes para vários arquivos"
    )
    
    args = parser.parse_args()
    
    try:
        # Validar argumentos
        validate_arguments(args)
        
        # Inicializar cliente
        client = WhatsAppEvolutionAPI()
        
        # Enviar mensagem de texto
        if args.text:
            print(f"Enviando mensagem de texto para {args.telefone_destino}...")
            result = client.send_text(args.telefone_destino, args.text)
            print("✓ Mensagem enviada com sucesso!")
            print(f"Resposta: {result}")
        
        # Enviar arquivos
        elif args.file:
            print(f"Enviando {len(args.file)} arquivo(s) para {args.telefone_destino}...\n")
            
            for idx, file_path in enumerate(args.file, 1):
                try:
                    print(f"[{idx}/{len(args.file)}] Enviando {Path(file_path).name}...")
                    result = client.send_media(args.telefone_destino, file_path)
                    print(f"✓ Arquivo enviado com sucesso!")
                    print(f"    Resposta: {result}\n")
                except (FileNotFoundError, RuntimeError) as e:
                    print(f"✗ Erro ao enviar {Path(file_path).name}: {str(e)}\n")
                    continue
            
            print(f"✓ Envio de {len(args.file)} arquivo(s) concluído!")
    
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"❌ Erro: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
