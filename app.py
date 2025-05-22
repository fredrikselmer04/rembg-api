from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from rembg import remove
import requests
from io import BytesIO

app = FastAPI()

@app.post("/remove-bg")
async def remove_bg(request: Request):
    try:
        data = await request.json()
        image_url = data.get("image_url")

        if not image_url:
            return JSONResponse(content={"error": "Missing image_url"}, status_code=400)

        # Hent bildet fra URL
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            return JSONResponse(content={"error": "Could not download image"}, status_code=422)

        input_image = image_response.content
        output_image = remove(input_image)

        return StreamingResponse(BytesIO(output_image), media_type="image/png")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def index():
    return {"message": "Rembg API is running!"}
