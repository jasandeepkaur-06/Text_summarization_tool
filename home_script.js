function summarizeText() {

    var text = document.getElementById("inputText").value;

    fetch("/summarize", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "text=" + encodeURIComponent(text)
    })
    .then(response => response.json())
    .then(data => {

        if (data.error) {
            document.getElementById("summaryOutput").innerText = data.error;
        } else {
            document.getElementById("summaryOutput").innerText = data.summary;
        }

    })
    .catch(error => {
        document.getElementById("summaryOutput").innerText = "Error generating summary.";
    });
}