# demo flask app

import os
from flask import Flask, request, send_file, Response
from fileHandler import allowed_file, get_file_details, get_file_hash, get_file_size
from werkzeug.utils import secure_filename
from resizeHandler import resizeImage

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

url = "https://image-editor-api.vercel.app"


@app.route("/uploads/<file>")
@cross_origin()
def tmp_files(file):
    return send_file(f"/tmp/{file}",as_attachment=True)


@app.route("/resize")
@cross_origin()
def resize_image():
    file = request.args.get("file")
    width = request.args.get("width")
    height = request.args.get("height")

    image = resizeImage(height, width, file)
    imageUrl = f"{url}/uploads/{image}"
    size = get_file_size(f"/tmp/{image}")
    return f"{imageUrl};{image};{size}"


@app.route("/")
def index():
    return "Working"


@app.route("/upload", methods=["POST"])
@cross_origin()
def upload_file():
    file = request.files["file"]
    filename = file.filename

    if allowed_file(filename):
        filename = secure_filename(filename)
        extension = filename.rsplit(".", 1)[1]
        hash = get_file_hash()

        file.save(f"/tmp/{hash}.{extension}")

        try:
            width, height = get_file_details(f"/tmp/{hash}.{extension}")
        except Exception as e:
            os.remove(f"/tmp/{hash}.{extension}")
            return Response(
                f"Error getting file details: {str(e)}",
                status=400,
                content_type="text/plain",
            )

        text = f"{hash}.{extension};{width};{height}"
        return Response(text, content_type="text/plain", status=200)
    else:
        return Response("File type not allowed", status=400, content_type="text/plain")
