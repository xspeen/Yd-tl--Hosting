import os
import uuid
import asyncio
import subprocess
import logging
import shutil
import tempfile
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="yt-dlp Unlimited Downloader API",
    description="Download videos from 1000+ platforms with no limits",
    version="3.0"
)

# Enable CORS for all origins (no restrictions)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NO RATE LIMITS - Removed all rate limiting code

# Download tracking
active_downloads: Dict[str, Dict[str, Any]] = {}
download_stats = {
    "total_downloads": 0,
    "total_bytes": 0,
    "start_time": datetime.now().isoformat()
}

# ==================== HELPER FUNCTIONS ====================

def cleanup_temp_dir(temp_dir: str):
    """Clean up temporary directory"""
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.info(f"Cleaned up: {temp_dir}")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

async def run_ytdlp_command(cmd: List[str], timeout: int = 300) -> tuple:
    """Run yt-dlp command with timeout"""
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), 
            timeout=timeout
        )
        return process.returncode, stdout, stderr
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        raise TimeoutError(f"Command timed out after {timeout} seconds")

def get_platform_specific_options(url: str) -> List[str]:
    """Get platform-specific yt-dlp options for better compatibility"""
    options = []
    
    if "tiktok.com" in url:
        options.extend([
            "--impersonate", "chrome-131",
            "--add-header", "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ])
    elif "instagram.com" in url:
        options.extend([
            "--add-header", "Referer:https://www.instagram.com/",
            "--add-header", "User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
        ])
    elif "twitter.com" in url or "x.com" in url:
        options.extend([
            "--add-header", "Authorization:Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        ])
    elif "youtube.com" in url or "youtu.be" in url:
        options.extend([
            "--extractor-args", "youtube:player_client=android",
            "--concurrent-fragments", "5"
        ])
    
    return options

# ==================== HEALTH CHECK ====================
@app.get("/")
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "yt-dlp Unlimited Downloader",
        "version": "3.0",
        "supported_platforms": "1000+",
        "limits": "UNLIMITED - No rate limits, no restrictions",
        "stats": download_stats,
        "active_downloads": len(active_downloads),
        "endpoints": {
            "/": "This info",
            "/info": "GET - Get video information",
            "/formats": "GET - List available formats",
            "/download": "POST - Download video",
            "/stream/{task_id}": "GET - Stream download progress",
            "/cancel/{task_id}": "POST - Cancel download",
            "/stats": "GET - Download statistics"
        }
    }

@app.get("/stats")
async def get_stats():
    """Get download statistics"""
    return {
        "stats": download_stats,
        "active_downloads": len(active_downloads),
        "active_tasks": list(active_downloads.keys())
    }

# ==================== GET VIDEO INFO ====================
@app.get("/info")
async def get_video_info(url: str):
    """Get video information without downloading"""
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] Getting info for: {url}")
    
    try:
        # Build command
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-playlist",
            "--no-warnings",
            "--ignore-errors"
        ]
        
        # Add platform-specific options
        cmd.extend(get_platform_specific_options(url))
        cmd.append(url)
        
        returncode, stdout, stderr = await run_ytdlp_command(cmd, timeout=60)
        
        if returncode != 0:
            error_msg = stderr.decode()
            logger.error(f"[{request_id}] yt-dlp error: {error_msg}")
            
            # Try with different options if it's a known platform
            if "tiktok" in url:
                # Try without impersonation
                cmd = ["yt-dlp", "--dump-json", "--no-playlist", url]
                returncode, stdout, stderr = await run_ytdlp_command(cmd, timeout=60)
                if returncode != 0:
                    raise HTTPException(status_code=400, detail="Could not fetch video info")
            else:
                raise HTTPException(status_code=400, detail="Could not fetch video info")
        
        info = json.loads(stdout)
        
        # Extract available formats
        formats = []
        for f in info.get('formats', []):
            format_info = {
                'format_id': f.get('format_id'),
                'ext': f.get('ext'),
                'filesize': f.get('filesize') or f.get('filesize_approx', 0),
                'vcodec': f.get('vcodec'),
                'acodec': f.get('acodec')
            }
            
            # Determine quality label
            if f.get('height'):
                format_info['quality'] = f'{f.get("height")}p'
                format_info['type'] = 'video'
            elif f.get('abr'):
                format_info['quality'] = f'{f.get("abr")}kbps'
                format_info['type'] = 'audio'
            else:
                continue
            
            formats.append(format_info)
        
        result = {
            'id': info.get('id'),
            'title': info.get('title'),
            'duration': info.get('duration'),
            'uploader': info.get('uploader'),
            'uploader_url': info.get('uploader_url'),
            'views': info.get('view_count'),
            'likes': info.get('like_count'),
            'thumbnail': info.get('thumbnail'),
            'description': info.get('description')[:500] if info.get('description') else '',
            'webpage_url': info.get('webpage_url'),
            'extractor': info.get('extractor'),
            'formats': formats[:20]  # Limit to 20 formats for response size
        }
        
        logger.info(f"[{request_id}] Success: {info.get('title')}")
        return result
        
    except asyncio.TimeoutError:
        logger.error(f"[{request_id}] Timeout")
        raise HTTPException(status_code=504, detail="Request timeout")
    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== LIST FORMATS ====================
@app.get("/formats")
async def list_formats(url: str):
    """List all available formats in human-readable format"""
    try:
        cmd = [
            "yt-dlp",
            "-F",
            "--no-playlist",
            url
        ]
        
        returncode, stdout, stderr = await run_ytdlp_command(cmd, timeout=60)
        
        if returncode != 0:
            raise HTTPException(status_code=400, detail="Could not fetch formats")
        
        return {"formats": stdout.decode()}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== DOWNLOAD VIDEO - NO LIMITS ====================
@app.post("/download")
async def download_video(
    url: str,
    format_id: Optional[str] = "best",
    audio_only: Optional[bool] = False,
    background_tasks: BackgroundTasks = None
):
    """Download video with no size limits - streams directly"""
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] Download request: {url}, format: {format_id}")
    
    # Track download
    download_stats["total_downloads"] += 1
    task_id = request_id
    
    active_downloads[task_id] = {
        "status": "downloading",
        "url": url,
        "start_time": datetime.now().isoformat(),
        "format": format_id
    }
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix=f"ytdlp_{request_id}_")
    
    try:
        # Determine output template
        output_template = os.path.join(temp_dir, "%(title)s.%(ext)s")
        
        # Build base command
        cmd = [
            "yt-dlp",
            "--no-playlist",
            "--no-warnings",
            "--ignore-errors",
            "--progress",
            "--newline",
            "-o", output_template
        ]
        
        # Add format selection
        if audio_only:
            cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
        elif format_id and format_id != "best":
            # Try to get the best combination with selected video and best audio
            cmd.extend(["-f", f"{format_id}+bestaudio/best"])
        else:
            cmd.extend(["-f", "bestvideo+bestaudio/best"])
        
        # Add platform-specific options
        cmd.extend(get_platform_specific_options(url))
        
        # Add URL
        cmd.append(url)
        
        logger.info(f"[{request_id}] Command: {' '.join(cmd)}")
        
        # Execute yt-dlp with longer timeout for large files
        returncode, stdout, stderr = await run_ytdlp_command(cmd, timeout=600)  # 10 minute timeout
        
        if returncode != 0:
            error_msg = stderr.decode()
            logger.error(f"[{request_id}] yt-dlp error: {error_msg}")
            
            # Try fallback with different options
            if "requested format not available" in error_msg:
                # Fallback to best
                cmd = [
                    "yt-dlp",
                    "--no-playlist",
                    "-o", output_template,
                    "-f", "best",
                    url
                ]
                returncode, stdout, stderr = await run_ytdlp_command(cmd, timeout=600)
                
                if returncode != 0:
                    raise HTTPException(status_code=400, detail=f"Download failed: {error_msg}")
            else:
                raise HTTPException(status_code=400, detail=f"Download failed: {error_msg}")
        
        # Find the downloaded file
        files = os.listdir(temp_dir)
        if not files:
            raise HTTPException(status_code=500, detail="No file generated")
        
        file_path = os.path.join(temp_dir, files[0])
        file_size = os.path.getsize(file_path)
        
        # Update stats
        download_stats["total_bytes"] += file_size
        active_downloads[task_id]["status"] = "completed"
        active_downloads[task_id]["file_size"] = file_size
        active_downloads[task_id]["filename"] = files[0]
        
        # Determine media type
        media_type = "video/mp4"
        if audio_only:
            media_type = "audio/mpeg"
        elif file_path.endswith('.mp3'):
            media_type = "audio/mpeg"
        elif file_path.endswith('.webm'):
            media_type = "video/webm"
        elif file_path.endswith('.mkv'):
            media_type = "video/x-matroska"
        
        logger.info(f"[{request_id}] Success: {files[0]} ({file_size} bytes)")
        
        # Schedule cleanup after sending
        if background_tasks:
            background_tasks.add_task(cleanup_temp_dir, temp_dir)
        else:
            # If no background tasks, clean up after a delay
            asyncio.create_task(asyncio.sleep(60))
            asyncio.create_task(asyncio.to_thread(cleanup_temp_dir, temp_dir))
        
        # Stream file directly with no size limits
        return FileResponse(
            file_path,
            media_type=media_type,
            filename=files[0],
            headers={
                "Content-Length": str(file_size),
                "X-Request-ID": request_id,
                "X-Task-ID": task_id,
                "Cache-Control": "no-cache",
                "Content-Disposition": f"attachment; filename={files[0]}"
            }
        )
        
    except asyncio.TimeoutError:
        logger.error(f"[{request_id}] Download timeout")
        active_downloads[task_id]["status"] = "timeout"
        cleanup_temp_dir(temp_dir)
        raise HTTPException(status_code=504, detail="Download timeout - file may be too large")
        
    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}")
        active_downloads[task_id]["status"] = "error"
        active_downloads[task_id]["error"] = str(e)
        cleanup_temp_dir(temp_dir)
        raise HTTPException(status_code=500, detail=str(e))

# ==================== STREAM PROGRESS ====================
@app.get("/stream/{task_id}")
async def stream_progress(task_id: str):
    """Stream download progress (Server-Sent Events)"""
    async def event_generator():
        while task_id in active_downloads:
            task = active_downloads[task_id]
            yield f"data: {json.dumps(task)}\n\n"
            await asyncio.sleep(1)
        yield "data: {\"status\": \"completed\"}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

# ==================== CANCEL DOWNLOAD ====================
@app.post("/cancel/{task_id}")
async def cancel_download(task_id: str):
    """Cancel an active download"""
    if task_id in active_downloads:
        active_downloads[task_id]["status"] = "cancelled"
        return {"status": "cancelled", "task_id": task_id}
    raise HTTPException(status_code=404, detail="Task not found")

# ==================== TASK STATUS ====================
@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Get download task status"""
    if task_id in active_downloads:
        return active_downloads[task_id]
    raise HTTPException(status_code=404, detail="Task not found")

# ==================== CLEANUP OLD TASKS ====================
@app.post("/cleanup")
async def cleanup_old_tasks(hours: int = 24):
    """Clean up old completed tasks"""
    now = time.time()
    to_remove = []
    
    for task_id, task in active_downloads.items():
        if task["status"] in ["completed", "error", "cancelled"]:
            task_time = datetime.fromisoformat(task["start_time"]).timestamp()
            if now - task_time > hours * 3600:
                to_remove.append(task_id)
    
    for task_id in to_remove:
        del active_downloads[task_id]
    
    return {"removed": len(to_remove), "remaining": len(active_downloads)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=4,  # Multiple workers for better performance
        log_level="info"
    )
