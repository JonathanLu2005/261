document.addEventListener("DOMContentLoaded", () => {
    const steps = Array.from(document.querySelectorAll(".step"));
    const prevButton = document.getElementById("prev");
    const nextButton = document.getElementById("next");
    const submitButton = document.getElementById("submitJunction");
    const form = document.getElementById("addJunctionForm");

    let currentStep = 0;

    // Function to update visible steps
    function updateStep() {
        steps.forEach((step, index) => {
            step.classList.toggle("d-none", index !== currentStep);
        });
        prevButton.classList.toggle("d-none", currentStep === 0);
        const onLastStep = currentStep === steps.length - 1;
        nextButton.classList.toggle("d-none", onLastStep);
        submitButton.classList.toggle("d-none", !onLastStep);
    }

    // Move to the next step
    nextButton.addEventListener("click", () => {
        if (currentStep < steps.length - 1) {
            currentStep++;
            updateStep();
        }
    });

    // Move to the previous step
    prevButton.addEventListener("click", () => {
        if (currentStep > 0) {
            currentStep--;
            updateStep();
        }
    });

    // Handle form submission
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        alert("Form submitted!");
        // Additional logic for handling form data
    });

    // Initialize the step visibility
    updateStep();
});

