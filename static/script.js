document.getElementById('getWeatherButton').addEventListener('click', function() {
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
      document.getElementById('weatherReportContent').textContent = data.report;
      document.getElementById('weatherReport').style.display = 'block';
      
      const qrCodeImage = new Image();
      qrCodeImage.src = 'data:image/svg+xml;base64,' + btoa(data.qr_code_image);
      document.getElementById('qrCode').appendChild(qrCodeImage);
      document.getElementById('qrCode').style.display = 'block';
  })
  .catch(error => {
      console.error('Error:', error);
      document.getElementById('qrCode').style.display = 'none';
  });
});
