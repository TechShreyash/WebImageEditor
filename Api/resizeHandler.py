import requests


def resizeImage(fileUrl, height, width, hash):
    url = f"https://wsrv.nl/?w={width}&h={height}&fit=inside&url={fileUrl}"
    response = requests.get(url)
    file = response.content

    with open(f"/tmp/resized{hash}", "wb") as f:
        f.write(file)

    return f"resized{hash}"
