# Flask-first-project

## Install venv
```
python3 -m venv venv
```
## Acrivate venv
```
source venv/bin/activate
```
## Install requirements
```
pip install -r requirements.txt
```
## Start tests
```
pytest tests
```
## Start the project
```
flask --app main run
```
## Start the project with debug
```
flask --app main run --debug
```
## Open project
```
http://127.0.0.1:5000
```
## Status codes
An HTTP status code is a message a website 's server sends to the browser to indicate whether or not that request can be fulfilled. 
### List of status codes:
![photo_2023-02-23_12-17-53](https://user-images.githubusercontent.com/118758739/220894856-2a3bf5f1-897b-42e3-baa7-9eb39a4bdb4d.jpg)


## HTTP requests
**Idempotent** is a funny word that often throws people off track. Idempotence sometimes seems like a confusing concept, at least when judged by the academic definition. From the point of view of a RESTful service, an operation (or service call) is idempotent when clients can make the same call repeatedly with the same result, working as a "setter" in the programming language. In other words, creating a large number of identical requests has the same effect as a single request. Note that while idempotent operations produce the same result on the server (side effects), the response itself may not be the same (for example, the state of the resource may change between requests).

-	GET - The GET method is used to retrieve information from the given server using a given URI. Requests using GET should only retrieve data and should have no   other effect on the data.

-	HEAD - Same as GET, but it transfers the status line and the header section only.

- PATCH - partial change.

-	POST - A POST request is used to send data to the server, for example, customer information, file upload, etc. using HTML forms.

-	PUT - Replaces all the current representations of the target resource with the uploaded content.

-	DELETE - Removes all the current representations of the target resource given by URI.

-	CONNECT - Establishes a tunnel to the server identified by a given URI.

-	OPTIONS - Describe the communication options for the target resource.

-	TRACE - Performs a message loop back test along with the path to the target resource.

## HTTP vs HTTPS
What Is HTTP?
- Hypertext Transfer Protocol (HTTP) transfers data from a web server to your browser so that it can access and load websites. 

What Is HTTPS?
 - HTTPS is the acronym for Hypertext Transfer Protocol Secure. Like HTTP, its main purpose is to transfer data from a server to your browser, so you can load websites. 
However, HTTPS uses an encrypted connection to communicate between the server and the browser. A SSL (secure sockets layer) certificate protects the transferred data from being stolen as it’s exchanged. 

## REST and RESTful
### 1. Uniform Interface
By applying the principle of generality to the components interface, we can simplify the overall system architecture and improve the visibility of interactions.

Multiple architectural constraints help in obtaining a uniform interface and guiding the behavior of components.

The following four constraints can achieve a uniform REST interface:

- Identification of resources – The interface must uniquely identify each resource involved in the interaction between the client and the server.

- Manipulation of resources through representations – The resources should have uniform representations in the server response. API consumers should use these representations to modify the resources state in the server.

- Self-descriptive messages – Each resource representation should carry enough information to describe how to process the message. It should also provide information of the additional actions that the client can perform on the resource.

- Hypermedia as the engine of application state – The client should have only the initial URI of the application. The client application should dynamically drive all other resources and interactions with the use of hyperlinks.

### 2. Client-Server
The client-server design pattern enforces the separation of concerns, which helps the client and the server components evolve independently.

By separating the user interface concerns (client) from the data storage concerns (server), we improve the portability of the user interface across multiple platforms and improve scalability by simplifying the server components.

While the client and the server evolve, we have to make sure that the interface/contract between the client and the server does not break.

### 3. Stateless
Statelessness mandates that each request from the client to the server must contain all of the information necessary to understand and complete the request.

The server cannot take advantage of any previously stored context information on the server.

For this reason, the client application must entirely keep the session state.

### 4. Cacheable
The cacheable constraint requires that a response should implicitly or explicitly label itself as cacheable or non-cacheable.

If the response is cacheable, the client application gets the right to reuse the response data later for equivalent requests and a specified period.

### 5. Layered System
The layered system style allows an architecture to be composed of hierarchical layers by constraining component behavior.

For example, in a layered system, each component cannot see beyond the immediate layer they are interacting with.

### 6. Code on Demand (Optional)
REST also allows client functionality to extend by downloading and executing code in the form of applets or scripts.

The downloaded code simplifies clients by reducing the number of features required to be pre-implemented. Servers can provide part of features delivered to the client in the form of code, and the client only needs to execute the code.
