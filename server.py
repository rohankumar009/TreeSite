from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import urllib

"""
Tried my best to get the server to work. It was not really working the remaining times that it was just result in a 404 error or say that the data is not being sent, 
I did open the pages individually, and I was able to get all the pages to work, so they do work just not through the local host
"""

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
            <th>Date</th>
            <th>Straight Cash Homie?</th>
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

# PUT YOUR GLOBAL VARIABLES AND HELPER FUNCTIONS HERE.
#contact_log = [
#     {"name": "John Doe", "email": "johndoe@example.com", "date": "2023-10-20", "service": "general"},
#]
# It is not required, but is is strongly recommended that you write a function to parse form data out of the URL, and a second function for generating the contact log page html.


# Takes the query and returns a list containing the requested file and the parameters.
"""
def process_form_data(query_params):
    
    # Check query_params for the ?. If exists, need to return list with first element being the file, and second element the 'name'
    if ('?' in query_params):
        url_split = query_params.split("?")
        url_split[1] = url_split[1][5:]
        return url_split
    else:
        return [query_params]

def generate_contact_log_html():
    table = "<table>"
    for contact in contact_log:
        table += f"<tr><td>Name: {contact['name']}</td><td>Email: {contact['email']}</td><td>Date: {contact['date']}</td><td>Service: {contact['service']}</td></tr>"
    table += "</table>"
    return table
"""
def server(url):
    """
    url is a *PARTIAL* URL. If the browser requests `http://localhost:4131/contact?name=joe#test`
    then the `url` parameter will have the value "/contact?name=joe". So you can expect the PATH
    and any PARAMETERS from the url, but nothing else.

    This function is called each time another program/computer makes a request to this website.
    The URL represents the requested file.

    This function should return two strings in a list or tuple. The first is the content to return
    The second is the content-type.
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
        return open("static/html/contactform.html").read(), "text/html; charset= utf-8"
    elif url == "/main" or url == "/":
        return open("static/html/mainpage.html").read(), "text/html; charset= utf-8"
    elif url == "/testimonies":
        return open("static/html/testimonies.html").read(), "text/html; charset= utf-8"
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
                                        <th>Preferred Appointment Day</th>
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
        return open("static/css/main.css").read(), "text/css"
    elif url == "/images/main":
        return open("static/images/Tree.jpeg", "br").read(), "image/jpeg"
    else:
        return open("static/html/404.html").read(), "text/html: charset=utf-8"
    




    # url_to_file = {
    #     "/": "static/html/mainpage.html",
    #     "/main": "static/html/mainpage.html",
    #     "/contact": "static/html/contactform.html",
    #     "/testimonies": "static/html/testimonies.html",
    #     "/admin/contactlog": "static/html/contactlog.html",
    #     "/main.css": "static/css/main.css",
    #     "/images/main": "static/images/Tree.jpeg"
    # }

    # parsed_message = process_form_data(url)
    # if len(parsed_message) == 1:
    #     extension = url_to_file[parsed_message[0]].split(".")[1]
    #     file_type = "text/html"
    #     if extension == "html":
    #         file_type = "text/html"
    #     elif extension == "css":
    #         file_type = "text/css"
    #     return (open(url_to_file[parsed_message[0]], "rb").read(), file_type)
    
    # return (open("static/html/mainpage.html").read(), "text/html")
    

    # return open("static/html/mainpage.html").read(), "main/html"
    # return open("static/html/testimonies.html").read(), "testimonies/html"
    # return open("static/html/contact.html").read(), "contact/html"
    # return open("static/html/contactlist.html").read(), "contactlist/html"
    # return open("static/html/mainpage.html").read(), "main/html"
    # return open("static/html/mainpage.html").read(), "main/html"


# You shouldn't need to change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the student-edited server code.
        message, content_type = server(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(200)
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
    server = ('', PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
