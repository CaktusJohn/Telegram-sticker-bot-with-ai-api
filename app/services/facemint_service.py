# app/services/facemint_service.py
import aiohttp
import asyncio
import json
from typing import Any, Dict, Optional
from app.utils.logger import logger
from config import FACEMINT_API_KEY, DEBUG

BASE_URL = "https://api.facemint.io/api"
CONNECT_TIMEOUT = 10
REQUEST_TIMEOUT = 60
MAX_RETRIES = 3
RETRY_STATUSES = (429, 500, 502, 503, 504)

class FacemintError(Exception):
    """Общая ошибка Facemint API"""
    pass

class FacemintService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or FACEMINT_API_KEY

    async def _request(self, method: str, path: str, json_payload: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Универсальный запрос с retry/backoff и таймаутами.
        Возвращает распарсенный JSON или бросает FacemintError.
        """
        if DEBUG or not self.api_key:
            logger.debug(f"FacemintService: DEBUG mode or missing API key -> returning mock response for {path}")
            await asyncio.sleep(0.2)
            # Моки в зависимости от endpoint
            if "faces-from-url" in path:
                return {"code": 0, "data": {"count": 1, "faces": [{"x": 10, "y": 20, "w": 100, "h": 100}]}}
            if "create-face-swap-task" in path:
                return {"code": 0, "data": {"task_id": "mock_task_123"}}
            if "get-task-info" in path:
                return {"code": 0, "data": {"status": "completed", "result_url": "https://example.com/result.gif"}}
            return {"code": 0, "data": {}}

        headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        attempt = 0
        backoff = 1.0
        while attempt < MAX_RETRIES:
            attempt += 1
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT, connect=CONNECT_TIMEOUT)
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    url = f"{BASE_URL}/{path.lstrip('/')}"
                    logger.debug(f"\n 🎸FacemintService request method={method} attempt={attempt} url={url} payload={json_payload} params={params}")
                    async with session.request(method=method.upper(), url=url, json=json_payload, params=params, headers=headers) as resp:
                        text = await resp.text()
                        status = resp.status
                        logger.debug(f"\nFacemintService response status={status} body={text}")
                        # try parse json
                        try:
                            data = await resp.json()
                        except Exception:
                            raise FacemintError(f"Invalid JSON from Facemint (status {status}): {text[:500]}")

                        # If HTTP status indicates retryable error -> backoff & retry
                        if status in RETRY_STATUSES:
                            logger.warning(f"FacemintService transient status {status}, attempt {attempt}")
                            if attempt < MAX_RETRIES:
                                await asyncio.sleep(backoff)
                                backoff *= 2
                                continue
                            else:
                                raise FacemintError(f"Facemint returned status {status}: {text[:200]}")

                        # Now check the API-level code inside JSON if present
                        # Facemint docs: assume {"code": 0, "data": {...}} means success
                        if isinstance(data, dict) and data.get("code") is not None:
                            if data.get("code") != 0:
                                # API-specific error
                                raise FacemintError(f"Facemint API error code {data.get('code')}: {data.get('message')}")
                            return data.get("data", {})
                        # If data doesn't have 'code', return raw JSON
                        return data
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.warning(f"FacemintService network error on attempt {attempt}: {e}")
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(backoff)
                    backoff *= 2
                    continue
                raise FacemintError(f"Network error: {e}") from e

        raise FacemintError("Max retries reached")

    # --- API methods (thin wrappers) ---

    async def faces_from_url(self, image_url: str) -> Dict[str, Any]:
        """Детекция лиц по URL — возвращает словарь с данными (count, faces)."""
        return await self._request("POST", "faces-from-url", json_payload={"url": image_url})

    async def create_face_swap_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Создание задачи face-swap. payload — согласно документации Facemint."""
        return await self._request("POST", "create-face-swap-task", json_payload=payload)

    async def get_task_info(self, task_id: str) -> Dict[str, Any]:
        """Получение статуса задачи."""
        return await self._request("POST", "get-task-info", json_payload={"task_id": task_id})

    async def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """Отмена задачи (если поддерживается API)."""
        return await self._request("POST", "cancel-task", json_payload={"task_id": task_id})
