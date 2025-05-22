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
        contents = await file.read()

        if not contents or len(contents) < 100:
            return JSONResponse(
                status_code=422,
                content={"error": "Uploaded file is empty or too small to be an image."}
            )

        try:
            # ingen .decode() her
            output_image = remove(contents)
        except Exception as rembg_error:
            return JSONResponse(
                status_code=422,
                content={"error": f"Rembg failed to process image: {str(rembg_error)}"}
            )

        return StreamingResponse(BytesIO(output_image), media_type="image/png")

    except Exception as general_error:
        import traceback
        print("Unexpected error in /remove-bg:", traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": f"Unexpected server error: {str(general_error)}"}
        )
