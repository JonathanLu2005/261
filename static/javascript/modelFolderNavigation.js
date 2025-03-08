/* JS for model page */
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("modelsFolder").addEventListener("click", (event) => {
        const modelCard = event.target.closest(".model-card");

        /* When click on model, the URL will have the model id and its name when it shows all of the junctions inside it */
        if (modelCard) {
            const modelId = modelCard.dataset.id;
            const modelName = modelCard.dataset.name;
            window.location.href = `/junctionPage?modelId=${modelId}&modelName=${encodeURIComponent(modelName)}`;
        }
    });
});
