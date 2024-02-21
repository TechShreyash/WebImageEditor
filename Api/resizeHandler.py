import requests


def resizeImage(fileUrl, height, width, hash):
    url = f"https://wsrv.nl/?url={fileUrl}&w={width}&h={height}"
    response = requests.get(url)
    file = response.content

    with open(f"/tmp/resized{hash}", "wb") as f:
        f.write(file)
    
    return file
    return f"resized{hash}"
