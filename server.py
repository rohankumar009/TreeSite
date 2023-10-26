from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

contacts = [["test", "test@gmail.com", "2023-10-24", "Haircut", "No"]]

def split_parameter(parameter):
    k, v = parameter.split("=", 1)
    k_escaped = urllib.parse.unquote(k)
    v_escaped = urllib.parse.unquote(v)
    return k_escaped, v_escaped


def split_url(info):
    parameters = info.split("&")
    
    kv_pairs = [split_parameter(x) for x in parameters]
    data = {}

    for k,v in kv_pairs:
        data[k] = v

    data["cash"] = "Yes" if "cash" in data else "No"

    contact = [
        data["name"],
        data["email"],
        data["date"],
        data["cash"]

    ]

    contacts.append(contact) # adding contact to contact list
    print(contacts)
    return ""


def to_html_table(contacts):

    result = """
    <style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
    <table> 
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Appointment Day</th>
            <th>Service</th>
            <th>Paying w/ Cash</th>
            <th>Delete Row</th>
        </tr>
    """

    if len(contacts) == 0:
        result += "</table>"
        return result
    else:
        for contact in contacts:
            name = contact[0]
            email = contact[1]
            appointment_date = contact[2]
            cash = contact[3]
            result += """
            <tr>
                <th>""" + name + """</th>
                <th>""" + email + """</th>
                <th>""" + appointment_date + """</th>
                <th>""" + cash + """</th>
            </tr>
            """

        result += "</table>"

        return result

def server_GET(url: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    #YOUR CODE GOES HERE!

    parameters = None
    if "?" in url:
        ind = url.index("?")
        parameters = url[ind + 1 :]
        url = url[:ind]

    if url == "/contact":
        if parameters is not None:
            split_url(parameters)
        return open("static/html/contactform.html").read(), "text/html; charset= utf-8", 200
    elif url == "/main" or url == "/":
        return open("static/html/mainpage.html").read(), "text/html; charset= utf-8", 200
    elif url == "/testimonies":
        return open("static/html/testimonies.html").read(), "text/html; charset= utf-8", 200
    elif url == "/admin/contactlog":
        return (
            """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>My Contacts</title>
                    <link rel ="stylesheet" type="text/css" href="/main.css">
                </head>

                <body>
                    <header>
                        <nav>
                            <a href="/">My Company</a>
                            <a href="/testimonies">Testimonials</a>
                            <a href="/contact">Contact Us</a>
                            <a href="/admin/contactlog">Contacts</a>
                        </nav>
                    </header>

                    <main id="Appointments">
                        <h1>My Contacts and Appointments</h1>
                        <div>
                            <table>
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Email</th>
                                        <th>Appointment Day</th>
                                        <th>Service</th>
                                        <th>Paying with Cash</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    """
                + to_html_table(contacts)
                + """
                                </tbody>
                                </table>
                            </table>
                        </div>
                    </main>
                </body>
            </html>
                            """,
            "text/html; charset=utf-8"
        )
    elif url == "/main.css":
        return open("static/css/main.css").read(), "text/css", 200
    elif url == "/images/main":
        return open("static/images/Tree.jpeg", "br").read(), "image/jpeg", 200
    else:
        return open("static/html/404.html").read(), "text/html: charset=utf-8", 404
    


def server_POST(url: str, body: str) -> tuple[str | bytes, str, int]:
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe". (so the schema and
    authority will not be included, but the full path, any query, and any anchor will be included)

    This function is called each time another program/computer makes a POST request to this website.

    This function should return three values (string or bytes, string, int) in a list or tuple. The first is the content to return
    The second is the content-type. The third is the HTTP Status Code for the response
    """
    if url == "/contact":        
        print("this is a body")
        split_url(body)
        print(body)
        return open("static/css/main.css").read(), "text/css", 200
    else:
        return open("static/html/404.html").read(), "text/html: charset=utf-8", 404

# You shouldn't need to change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get('Content-Length',0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")

        message, content_type, response_code = server_POST(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

    def do_GET(self):
        # Call the student-edited server code.
        message, content_type, response_code = server_GET(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(response_code)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
