import re
import os
import base64

FORMAT = 'latin_1'


# returns the host given a uri
# is not a fully functional parses, but functional within the scope of this project
# remove 'http:// from uri
# host = everything before the first '/'
# e.g. http://www.example.com/hello.html -> www.example.com

def get_host_from_uri(uri: str) -> str:
    uri = uri.replace('http://', '')
    host = uri.partition('/')[0]
    return host


# returns the path given a uri
# is not a fully functional parses, but functional within the scope of this project
# remove 'http:// from uri
# path = everything after the first '/'
# e.g. http://www.example.com/hello.html -> /hello.html

def get_path_from_uri(uri: str) -> str:
    uri = uri.replace('http://', '')
    path = uri.partition('/')[2]
    return path


def write_html(body: str) -> None:
    print('Writing body to body.html')
    # create output folder if it does not exist.
    if not os.path.isdir('output/'):
        os.makedirs('output/')
    html_file = open("output/body.html", "w+")
    html_file.write(body)
    html_file.close()
    print('Done!\r\n')


def write_image(img: str, path: str) -> None:
    # get dir for image:
    dir = '/'.join(path.split('/')[0:-1])
    if not os.path.isdir('output/' + dir):
        os.makedirs('output/' + dir)
    file = open('output/' + path, "wb+")
    file.write(img)
    file.close()


def get_image_paths_from_html(body: str) -> list:
    print("Searching for images")
    tags = re.findall('<img.*?>', body)  # regular expression looking for images
    print(len(tags), 'images found')

    # Get image paths
    paths: list[str] = []
    for tag in tags:
        result = re.findall('src="/.*?"', tag)
        if len(result) == 0:
            # src might not start with a /
            result = re.findall('src=".*?"', tag)
            if len(result) == 0:
                # img does not contain src tag
                print("no source found for image")
            path = result[0][5:-1]
        else:

            # src path starts with '/' -> points to root dir
            # change path in html file by remove this '/'
            new_tag = tag.replace('src="/', 'src="')
            new_body = body.replace(tag, new_tag)
            path = result[0][6:-1]
            write_html(new_body)
        paths.append(path)

    return paths


COMMAND_INDEX: int = 0
URI_INDEX: int = 1
PORT_INDEX: int = 2