let clickCount = 0;    // Count of clicks
let lastClickTime = 0; // Time of last time clicked the button
var city = document.querySelector('#city');

function report() {
    const now = Date.now();
        // Stop multiple clicks within 4 seconds for safety
        if (now - lastClickTime < 480*30) {
            clickCount++;
            if (clickCount >= 2) {
                console.log("Please wait a moment before clicking again.");
                return;  // Ignore click if too frequent
            }
        } else {
            clickCount = 1;  // Reset click count if more than 4 seconds have passed
        }
    
        lastClickTime = now;  // Update last click time
        this.disabled = true; // Disable the button
    
        const city = document.getElementById('city').value;
    
        fetch('/weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'city=' + encodeURIComponent(city)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('weatherReport').style.display = 'block';
    
            // Display the report content using TypeWave from the external script
            const element = document.getElementById('weatherReportContent');
            console.log(data.report.length)
            TypeWave(element, data.report, 30);  // Call external TypeWave function
    
            // Display the SVG QR code
            const svgContainer = document.getElementById('qrCode');
            svgContainer.innerHTML = data.qr_code_image;
            svgContainer.style.display = "block";
    
            // Re-enable the button after TypeWave estimated duration (delay * text length)
            const typewaveDuration = data.report.length * 30; 
            setTimeout(() => {
                document.getElementById('getWeatherButton').disabled = false;
            }, typewaveDuration);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('qrCode').style.display = 'none';
            document.getElementById('getWeatherButton').disabled = false;  // Re-enable in case of an error
        });

}

document.getElementById('getWeatherButton').addEventListener('click', report);

let span = document.querySelector("#getWeatherButton span")
let inputcity = document.querySelector("#city");
inputcity.addEventListener("focus", function() {
    this.style.width = "100%";
    span.style.opacity = "0";
    span.style.fontSize = "0%";
});
inputcity.addEventListener("blur", function() {
    this.style.width = "54%";
    span.style.opacity = "1";
    span.style.fontSize = "100%";
});

city.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') { // Handle keyboard event
      report()
    }
  });

/*
Add this if no internet:

function TypeWave(element, text, delay = 100) {
    let index = 0;
    element.textContent = "";

    function type() {
        if (index < text.length) {
            element.textContent += text[index];
            index++;
            setTimeout(type, delay);
        }
    }

    type();
}
*/