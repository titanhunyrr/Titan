from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import base64, io

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Python Encoder Decoder API running"}

@app.post("/encode")
async def encode_file(file: UploadFile = File(...)):
    data = await file.read()
    encoded = base64.b64encode(data).decode("utf-8")
    return {
        "filename": file.filename,
        "encoded_data": encoded
    }

@app.post("/decode")
async def decode_file(
    encoded_data: str = Form(...),
    filename: str = Form("decoded_file")
):
    decoded = base64.b64decode(encoded_data)
    return StreamingResponse(
        io.BytesIO(decoded),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )