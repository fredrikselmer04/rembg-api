from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from rembg import remove
from io import BytesIO
import traceback

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
                content={"error": "Uploaded file is empty or too small."}
            )

        try:
            result = remove(contents)
            return StreamingResponse(BytesIO(result), media_type="image/png")

        except Exception as rembg_error:
            error_message = f"rembg failed: {str(rembg_error)}"
            print("🛑 rembg error:\n", traceback.format_exc())
            return JSONResponse(
                status_code=422,
                content={"error": error_message}
            )

    except Exception as e:
        print("❌ Unexpected error:\n", traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": f"Server crashed: {str(e)}"}
        )
