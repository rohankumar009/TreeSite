const dropdown = document.getElementById('dropdown');
        const dollarValue = document.getElementById('dollarValue');

        dropdown.addEventListener('change', function() {
            const selectedOption = dropdown.options[dropdown.selectedIndex];
            const value = selectedOption.value;
            dollarValue.value = '$' + value;
        });