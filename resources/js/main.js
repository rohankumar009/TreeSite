const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', toggleTheme);

function toggleTheme() {
    const body = document.body;
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
    } else {
        body.classList.add('dark-mode');
    }
}

function getAuthHeaders() {
    const username = 'admin';
    const password = 'password';
    return new Headers({
      'Authorization': 'Basic ' + btoa(username + ":" + password),
      'Content-Type': 'application/json'
    });
}

async function saleGet(){
        const response = await fetch("api/sale", {method: "GET"})
        const message_obj = await response.json();
        if (message_obj.active) {
            // get the sale banner and set text message to message_obj
            const sale = document.getElementById('Sale Banner')
            sale.innerText = message_obj.message
            sale.style.display = "block";
        }
        else {
            // Hide Sale banner
            sale.style.display = "none";
        }

}

async function saleSet(message) {
    const username = 'admin';
    const password = 'password';
    const headers = new Headers({
      'Authorization': 'Basic ' + btoa(username + ":" + password),
      'Content-Type': 'application/json'
    });
  
    try {
      const response = await fetch("/api/sale", {
        method: "POST",
        headers: headers,
        body: JSON.stringify({ message: message })
      });
  
      if (response.ok) {
      } else {
        console.error('Failed to set the sale banner with status:', response.status);
      }
    } catch (error) {
      console.error('Error during fetch:', error);
    }
  }

async function saleDelete() {
    const username = 'admin';
    const password = 'password';
    const headers = new Headers({
      'Authorization': 'Basic ' + btoa(username + ":" + password)
    });
  
    try {
      const response = await fetch("/api/sale", {
        method: "DELETE",
        headers: headers
      });
  
      if (response.ok) {
      } else {
        console.error('Failed to delete the sale banner with status:', response.status);
      }
    } catch (error) {
      console.error('Error during fetch:', error);
    }
  }