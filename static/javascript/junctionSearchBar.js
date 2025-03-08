/* JS for junction page */
document.addEventListener("DOMContentLoaded", () => {
    /* Get junction input and where all the junctions are stored */
    const searchJunctionInput = document.getElementById("searchJunctionInput");
    const junctionsFolder = document.getElementById("junctionsFolder");
    let allJunctions = []; 

    /* Render junctions */
    const renderJunctions = (junctions) => {
        junctionsFolder.innerHTML = "";

        /* Cards to render junctions */
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

    /* Display filtered junctions */
    const fetchJunctions = async () => {
        /* Get model id */
        const urlParams = new URLSearchParams(window.location.search);
        const modelId = urlParams.get("modelId");

        if (!modelId) {
            console.error("Missing modelId in URL");
            return;
        }

        try {
            /* Get junctions from backend and render junctions */
            const response = await fetch(`/api/junctions?modelId=${modelId}`);
            if (response.ok) {
                const junctions = await response.json();
                allJunctions = junctions;
                renderJunctions(junctions);
            } else {
                console.error("Error fetching junctions:", await response.text());
            }
        } catch (error) {
            console.error("Error fetching junctions:", error);
        }
    };

    /* Given name, will provide junctions with similar junction names */
    searchJunctionInput.addEventListener("input", () => {
        const searchQuery = searchJunctionInput.value.toLowerCase();
        const filteredJunctions = allJunctions.filter((junction) =>
            junction.junctionname.toLowerCase().includes(searchQuery)
        );

        /* Then render junctions specifically with those filtered names */
        renderJunctions(filteredJunctions);
    });

    fetchJunctions();
});
