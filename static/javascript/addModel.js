document.addEventListener("DOMContentLoaded", async () => {
    const modelForm = document.getElementById("addModelForm");
    const modelsFolder = document.getElementById("modelsFolder");

    // Function to render models
    const renderModels = (models) => {
        // Clear existing models
        modelsFolder.innerHTML = "";

        // Render each model
        models.forEach((model) => {
            const modelCard = document.createElement("div");
            modelCard.className = "col";
            modelCard.innerHTML = `
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${model.name}</h5>
                    </div>
                </div>`;
            modelsFolder.appendChild(modelCard);
        });
    };

    // Fetch and display models on page load
    try {
        const response = await fetch("/api/models");
        const models = await response.json();
        renderModels(models);
    } catch (error) {
        console.error("Error fetching models:", error);
    }

    // Handle form submission
    modelForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const modelFormData = new FormData(modelForm);
        const modelData = Object.fromEntries(modelFormData);

        try {
            const response = await fetch("/addModel", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(modelData),
            });

            if (response.ok) {
                const updatedModels = await response.json();
                renderModels(updatedModels);

                // Reset form and close modal
                modelForm.reset();
                const modelModal = document.getElementById("addModelModal");
                const modalInstance = bootstrap.Modal.getInstance(modelModal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            } else {
                console.error("Failed to add model:", await response.text());
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
});


