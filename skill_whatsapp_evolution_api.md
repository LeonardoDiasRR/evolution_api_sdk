# Skill: Enviar Mensagens de WhatsApp via Evolution API

## Descrição

Esta skill permite que um agente envie mensagens de WhatsApp (texto ou
áudio) utilizando o módulo `whatsapp_send_message.py` que integra-se
com a **Evolution API**.

A skill encapsula toda a complexidade da API, permitindo que agentes
enviem mensagens de forma simples usando linha de comando.

------------------------------------------------------------------------

------------------------------------------------------------------------

# 2. Módulo whatsapp_send_message.py

O módulo `whatsapp_send_message.py` é um script Python que gerencia
o envio de mensagens WhatsApp via Evolution API.

**Localização no Linux:**

    /opt/projetos/evolution_api_sdk/whatsapp_send_message.py

**Executor Python (Linux):**

    /opt/projetos/evolution_api_sdk/venv/bin/python

------------------------------------------------------------------------

# 3. Enviar Mensagem de Texto

Para enviar uma mensagem de texto via WhatsApp:

**Comando Linux:**

``` bash
/opt/projetos/evolution_api_sdk/venv/bin/python /opt/projetos/evolution_api_sdk/whatsapp_send_message.py --telefone_destino=5595981021111 --text="Olá! Esta é uma mensagem de texto."
```

**Parâmetros:**

- `--telefone_destino` (obrigatório): Número em formato internacional
  - Exemplo: `5595981021111`
  - Sem espaços, parênteses ou hífens

- `--text` (obrigatório ou mutual com `--file`): Mensagem de texto
  - Exemplo: `"Seu texto aqui"`

**Resposta esperada:**

``` json
{
  "success": true,
  "message": "Message sent successfully"
}
```

------------------------------------------------------------------------

# 4. Enviar Arquivo de Áudio

Para enviar um arquivo de áudio via WhatsApp:

**Comando Linux:**

``` bash
/opt/projetos/evolution_api_sdk/venv/bin/python /opt/projetos/evolution_api_sdk/whatsapp_send_message.py --telefone_destino=5595981021111 --file="/caminho/para/audio.mp3"
```

**Importante:** Cada arquivo enviado gera uma mensagem separada no WhatsApp.

**Tipos de áudio suportados:**

- `.mp3` - MPEG Audio
- `.wav` - Waveform Audio
- `.m4a` - MPEG-4 Audio
- `.ogg` - Ogg Vorbis
- `.aac` - Advanced Audio Coding
- `.flac` - FLAC Audio

**Parâmetros:**

- `--telefone_destino` (obrigatório): Número em formato internacional

- `--file` (obrigatório ou mutual com `--text`): Caminho do arquivo
  - Pode ser usado múltiplas vezes para enviar vários arquivos
  - Exemplo: `--file=/caminho/audio1.mp3 --file=/caminho/audio2.mp3`
  - **Importante:** Cada arquivo é enviado em uma mensagem separada

**Resposta esperada (por arquivo):**

``` json
{
  "success": true,
  "message": "File sent successfully"
}
```

------------------------------------------------------------------------

# 5. Enviar Múltiplos Arquivos

O módulo suporta o envio de múltiplos arquivos em uma única execução.
**Cada arquivo é enviado em uma mensagem separada no WhatsApp.**

**Comando Linux:**

``` bash
/opt/projetos/evolution_api_sdk/venv/bin/python /opt/projetos/evolution_api_sdk/whatsapp_send_message.py --telefone_destino=5595981021111 --file="/caminho/audio1.mp3" --file="/caminho/documento.pdf" --file="/caminho/imagem.jpg"
```

**Behavior:**

Ao passar 3 arquivos como no exemplo acima, o módulo enviará:
1. Mensagem 1: audio1.mp3
2. Mensagem 2: documento.pdf
3. Mensagem 3: imagem.jpg

O receptor receberá 3 mensagens separadas na conversa do WhatsApp.

**Tipos de arquivo suportados:**

- **Imagens:** jpg, jpeg, png, gif, webp
- **Áudio:** mp3, wav, m4a, ogg, aac, flac
- **Vídeos:** mp4, avi, mov, mkv, flv, wmv
- **Documentos:** pdf, doc, docx, txt, xlsx, xls, ppt, pptx, zip, rar, 7z

------------------------------------------------------------------------

# 6. Regras para o Agente

O agente deve seguir as seguintes regras:

1. **Formato do telefone:** Sempre usar formato internacional sem
   formatação:
   - ✅ Correto: `5595981021111`
   - ❌ Incorreto: `(55) 9598-1021111`, `+55 95 98102-1111`

2. **Parâmetros mutamente excludentes:**
   - Use OU `--text` OU `--file`, nunca ambos
   - O módulo retornará erro se ambos forem fornecidos

3. **Múltiplos arquivos geram múltiplas mensagens:**
   - Cada arquivo passado via `--file` gera uma mensagem separada
   - 3 arquivos = 3 mensagens no WhatsApp do receptor
   - Útil para organizar conteúdo temático

4. **Caminho do arquivo:** Usar caminho absoluto ou relativo válido
   - Verificar se o arquivo existe antes de enviar

5. **Variáveis de ambiente:** Devem estar configuradas antes da execução
   - `EVOLUTION_API_KEY`
   - `EVOLUTION_API_URL`
   - `EVOLUTION_INSTANCE`

6. **Tratamento de erros:**
   - Capturar erros HTTP da API
   - Se um arquivo falhar, os demais continuam sendo enviados
   - Registrar logs das tentativas de envio
   - Evitar envios duplicados

------------------------------------------------------------------------

# 7. Fluxo de Decisão do Agente

```
Usuário pediu envio de mensagem WhatsApp?
        │
        ├─ Mensagem de texto (1 mensagem)
        │      └─ --text="mensagem"
        │
        └─ Arquivo(s) (1 mensagem por arquivo)
               ├─ --file=/caminho/arquivo1
               ├─ --file=/caminho/arquivo2
               └─ --file=/caminho/arquivo3
                  (Resultado: 3 mensagens no WhatsApp)
```

------------------------------------------------------------------------

# 8. Exemplos Práticos

### Enviar saudação

``` bash
/opt/projetos/evolution_api_sdk/venv/bin/python /opt/projetos/evolution_api_sdk/whatsapp_send_message.py --telefone_destino=5595981021111 --text="Olá! Sua solicitação foi recebida."
```

### Enviar nota de voz

``` bash
/opt/projetos/evolution_api_sdk/venv/bin/python /opt/projetos/evolution_api_sdk/whatsapp_send_message.py --telefone_destino=5595981021111 --file="/arquivos/nota_voz.mp3"
```

### Enviar múltiplos documentos

``` bash
/opt/projetos/evolution_api_sdk/venv/bin/python /opt/projetos/evolution_api_sdk/whatsapp_send_message.py --telefone_destino=5595981021111 --file="/documentos/contrato.pdf" --file="/documentos/termo.docx" --file="/imagens/assinatura.jpg"
```

**Resultado:** O receptor receberá 3 mensagens separadas:
1. Arquivo contrato.pdf
2. Arquivo termo.docx
3. Arquivo assinatura.jpg

------------------------------------------------------------------------

# 9. Códigos de Erro

  Código   Significado                            Solução
  -------- -------------------------------------- -----------------------------------------------
  401      API Key inválida                       Verificar EVOLUTION_API_KEY no .env
  404      Instância não encontrada               Verificar EVOLUTION_INSTANCE no .env
  400      Parâmetro inválido                     Validar formato do telefone e parâmetros
  500      Erro interno da Evolution API          Verificar logs da Evolution API
  FileError Arquivo não encontrado                Verificar caminho do arquivo fornecido
  ValueError --text e --file usados simultaneamente Use apenas um dos parâmetros

------------------------------------------------------------------------

# 10. Boas Práticas

- ✅ Validar número de telefone antes de enviar
- ✅ Registrar logs de todas as tentativas de envio
- ✅ Verificar se o arquivo existe antes de processar
- ✅ Tratrar erros de conexão com retry
- ✅ Usar caminhos absolutos para arquivos
- ✅ Manter arquivo `.env` seguro (não fazer commit no git)
- ✅ Lembrar que cada arquivo gera uma mensagem separada
- ✅ Agrupar arquivos relacionados em uma única execução
- ❌ Nunca hardcodear API KEY no código
- ❌ Nunca envisar sem validar o número
- ❌ Não enviar sem verificar se arquivo existe
- ❌ Não enviar centenas de arquivos em uma única execução

------------------------------------------------------------------------

# 11. Integração com Agentes

Para integrar com um agente, execute o módulo através de uma chamada
de sistema (subprocess/shell):

### Enviar mensagem de texto

``` python
import subprocess

def enviar_whatsapp_texto(telefone, mensagem):
    cmd = "/opt/projetos/evolution_api_sdk/venv/bin/python /opt/projetos/evolution_api_sdk/whatsapp_send_message.py --telefone_destino={} --text='{}'".format(telefone, mensagem)
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        return {"success": True, "output": result.stdout}
    else:
        return {"success": False, "error": result.stderr}
```

### Enviar múltiplos arquivos (cada um em uma mensagem)

``` python
import subprocess

def enviar_whatsapp_arquivos(telefone, arquivos):
    """
    Envia múltiplos arquivos. Cada arquivo gera uma mensagem separada.
    
    Args:
        telefone: Número em formato internacional
        arquivos: Lista de caminhos dos arquivos
    
    Returns:
        Resultado da execução
    """
    arquivos_args = " ".join([f"--file=\"{arquivo}\"" for arquivo in arquivos])
    cmd = f"/opt/projetos/evolution_api_sdk/venv/bin/python /opt/projetos/evolution_api_sdk/whatsapp_send_message.py --telefone_destino={telefone} {arquivos_args}"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        return {"success": True, "output": result.stdout}
    else:
        return {"success": False, "error": result.stderr}

# Exemplo de uso:
# enviar_whatsapp_arquivos(
#     "5595981021111",
#     ["/docs/contrato.pdf", "/docs/termo.docx", "/imagens/assinatura.jpg"]
# )
# Resultado: 3 mensagens enviadas (uma para cada arquivo)
```
