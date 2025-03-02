document.addEventListener("DOMContentLoaded", () => {
    const searchJunctionInput = document.getElementById("searchJunctionInput");
    const junctionsFolder = document.getElementById("junctionsFolder");
    let allJunctions = []; // Store all junctions to filter later

    // Function to render junctions
    const renderJunctions = (junctions) => {
        junctionsFolder.innerHTML = "";

        junctions.forEach((junction) => {
            const junctionCard = document.createElement("div");
            junctionCard.className = "col";
            junctionCard.innerHTML = `
                <div class="card h-100" style="outline: 2px solid #2B7A78; background-color: #DEF2F1;">
                    <div class="card-body">
                        <h5 class="card-title">${junction.junctionname}</h5>
                    </div>
                </div>`;
            junctionsFolder.appendChild(junctionCard);
        });
    };

    // Fetch and display junctions on page load
    const fetchJunctions = async () => {
        const urlParams = new URLSearchParams(window.location.search);
        const modelId = urlParams.get("modelId");

        if (!modelId) {
            console.error("Missing modelId in URL");
            return;
        }

        try {
            const response = await fetch(`/api/junctions?modelId=${modelId}`);
            if (response.ok) {
                const junctions = await response.json();
                allJunctions = junctions; // Store fetched junctions
                renderJunctions(junctions);
            } else {
                console.error("Error fetching junctions:", await response.text());
            }
        } catch (error) {
            console.error("Error fetching junctions:", error);
        }
    };

    // Handle search input
    searchJunctionInput.addEventListener("input", () => {
        const searchQuery = searchJunctionInput.value.toLowerCase();
        const filteredJunctions = allJunctions.filter((junction) =>
            junction.junctionname.toLowerCase().includes(searchQuery)
        );
        renderJunctions(filteredJunctions);
    });

    // Initial fetch
    fetchJunctions();
});
