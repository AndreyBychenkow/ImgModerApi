from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
import io


load_dotenv()

app = FastAPI(title="Image Moderation API")


DEEPAI_API_KEY = os.getenv("DEEPAI_API_KEY")

if not DEEPAI_API_KEY:
    raise ValueError("DEEPAI_API_KEY not found in environment variables")
DEEPAI_API_URL = "https://api.deepai.org/api/nsfw-detector"


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def is_allowed_file(filename: str) -> bool:

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):

    if not file.filename or not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only .jpg and .png files are allowed.",
        )
    try:

        contents = await file.read()

        files = {"image": (file.filename, io.BytesIO(contents), file.content_type)}

        headers = {"api-key": DEEPAI_API_KEY}

        response = requests.post(
            DEEPAI_API_URL, files=files, headers=headers, timeout=30
        )

        if response.status_code != 200:
            print("DeepAI response text:", response.text)
            raise HTTPException(
                status_code=500, detail=f"DeepAI API error: {response.text}"
            )
        else:
            print("DeepAI response text:", response.text)
        result = response.json()

        nsfw_score = result.get("output", {}).get("nsfw_score", 0)

        if nsfw_score > 0.7:
            return JSONResponse(
                content={"status": "REJECTED", "reason": "NSFW content"}
            )
        else:
            return JSONResponse(content={"status": "OK"})
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to DeepAI API: {str(e)}"
        )
    except Exception as e:
        import traceback

        print("ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/")
async def root():

    return {"message": "Image Moderation API is running"}


@app.get("/health")
async def health_check():

    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    