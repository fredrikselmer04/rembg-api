from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from rembg import remove
import requests
from io import BytesIO

app = FastAPI()

@app.post("/remove-bg")
async def remove_bg(image_url: str = Form(...)):
    try:
        response = requests.get(image_url)
        input_image = response.content
        output_image = remove(input_image)
        return StreamingResponse(BytesIO(output_image), media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Rembg API is running!"}
