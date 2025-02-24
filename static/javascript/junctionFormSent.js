document.addEventListener("DOMContentLoaded", () => {
    const modelId = "{{ model_id }}"; // Pass the modelId from Flask to the template

    // Handle form submission
    const junctionForm = document.getElementById("addJunctionForm");
    junctionForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(junctionForm);
        const junctionData = Object.fromEntries(formData);
        
        // Attach modelId to the junction data
        junctionData.modelId = modelId;

        try {
            const response = await fetch("/addJunction", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(junctionData),
            });
        } catch (error) {
            console.error("Error:", error);
        }
    });
});