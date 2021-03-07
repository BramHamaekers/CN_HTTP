# CN_lab1
A python CLI HTTP client and server application written for a lab assignment for the Computer Networks (G0Q43A) course at KU Leuven. (2020-2021)
The client can send get, head, post and put requests to a given http server given a port.
With post and put requests, a custom message can be sent.
Both fixed-length and chunked responses can be read.

Client writes its output to an output folder.

The server should be multi-threaded to support multiple clients at the same time.
The server supports the following client operations: HEAD, GET, PUT and POST.
server supports the 'if-modified-since' HTTP header
