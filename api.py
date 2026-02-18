from fastapi import FastAPI, HTTPException, Query
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Insta Downloader API is Running!"}

@app.get("/download")
def get_video_info(url: str = Query(..., description="Instagram URL")):
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        # yt-dlp സെറ്റിംഗ്സ്
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best',
            # ലോഗിൻ ഇഷ്യൂ ഒഴിവാക്കാൻ ചിലപ്പോൾ ഇത് സഹായിക്കും
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # വീഡിയോ ആണോ ഫോട്ടോ ആണോ എന്ന് നോക്കുന്നു
            video_url = info.get('url')
            thumbnail = info.get('thumbnail')
            title = info.get('title', 'No Title')

            return {
                "status": "success",
                "title": title,
                "video_url": video_url,
                "thumbnail": thumbnail
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

