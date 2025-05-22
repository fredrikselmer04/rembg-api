from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from rembg import remove
import requests
from io import BytesIO

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Rembg API is running!"}

@app.post("/remove-bg")
async def remove_bg(request: Request):
    try:
        data = await request.json()
        image_url = data.get("image_url")

        if not image_url:
            return JSONResponse(content={"error": "Missing image_url"}, status_code=400)

        response = requests.get(image_url)
        if response.status_code != 200:
            return JSONResponse(content={"error": "Image not downloadable"}, status_code=422)

        input_image = response.content
        output_image = remove(input_image)

        return StreamingResponse(BytesIO(output_image), media_type="image/png")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
