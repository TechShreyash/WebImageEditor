import requests


def resizeImage(fileUrl, height, width, hash):
    url = f"https://wsrv.nl/?url={fileUrl}&w={width}&h={height}"
    response = requests.get(url)
    file = response.content

    with open(f"/tmp/resized{hash}", "wb") as f:
        f.write(file)

    return f"resized{hash}"


# a = resizeImage('https://image-editor-api.vercel.app/uploads/EdO1dCSJlj.jpg',600,600,'EdO1dCSJlj.jpg')
# with open('resizedEdO1dCSJlj.jpg','wb') as f:
#     f.write(a)
