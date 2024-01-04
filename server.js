const basicAuth = require('express-basic-auth')
const auth = basicAuth({ users: { 'admin': 'password' }, challenge: true,})


const http = require('http');
const url = require('url');
const querystring = require('querystring');
const fs = require('fs');


const express = require('express');
const bodyParser = require('body-parser');

const pug = require('pug');


const app = express();
app.set('views', 'templates');
app.set('view engine', 'pug');
const PORT = 4131;


let contacts = [["Jack", "jack@gmail.com", "2023-10-26", "Bonsai"]];
let nextId = 0;

function splitParameter(parameter) {
    const [k, v] = parameter.split("=");
    const kEscaped = decodeURIComponent(k);
    const vEscaped = decodeURIComponent(v);
    return [kEscaped, vEscaped];
}

function parseParameters(info) {
    const parameters = info.split("&");
    const kvPairs = parameters.map(splitParameter);
    const data = {};

    for (const [k, v] of kvPairs) {
        data[k] = v;
    }

    return data;
}

function addContactWithParameters(data) {
    const contact = [
        data["name"],
        data["email"],
        data["date"],
        data["service"],
        nextId
    ];

    contacts.push(contact);
    nextId++;
    console.log(contacts);
    return "";
}

function toHtmlTable(contacts) {
    let result = `
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
            <th>Delete Row</th>
        </tr>
    `;

    if (contacts.length === 0) {
        result += "</table>";
        return result;
    }

    for (const contact of contacts) {
        const [name, email, appointmentDate, service, id] = contact;
    
        const deleteButton = `<button onclick="deleteRow(this, ${id})">Delete</button>`;
    
        result += `
        <tr data-id="${id}">
            <th>${name}</th>
            <th>${email}</th>
            <th>${appointmentDate}</th>
            <th>${service}</th>
            <th>${deleteButton}</th>
        </tr>
        `;
    }

    result += `
    </table>
    <script>
        function deleteRow(button) {
            var row = button.parentNode.parentNode;
            row.parentNode.removeChild(row);
        }
    </script>
    `;

    return result;
}

function generateConfirmationHtml() {
    return `
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>My Contacts</title>
                <link rel ="stylesheet" type="text/css" href="/main.css">
                
                <style>
                    .add-entry-box {
                        border: 1px solid #ddd; 
                        background-color: #f9f9f9;
                        padding: 10px;
                        margin-top: 20px;
                    }
                    .add-entry-box form {
                        display: flex;
                        align-items: center;
                    }
                    .add-entry-box label {
                        margin-right: 10px;
                    }
                    .add-entry-box input {
                        padding: 5px;
                    }
                    .add-entry-box button {
                        padding: 5px 10px;
                    }
                </style>
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
                        ${toHtmlTable(contacts)}
                    </div>
                    
                    <div class="add-entry-box">
                        <form action="/admin/contactlog" method="get">
                            <label for="Sales banner">Sales Banner:</label>
                            <input type="text" id="SaleSet" name="newEntry">
                            <button type="submit">Set</button>
                            <button type="submit">Delete</button>
                        </form>
                    </div>
                </main>
            </body>
        </html>
    `;
}

app.delete('/api/contact', auth, (req, res) => {
    const { id } = req.body;
    const contactId = parseInt(id, 10);
    const index = contacts.findIndex(contact => contact[4] === contactId);

    if (index === -1) {
        res.status(404).send("Contact not found");
    } else {
        contacts.splice(index, 1);
        res.status(200).json({ id: contactId });
    }
});

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('templates/contactlog', (req, res) => {
    res.render(
        'contactlog'
      )
})

app.get('templates/contactform', (req, res) => {
    res.render(
        'contactform'
      )
})

app.get('/contact', (req, res) => {
    res.render(
        'contactform'
    )
})

app.get('/admin/contactlog', auth, (req, res) => {
    res.render('contactlog', { contacts: contacts });
});

app.post('/contact', (req, res) => {
const formData = req.body;
const requiredFields = ["name", "email", "date", "service"];

if (requiredFields.every(field => formData[field])) {
    contacts.push([formData.name, formData.email, formData.date, formData.service, nextId++]);
    // Redirecting to the contactlog page to avoid re-submission on refresh
    res.redirect('/admin/contactlog');
} else {
    res.status(400).send('Error: Missing required fields');
}
});



app.post('/contact', (req, res) => {
    const formData = req.body;
    const requiredFields = ["name", "email", "date", "service"];

    if (requiredFields.every(field => formData[field])) {
        contacts.push([formData.name, formData.email, formData.date, formData.service, nextId++]);
        res.redirect('/admin/contactlog');
    } else {
        res.status(400).send('Error: Missing required fields');
    }
});




app.post('/contactsuccess', (req, res) => {
    res.status(200);
})

  

app.get(['/main', '/'], (req, res) => {
    res.render('mainpage');
});

app.get('/testimonies', (req, res) => {
    res.render(
      'testimonies'
    )
  })

app.get('/css/main.css', (req, res) => {
    res.sendFile(__dirname + "/resources/css/main.css");
});

app.get('/js/main.js', (req, res) => {
    res.sendFile(__dirname + "/resources/js/main.js");
});

app.get('/js/table.js', (req, res) => {
    res.sendFile(__dirname + "/resources/js/table.js");
});

app.get('/images/main', (req, res) => {
    res.sendFile(__dirname + "/resources/images/Tree.jpeg");
});

app.use((req, res) => {
    res.sendFile(__dirname + "/templates/404.pug");
});

app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}/`);
});


app.use('*', (req, res) => {
    res.status(404).send('Resource not found');
});