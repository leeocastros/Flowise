from fastapi import FastAPI, File, HTTPException, UploadFile
from google.cloud import vision

app = FastAPI(title="OCR Service", version="0.1.0")
client = vision.ImageAnnotatorClient()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/ocr/process")
async def process_ocr(file: UploadFile = File(...)) -> dict:
    if not file.content_type:
        raise HTTPException(status_code=400, detail="Missing content type.")

    is_image = file.content_type.startswith("image/")
    if not is_image:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload an image.",
        )

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file.")

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise HTTPException(status_code=502, detail=response.error.message)

    full_text = response.full_text_annotation.text or ""
    pages = len(response.full_text_annotation.pages)

    return {
        "filename": file.filename,
        "mime_type": file.content_type,
        "full_text": full_text,
        "pages": pages,
    }
