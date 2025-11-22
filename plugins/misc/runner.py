import asyncio

from aiohttp import web


async def handle(request):
    path = request.match_info.get("filename", "index.html")
    return web.FileResponse(f"./site/{path}")


app = web.Application()
app.router.add_get("/", handle)
app.router.add_get("/{filename:.*}", handle)

if __name__ == "__main__":
    web.run_app(app, port=8000)
