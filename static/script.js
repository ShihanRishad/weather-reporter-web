document
  .getElementById("getWeatherButton")
  .addEventListener("click", function () {
    const city = document.getElementById("city").value;

    fetch("/weather", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "city=" + encodeURIComponent(city),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json(); // Read the response body once
      })
      .then((data) => {
        document.getElementById("weatherReportContent").textContent =
          data.report;
        document.getElementById("weatherReport").style.display = "block";
      })
      .catch((error) => {
        console.error("Error:", error);
        document.getElementById("weatherReportContent").textContent =
          "Error fetching weather report.";
        document.getElementById("weatherReport").style.display = "block";
      });
  });
