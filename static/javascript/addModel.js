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

            const modelResponse = await fetch("/addModel", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(modelData),
            });

            if (modelResponse.ok) {
                const newModel = await modelResponse.json();

                // Add to model page
                const modelCard = document.createElement('div');
                modelCard.className = 'col';
                modelCard.innerHTML = `
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">${newModel.name}</h5>
                        </div>
                    </div>`;
                modelsFolder.appendChild(modelCard);

                modelForm.reset();
                const modelModal = new bootstrap.Modal.getInstance(document.getElementById('addModelModal'));
                modelModal.hide();
            } else {
                console.error("Failed to add model:", await modelResponse.text());
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
});