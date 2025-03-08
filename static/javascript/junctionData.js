/* JS for junction page, sends model and junction id to backend for visualisations */
document.addEventListener("DOMContentLoaded", () => {
    /* Get junction folder */
    const junctionsFolder = document.getElementById("junctionsFolder");

    /* Get model id */
    const modelId = getModelId();

    async function fetchJunctions() {
        /* Fetches and render junctions on frontend */
        const response = await fetch(`/api/junctions?modelId=${modelId}`);
        const junctions = await response.json();
        
        /* Render junctions to frontend */
        junctionsFolder.innerHTML = junctions
            .map(
                (junction) => `
                <div class="col">
                    <div 
                        class="card junction-card" 
                        data-junctionid="${junction.junctionid}" 
                        data-modelid="${modelId}" 
                        style="cursor: pointer; border: 2px solid #2B7A78;"
                    >
                        <div class="card-body">
                            <h5 class="card-title">${junction.junctionname}</h5>
                        </div>
                    </div>
                </div>
            `
            )
            .join("");

        attachCardListeners();
    }

    /* When junction is clicked, able send its model and junction id to backend */
    function attachCardListeners() {
        const junctionCards = document.querySelectorAll(".junction-card");
        junctionCards.forEach((card) => {
            card.addEventListener("click", () => {
                const junctionId = card.getAttribute("data-junctionid");
                sendJunctionDataToBackend(modelId, junctionId);
            });
        });
    }

    /* Sends model id and junction to backend */
    async function sendJunctionDataToBackend(modelId, junctionId) {
        const response = await fetch(`/api/receiveJunctionData`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ modelId, junctionId }),
        });

        if (response.ok) {
            const data = await response.json(); 
            console.log("Data sent successfully to backend");
            if (data.image_path) { 
                console.log(data.image_path)
                document.querySelector("junctionImage").src = data.image_path;
        }
        } else {
            console.error("Failed to send data to backend");
        }
    }

    /* Use URL to get model id */
    function getModelId() {
        const urlParams = new URLSearchParams(window.location.search);
        const modelId = urlParams.get("modelId");

        if (!modelId) {
            console.error("Model ID not found in the URL or context.");
            return null;
        }

        return modelId;
    }

    if (modelId) {
        fetchJunctions();
    }
});
