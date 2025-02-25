document.addEventListener("DOMContentLoaded", () => {
    // Retrieve modelId from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const modelId = urlParams.get("modelId"); // Get modelId from the query string
    console.log("Model ID:", modelId); // Check the modelId

    // Handle form submission
    const junctionForm = document.getElementById("addJunctionForm");
    junctionForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(junctionForm);
        const junctionData = Object.fromEntries(formData);

        // Attach modelId to the junction data
        junctionData.modelId = modelId;

        console.log("Junction Data:", junctionData); // Debug print to check junction data before sending

        try {
            const response = await fetch("/addJunction", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(junctionData),
            });

            if (response.ok) {
                console.log("Junction added successfully!");

                // Reset the form
                junctionForm.reset();

                // Close the modal
                const junctionModal = document.getElementById("addJunctionModal");
                const modalInstance = bootstrap.Modal.getInstance(junctionModal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            } else {
                console.error("Error adding junction:", await response.text());
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
});


