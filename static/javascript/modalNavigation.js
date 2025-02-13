document.addEventListener("DOMContentLoaded", () => {
    const steps = Array.from(document.querySelectorAll(".step"));
    const nextButton = document.getElementById("next");
    const prevButton = document.getElementById("prev");
    const submitButton = document.getElementById("submitModel");

    let currentStep = 0;

    function updateStep() {
        steps.forEach((step, index) => {
            step.classList.toggle("d-none", index !== currentStep);
        });

        prevButton.classList.toggle("d-none", currentStep === 0); 
        nextButton.classList.toggle("d-none", currentStep === steps.length - 1); 
        submitButton.classList.toggle("d-none", currentStep !== steps.length - 1); 
    }

    nextButton.addEventListener("click", () => {
        if (currentStep < steps.length - 1) {
            currentStep++;
            updateStep();
        }
    });

    prevButton.addEventListener("click", () => {
        if (currentStep > 0) {
            currentStep--;
            updateStep();
        }
    });

    updateStep();
});
