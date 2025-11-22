from aiohttp import web


async def handle(request):
    path = request.match_info.get("filename", "index.html")
    return web.FileResponse(f"./site/{path}")


if __name__ == "__main__":
    app = web.Application()
    app.router.add_get("/", handle)
    app.router.add_get("/{filename:.*}", handle)

    web.run_app(app, port=8000)
