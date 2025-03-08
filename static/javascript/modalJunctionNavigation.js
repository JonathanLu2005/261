/* For junction page modal navigation */
document.addEventListener("DOMContentLoaded", () => {
    /* Junction modal, gets the buttons from the modal */
    const steps = Array.from(document.querySelectorAll(".step"));
    const prevButton = document.getElementById("prev");
    const nextButton = document.getElementById("next");
    const submitButton = document.getElementById("submitJunction");
    const form = document.getElementById("addJunctionForm");

    let currentStep = 0;

    /* Change step when moving back and forth on modal */
    function updateStep() {
        steps.forEach((step, index) => {
            step.classList.toggle("d-none", index !== currentStep);
        });
        prevButton.classList.toggle("d-none", currentStep === 0);
        const onLastStep = currentStep === steps.length - 1;
        nextButton.classList.toggle("d-none", onLastStep);
        submitButton.classList.toggle("d-none", !onLastStep);
    }

    /* Move to next part of modal */
    nextButton.addEventListener("click", () => {
        if (currentStep < steps.length - 1) {
            currentStep++;
            updateStep();
        }
    });

    /* Move previous part of modal */
    prevButton.addEventListener("click", () => {
        if (currentStep > 0) {
            currentStep--;
            updateStep();
        }
    });

    /* Handle form submission */
    form.addEventListener("submit", (event) => {
        event.preventDefault();
    });

    updateStep();
});

