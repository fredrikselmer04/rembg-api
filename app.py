from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from rembg import remove
from io import BytesIO

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Rembg API is running!"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        input_image = await file.read()
        output_image = remove(input_image)
        return StreamingResponse(BytesIO(output_image), media_type="image/png")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
