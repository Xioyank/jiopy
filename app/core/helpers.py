import base64
import re
from typing import List, Dict, Any, Optional, Tuple
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import httpx
import random

QUALITY_REGEX = re.compile(r"150x150|50x50")
PROTOCOL_REGEX = re.compile(r"^http://")

def create_download_links(encrypted_media_url: str) -> List[Dict[str, str]]:
    if not encrypted_media_url: return []
    qualities = [
        {"id": "_12", "bitrate": "12kbps"}, {"id": "_48", "bitrate": "48kbps"},
        {"id": "_96", "bitrate": "96kbps"}, {"id": "_160", "bitrate": "160kbps"},
        {"id": "_320", "bitrate": "320kbps"}
    ]
    key = b'38346591'
    try:
        # Fix base64 padding issue
        encrypted_media_url += "=" * ((4 - len(encrypted_media_url) % 4) % 4)
        encrypted_bytes = base64.b64decode(encrypted_media_url)
        cipher = DES.new(key, DES.MODE_ECB)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), DES.block_size)
        decrypted_link = decrypted_bytes.decode('utf-8')
    except Exception as e:
        print(f"Decryption failed: {e}")
        return []
    return [{"quality": q["bitrate"], "url": decrypted_link.replace("_96", q["id"])} for q in qualities]

def create_image_links(link: str) -> List[Dict[str, str]]:
    if not link: return []
    qualities = ["50x50", "150x150", "500x500"]
    return [{"quality": q, "url": PROTOCOL_REGEX.sub("https://", QUALITY_REGEX.sub(q, link))} for q in qualities]

USER_AGENTS = ["Mozilla/5.0"]

async def use_fetch(endpoint: str, params: Dict[str, Any], context: Optional[str] = "web6dot0") -> Dict[str, Any]:
    url = "https://www.jiosaavn.com/api.php"
    query_params = {"__call": endpoint, "_format": "json", "_marker": "0", "api_version": "4", "ctx": context}
    query_params.update(params)
    headers = {"Content-Type": "application/json", "User-Agent": USER_AGENTS[0]}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=query_params, headers=headers)
            return {"data": response.json() if response.is_success else None, "ok": response.is_success}
        except Exception as e:
            print(f"Fetch Error: {e}")
            return {"data": None, "ok": False}
