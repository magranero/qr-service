from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
import tempfile, os, io, httpx
from amzqr import amzqr

app = FastAPI(title="QR Service")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/qr")
def generate_qr(
    url: str = Query(..., description="URL to encode"),
    colorized: bool = Query(False),
    contrast: float = Query(1.0),
    brightness: float = Query(1.0),
    picture: str = Query(None, description="Background image URL"),
):
    with tempfile.TemporaryDirectory() as tmpdir:
        fname = "qr.png"
        kwargs = dict(
            words=url,
            save_name=fname,
            save_dir=tmpdir,
            colorized=colorized,
            contrast=contrast,
            brightness=brightness,
        )
        if picture:
            try:
                r = httpx.get(picture, timeout=10, follow_redirects=True)
                r.raise_for_status()
                ext = picture.rsplit(".", 1)[-1].split("?")[0][:4] or "png"
                pic_path = os.path.join(tmpdir, f"bg.{ext}")
                with open(pic_path, "wb") as f:
                    f.write(r.content)
                kwargs["picture"] = pic_path
            except Exception as e:
                raise HTTPException(400, f"Failed to fetch picture: {e}")
        try:
            version, level, qr_name = amzqr.run(**kwargs)
        except Exception as e:
            raise HTTPException(500, f"QR generation failed: {e}")
        qr_path = os.path.join(tmpdir, qr_name)
        data = open(qr_path, "rb").read()
    return StreamingResponse(io.BytesIO(data), media_type="image/png",
                             headers={"Content-Disposition": "inline; filename=qr.png"})
