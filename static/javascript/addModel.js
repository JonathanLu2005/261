document.addEventListener("DOMContentLoaded", () => {
    const modelForm = document.getElementById("addModelForm");
    const modelsFolder = document.getElementById("modelsFolder");

    // Form submission
    modelForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const modelFormData = new FormData(modelForm);
        const modelData = Object.fromEntries(modelFormData);

        try {
            // Send to backend
            const response = await fetch("/addModel", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(modelData),
            });

            if (response.ok) {
                const updatedModels = await response.json();

                // Clear existing models
                modelsFolder.innerHTML = "";

                // Add updated models
                updatedModels.forEach((model) => {
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

