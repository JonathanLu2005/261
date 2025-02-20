// static/javascript/addModel.js

document.addEventListener("DOMContentLoaded", () => {
  const modelForm = document.getElementById("addModelForm");
  const nextButton = document.getElementById("next");
  const submitButton = document.getElementById("submitModel");

  // define the limits
  const limits = {
    simulationTime: { min: 1, max: 999999 },

    northBoundNorth: { min: 0, max: 999999 },
    northBoundEast: { min: 0, max: 999999 },
    northBoundWest: { min: 0, max: 999999 },

    southBoundSouth: { min: 0, max: 999999 },
    southBoundEast: { min: 0, max: 999999 },
    southBoundWest: { min: 0, max: 999999 },

    westBoundWest: { min: 0, max: 999999 },
    westBoundNorth: { min: 0, max: 999999 },
    westBoundSouth: { min: 0, max: 999999 },

    eastBoundEast: { min: 0, max: 999999 },
    eastBoundNorth: { min: 0, max: 999999 },
    eastBoundSouth: { min: 0, max: 999999 },

    vehicleTopSpeed: { min: 0, max: 30 },
    vehicleReactionTime: { min: 0, max: 999999 },
    vehicleStationaryDistance: { min: 0, max: 999999 },

    maxWaitTimeWeight: { min: 0, max: 1 },
    averageWaitTimeWeight: { min: 0, max: 1 },
    maxQueueLengthWeight: { min: 0, max: 1 }
  };

  // return the input field at current step
  function getActiveStepInputFields() {
    const activeStep = document.querySelector(".step:not(.d-none)");
    if (!activeStep) return [];
    return activeStep.querySelectorAll("input[type='number']");
  }

  // verify the input at current step
  function validateCurrentStep() {
    let allValid = true;
    const fields = getActiveStepInputFields();

    fields.forEach((input) => {
      const valueStr = input.value.trim();
      const fieldId = input.id;
      const limit = limits[fieldId] || { min: 0, max: 99999 };

      let warningMessage = input.nextElementSibling;
      if (!warningMessage || !warningMessage.classList.contains("warning-message")) {
        warningMessage = document.createElement("p");
        warningMessage.className = "warning-message";
        warningMessage.style.color = "red";
        input.parentNode.insertBefore(warningMessage, input.nextSibling);
      }

      if (valueStr === "") {
        warningMessage.innerText = "Value is required.";
        warningMessage.style.display = "block";
        input.style.border = "2px solid red";
        allValid = false;
        return;
      }

      const value = parseFloat(valueStr);
      if (isNaN(value) || value < limit.min || value > limit.max) {
        warningMessage.innerText = `Value must be between ${limit.min} and ${limit.max}`;
        warningMessage.style.display = "block";
        input.style.border = "2px solid red";
        allValid = false;
      } else {
        warningMessage.style.display = "none";
        input.style.border = "";
      }
    });

    nextButton.disabled = !allValid;
    nextButton.style.backgroundColor = allValid ? "" : "#d3d3d3";
    nextButton.style.cursor = allValid ? "pointer" : "not-allowed";

    return allValid;
  }

  const allNumberInputs = modelForm.querySelectorAll("input[type='number']");
  allNumberInputs.forEach((input) => {
    input.addEventListener("input", () => {
      // only validate the current step
      validateCurrentStep();
    });
  });

  window.validateCurrentStep = validateCurrentStep;

  // validate again before submit
  modelForm.addEventListener("submit", (event) => {
    const valid = validateCurrentStep();
    if (!valid) {
      event.preventDefault();
      alert("Please correct the errors before submitting.");
    }
  });
});


