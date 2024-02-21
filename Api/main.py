from werkzeug.utils import secure_filename
import os
from aiohttp import web
from fileHandler import allowed_file, get_file_details, get_file_hash
import aiohttp_cors

from resizeHandler import resizeImage

app = web.Application()
url = "http://127.0.0.1:8080"

routes = web.RouteTableDef()

cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True, expose_headers="*", allow_headers="*"
        )
    },
)


@routes.post("/upload")
async def upload_file(request):
    reader = await request.multipart()
    field = await reader.next()
    filename = field.filename

    if field is None:
        return web.Response(
            text="No file uploaded.",
            status=400,
            content_type="text/plain",
        )
    print(filename)
    if allowed_file(filename):
        if filename == "":
            return web.Response(
                text="No file selected.", content_type="text/plain", status=400
            )

        filename = secure_filename(filename)
        extension = filename.rsplit(".", 1)[1]
        hash = get_file_hash()

        try:
            with open(
                os.path.join("/tmp/uploads", hash + "." + extension), "wb"
            ) as f:
                while True:
                    chunk = await field.read_chunk()
                    if not chunk:
                        break
                    f.write(chunk)
        except Exception as e:
            return web.Response(
                text=f"Error saving file: {str(e)}",
                status=400,
                content_type="text/plain",
            )

        try:
            width, height = get_file_details(
                os.path.join("/tmp/uploads", hash + "." + extension)
            )
        except Exception as e:
            os.remove(os.path.join("/tmp/uploads", hash + "." + extension))
            return web.Response(
                text=f"Error getting file details: {str(e)}",
                status=400,
                content_type="text/plain",
            )

        text = f"{hash}.{extension};{width};{height}"

        return web.Response(text=text, content_type="text/plain", status=200)
    else:
        return web.Response(
            text="File type not allowed", status=400, content_type="text/plain"
        )


@routes.get("/uploads/{file}")
async def tmp_files(request):
    return web.FileResponse(f"/tmp/{request.match_info['file']}")


@routes.get("/resize")
async def resize_image(request):
    request_params = request.rel_url.query
    file = request_params.get("file")
    width = request_params.get("width")
    height = request_params.get("height")

    fileUrl = f"{url}/uploads/{file}"
    image = resizeImage(fileUrl, height, width, file)

    imageUrl = f"{url}/uploads/{image}"
    return web.Response(
        text=imageUrl,
        content_type="text/plain",
        status=200,
    )


@routes.get("/")
async def index(request):
    return web.Response(text="Working", content_type="text/plain", status=200)


app.add_routes(routes)

for route in list(app.router.routes()):
    cors.add(route)


if __name__ == "__main__":  
    web.run_app(app)
