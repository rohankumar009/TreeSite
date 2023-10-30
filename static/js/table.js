function deleteRow(button) {
    var row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}


function updateCountdown() {
    var now = new Date();
    dateCells.forEach(function (cell) {
        var appointmentDate = new Date(cell.getAttribute('data-date'));
        var timeDifference = appointmentDate - now;
        if (timeDifference > 0) {
            var days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
            var hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
            cell.innerHTML = days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's';
        } else {
            cell.innerHTML = 'PAST';
        }
    });
}

setInterval(updateCountdown, 1000);