import re

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


def write_html(body):
    print('Writing body to body.html')
    html_file = open("body.html", "w")
    html_file.write(body)
    html_file.close()
    print('Done!\r\n')



def get_image_paths_from_html(body):
    print("Searching for images")
    tags = re.findall('<img.*?>', body)  # regular expression looking for images
    print(len(tags), 'images found')

    for tag in tags:
        result = re.findall('src="/.*?"', tag)
        path = result[0][6:-1]


COMMAND_INDEX: int = 0
URI_INDEX: int = 1
PORT_INDEX: int = 2