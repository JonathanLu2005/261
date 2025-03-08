/* JS for model page */
document.addEventListener("DOMContentLoaded", async () => {
    /* Get model folder and input */
    const modelsFolder = document.getElementById("modelsFolder");
    const searchInput = document.getElementById("searchInput");
    let allModels = []; 

    /* Render models to frontend */
    function renderModels(models) {
        modelsFolder.innerHTML = "";

        /* Provide card style for each model */
        models.forEach((model) => {
            const modelCard = document.createElement("div");
            modelCard.className = "col";
            modelCard.innerHTML = `
                <div class="card h-100 model-card" data-id="${model.id}" data-name="${model.name}" style="outline: 2px solid #2B7A78; background-color: #DEF2F1;">
                    <div class="card-body">
                        <h5 class="card-title">${model.name}</h5>
                    </div>
                </div>`;
            modelsFolder.appendChild(modelCard);
        });
    }

    /* Get all models from backend to render */
    async function fetchModels() {
        try {
            const response = await fetch("/api/models");
            allModels = await response.json();
            renderModels(allModels);
        } catch (error) {
            console.error("Error fetching models:", error);
        }
    }

    /* Get all models that have similar name to query and render the filtered models */
    function filterModels(query) {
        const filteredModels = allModels.filter((model) =>
            model.name.toLowerCase().includes(query.toLowerCase())
        );
        renderModels(filteredModels);
    }

    /* Render models when page loads */
    await fetchModels();

    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.trim();
        filterModels(query);
    });
});
