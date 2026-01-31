# Serviço de OCR em Python (Google Cloud Vision API)

Este guia descreve um microserviço de OCR em Python para o MVP, usando Google
Cloud Vision API, com orquestração via n8n.

## Visão geral

- **OCR service**: recebe um arquivo, chama o Vision API e retorna texto extraído.
- **n8n**: orquestra o fluxo (upload → OCR → gravação em banco → alertas).
- **Banco**: fonte oficial dos dados extraídos e auditáveis.

## Passos recomendados

1. **Habilitar Vision API** no Google Cloud.
2. **Criar Service Account** com permissão para Vision API.
3. **Baixar o JSON** da chave da Service Account.
4. **Subir o microserviço** (FastAPI) com a variável `GOOGLE_APPLICATION_CREDENTIALS`.
5. **Configurar o n8n** para chamar o endpoint `/ocr/process`.
6. **Persistir o resultado** no banco (com logs e status do documento).

## Estrutura sugerida

```
examples/ocr-service-python/
  app.py
  requirements.txt
  Dockerfile
  README.md
```

## Contrato do endpoint (sugestão)

**POST** `/ocr/process`  
**Body**: `multipart/form-data` com campo `file`  
**Response (exemplo)**:

```json
{
  "filename": "rg_joao.png",
  "mime_type": "image/png",
  "full_text": "JOAO DA SILVA...",
  "pages": 1
}
```

## Observações importantes

- Para PDF, considere converter para imagem antes do OCR ou usar
  `async_batch_annotate_files` (mais complexo).
- Registre o status de OCR e o timestamp no banco para auditoria.
- Defina um tamanho máximo de upload para evitar abusos.

