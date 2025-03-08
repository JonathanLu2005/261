/* For junction page */
document.addEventListener("DOMContentLoaded", () => {
    /* Get junction model id */
    const urlParams = new URLSearchParams(window.location.search);
    const modelId = urlParams.get("modelId"); 

    /* Handles junction form */
    const junctionForm = document.getElementById("addJunctionForm");
    junctionForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        /* Get junction form data */
        const formData = new FormData(junctionForm);
        const junctionData = Object.fromEntries(formData);

        /* Get junction model id */
        junctionData.modelId = modelId;

        try {
            /* Try to add junction in backend */
            const response = await fetch("/addJunction", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(junctionData),
            });

            if (response.ok) {
                console.log("Junction added successfully!");

                /* Close modal after adding */
                junctionForm.reset();
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


