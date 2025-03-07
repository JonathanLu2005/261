document.addEventListener("DOMContentLoaded", () => {
    const junctionsFolder = document.getElementById("junctionsFolder");

    // Fetch the model ID dynamically (e.g., from a hidden input, a global variable, or URL)
    const modelId = getModelId();

    // Fetch and populate junction cards dynamically
    async function fetchJunctions() {
        const response = await fetch(`/api/junctions?modelId=${modelId}`);
        const junctions = await response.json();

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

    // Attach click event listeners to junction cards
    function attachCardListeners() {
        const junctionCards = document.querySelectorAll(".junction-card");
        junctionCards.forEach((card) => {
            card.addEventListener("click", () => {
                const junctionId = card.getAttribute("data-junctionid");

                // Send data to backend
                sendJunctionDataToBackend(modelId, junctionId);
            });
        });
    }

    // Send the modelId and junctionId to the backend
    async function sendJunctionDataToBackend(modelId, junctionId) {
        const response = await fetch(`/api/receiveJunctionData`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ modelId, junctionId }),
        });

        if (response.ok) {
            console.log("Data sent successfully to backend");
        } else {
            console.error("Failed to send data to backend");
        }
    }

    // Function to dynamically get the model ID
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
