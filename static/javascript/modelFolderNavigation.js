document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("modelsFolder").addEventListener("click", (event) => {
        const modelCard = event.target.closest(".model-card");
        if (modelCard) {
            const modelId = modelCard.dataset.id;
            const modelName = modelCard.dataset.name;

            // Navigate to junctionPage with model ID and name
            window.location.href = `/junctionPage?modelId=${modelId}&modelName=${encodeURIComponent(modelName)}`;
        }
    });
});
