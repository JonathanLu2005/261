// static/javascript/modalNavigation.js

document.addEventListener("DOMContentLoaded", () => {
    const steps = Array.from(document.querySelectorAll(".step"));
    const prevButton = document.getElementById("prev");
    const nextButton = document.getElementById("next");
    const submitButton = document.getElementById("submitModel");
  
    let currentStep = 0;
  
    function updateStep() {
      steps.forEach((step, index) => {
        step.classList.toggle("d-none", index !== currentStep);
      });
      prevButton.classList.toggle("d-none", currentStep === 0);
      const onLastStep = currentStep === steps.length - 1;
      nextButton.classList.toggle("d-none", onLastStep);
      submitButton.classList.toggle("d-none", !onLastStep);
    }
  
    nextButton.addEventListener("click", () => {
      if (window.validateCurrentStep && window.validateCurrentStep()) {
        if (currentStep < steps.length - 1) {
          currentStep++;
          updateStep();
        }
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
