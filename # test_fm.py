# test_fm.py
import asyncio
from app.services.facemint_service import FacemintService

async def tst():
    svc = FacemintService(api_key="")
    res = await svc.faces_from_url("https://example.com/image.jpg")
    print("faces_from_url ->", res)
    task = await svc.create_face_swap_task({"dummy": "payload"})
    print("create_face_swap_task ->", task)
    info = await svc.get_task_info("mock_task_123")
    print("get_task_info ->", info)

asyncio.run(tst())
