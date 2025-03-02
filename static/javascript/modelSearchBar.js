document.addEventListener("DOMContentLoaded", async () => {
    const modelsFolder = document.getElementById("modelsFolder");
    const searchInput = document.getElementById("searchInput");

    let allModels = []; // Store all models to filter dynamically

    function renderModels(models) {
        modelsFolder.innerHTML = "";

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

    async function fetchModels() {
        try {
            const response = await fetch("/api/models");
            allModels = await response.json();
            renderModels(allModels);
        } catch (error) {
            console.error("Error fetching models:", error);
        }
    }

    function filterModels(query) {
        const filteredModels = allModels.filter((model) =>
            model.name.toLowerCase().includes(query.toLowerCase())
        );
        renderModels(filteredModels);
    }

    // Fetch models on page load
    await fetchModels();

    // Add event listener for the search input
    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.trim();
        filterModels(query);
    });
});
