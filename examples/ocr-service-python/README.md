# OCR Service (Python + Google Cloud Vision)

Microserviço simples de OCR para o MVP. Recebe imagens e retorna o texto
extraído pelo Google Cloud Vision API.

## Pré-requisitos

1. Habilitar **Vision API** no Google Cloud.
2. Criar uma **Service Account** com permissão para Vision API.
3. Baixar o arquivo JSON da chave.

## Executar localmente

```bash
python -m venv .venv
source .venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/credencial.json
pip install -r requirements.txt
uvicorn app:app --reload --port 8080
```

> Dica: no VS Code, abra a pasta `examples/ocr-service-python/` e execute
> os comandos acima no terminal integrado. Não é necessário “transformar”
> o VS Code em aplicativo, ele só serve como editor/terminal.

## Executar com Docker

```bash
docker build -t ocr-service-python .
docker run -p 8080:8080 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/credentials/vision.json \
  -v /caminho/para/credencial.json:/credentials/vision.json \
  ocr-service-python
```

## Endpoint principal

**POST** `/ocr/process`  
Body: `multipart/form-data` com o campo `file`

```bash
curl -X POST http://localhost:8080/ocr/process \
  -F file=@/caminho/para/rg.png
```

## Integração com n8n (resumo)

1. Trigger (upload do documento).
2. HTTP Request para `POST /ocr/process`.
3. Persistir `full_text` no banco.
4. Disparar alertas e atualizar status do documento.

## Limitações atuais

- Suporte apenas a imagens (PNG/JPG).
- PDFs devem ser convertidos antes do OCR.
