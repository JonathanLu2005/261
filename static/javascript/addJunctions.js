document.addEventListener("DOMContentLoaded", async () => {
    const junctionForm = document.getElementById("addJunctionForm");
    const junctionsFolder = document.getElementById("junctionsFolder");

    // Function to render junctions
    const renderJunctions = (junctions) => {
        // Clear existing junctions
        junctionsFolder.innerHTML = "";

        // Render each junction
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
                renderJunctions(junctions);
            } else {
                console.error("Error fetching junctions:", await response.text());
            }
        } catch (error) {
            console.error("Error fetching junctions:", error);
        }
    };

    // Handle form submission
    junctionForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(junctionForm);
        const junctionData = Object.fromEntries(formData);

        // Attach the modelId to the junction data
        const urlParams = new URLSearchParams(window.location.search);
        const modelId = urlParams.get("modelId");
        junctionData.modelId = modelId;

        try {
            const response = await fetch("/addJunction", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(junctionData),
            });

            if (response.ok) {
                await fetchJunctions(); // Refresh the list of junctions
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
            console.error("Error adding junction:", error);
        }
    });

    // Initial fetch
    fetchJunctions();
});

