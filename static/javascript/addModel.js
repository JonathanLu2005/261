document.addEventListener("DOMContentLoaded", async () => {
  const modelForm = document.getElementById("addModelForm");
  const nextButton = document.getElementById("next");
  const submitButton = document.getElementById("submitModel");
  const modelsFolder = document.getElementById("modelsFolder");

  // Render models function
  function renderModels(models) {
    modelsFolder.innerHTML = "";
    models.forEach((model) => {
      const modelCard = document.createElement("div");
      modelCard.className = "col";
      modelCard.innerHTML = `
            <div class="card h-100 model-card" data-id="${model.id}" data-name="${model.name}" style="outline: 2px solid #2B7A78; background-color: #DEF2F1;">
                <div class="card-body">
                    <h5 class="card-title">${model.name}</h5>
                </div>
            </div>`;
      modelsFolder.appendChild(modelCard);
    });
  }

  // Initial fetch of models
  try {
    const response = await fetch("/api/models");
    const models = await response.json();
    renderModels(models);
  } catch (error) {
    console.error("Error fetching models:", error);
  }

  //define the limits
  const limits = {
    simulationTime: { min: 0 },

    northBoundNorth: { min: 0, integer: true },
    northBoundEast: { min: 0, integer: true },
    northBoundWest: { min: 0, integer: true },

    southBoundSouth: { min: 0, integer: true },
    southBoundEast: { min: 0, integer: true },
    southBoundWest: { min: 0, integer: true },

    westBoundWest: { min: 0, integer: true },
    westBoundNorth: { min: 0, integer: true },
    westBoundSouth: { min: 0, integer: true },

    eastBoundEast: { min: 0, integer: true },
    eastBoundNorth: { min: 0, integer: true },
    eastBoundSouth: { min: 0, integer: true },

    vehicleTopSpeed: { min: 1, max: 30, integer: true },
    vehicleReactionTime: { min: 0 },
    vehicleStationaryDistance: { min: 0.5 },

    vehicleLength: { min: 1.5 },
    // For vehicleLengthFluctuation, we only check it's >= 0.
    // Dynamic check: value must be <= (vehicleLength - 1.5) will be done separately.
    vehicleLengthFluctuation: { min: 0 },

    vehicleTopSpeedSpecial: { min: 1, integer: true },
    vehicleLengthSpecial: { min: 1 },
    // For vehicleLengthFluctuationSpecial, dynamic check: <= (vehicleLengthSpecial - 1)
    vehicleLengthFluctuationSpecial: { min: 0 },

    northBoundNorthSpecial: { min: 0, integer: true },
    northBoundEastSpecial: { min: 0, integer: true },
    northBoundWestSpecial: { min: 0, integer: true },

    southBoundSouthSpecial: { min: 0, integer: true },
    southBoundEastSpecial: { min: 0, integer: true },
    southBoundWestSpecial: { min: 0, integer: true },

    westBoundWestSpecial: { min: 0, integer: true },
    westBoundNorthSpecial: { min: 0, integer: true },
    westBoundSouthSpecial: { min: 0, integer: true },

    eastBoundEastSpecial: { min: 0, integer: true },
    eastBoundNorthSpecial: { min: 0, integer: true },
    eastBoundSouthSpecial: { min: 0, integer: true },

    // Weighting factors: must be in [0, 1]
    maxWaitTimeWeight: { min: 0, max: 1 },
    averageWaitTimeWeight: { min: 0, max: 1 },
    maxQueueLengthWeight: { min: 0, max: 1 }
  };

  // Helper: get currently visible step's number inputs
  function getActiveStepInputFields() {
    const activeStep = document.querySelector(".step:not(.d-none)");
    if (!activeStep) return [];
    return activeStep.querySelectorAll("input[type='number']");
  }

  // Validate current step fields in real time
  function validateCurrentStep() {
    let allValid = true;
    const fields = getActiveStepInputFields();

    fields.forEach((input) => {
      const valueStr = input.value.trim();
      const fieldId = input.id;
      const limit = limits[fieldId] || { min: 0,};

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
      if (isNaN(value) || value < limit.min || (limit.max !== undefined && value > limit.max)) {
        if (limit.max !== undefined) {
          warningMessage.innerText = `Value must be between ${limit.min} and ${limit.max}`;
        } else {
          warningMessage.innerText = `Value must be greater than ${limit.min}`;
        }
        warningMessage.style.display = "block";
        input.style.border = "2px solid red";
        allValid = false;
      } else {
        // For vehicleLengthFluctuation: value must be <= (vehicleLength - 1.5)
        if (fieldId === "vehicleLengthFluctuation") {
          const vehicleLengthInput = document.getElementById("vehicleLength");
          const vehicleLengthVal = parseFloat(vehicleLengthInput.value.trim());
          if (!isNaN(vehicleLengthVal) && value > (vehicleLengthVal - 1.5)) {
            warningMessage.innerText = `Value must be no more than vehicleLength - 1.5 (${vehicleLengthVal - 1.5})`;
            warningMessage.style.display = "block";
            input.style.border = "2px solid red";
            allValid = false;
          } else {
            warningMessage.style.display = "none";
            input.style.border = "";
          }
        }
        // For vehicleLengthFluctuationSpecial: value must be <= (vehicleLengthSpecial - 1)
        if (fieldId === "vehicleLengthFluctuationSpecial") {
          const vehicleLengthSpecialInput = document.getElementById("vehicleLengthSpecial");
          const vehicleLengthSpecialVal = parseFloat(vehicleLengthSpecialInput.value.trim());
          if (!isNaN(vehicleLengthSpecialVal) && value > (vehicleLengthSpecialVal - 1)) {
            warningMessage.innerText = `Value must be no more than vehicleLengthSpecial - 1 (${vehicleLengthSpecialVal - 1})`;
            warningMessage.style.display = "block";
            input.style.border = "2px solid red";
            allValid = false;
          } else {
            warningMessage.style.display = "none";
            input.style.border = "";
          }
        }
        //check if it's integer
        if (limit.integer && !Number.isInteger(value)) {
          warningMessage.innerText = "Value must be an integer.";
          warningMessage.style.display = "block";
          input.style.border = "2px solid red";
          allValid = false;
        }
        if (allValid) {
          warningMessage.style.display = "none";
          input.style.border = "";
        }
      }
    });

    //update next button
    nextButton.disabled = !allValid;
    nextButton.style.backgroundColor = allValid ? "" : "#d3d3d3";
    nextButton.style.cursor = allValid ? "pointer" : "not-allowed";

    return allValid;
  }

  //update next button
  const allNumberInputs = modelForm.querySelectorAll("input[type='number']");
  allNumberInputs.forEach((input) => {
    input.addEventListener("input", () => {
      validateCurrentStep();
    });
  });

  // Expose validation function for navigation modules if needed
  window.validateCurrentStep = validateCurrentStep;

  // Handle form submission
  modelForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const valid = validateCurrentStep();
    if (!valid) {
      alert("Please correct the errors before submitting.");
      return;
    }
    const modelFormData = new FormData(modelForm);
    const modelData = Object.fromEntries(modelFormData);

    try {
      const response = await fetch("/addModel", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(modelData),
      });
      if (response.ok) {
        const updatedModels = await response.json();
        renderModels(updatedModels);
        modelForm.reset();
        const modelModal = document.getElementById("addModelModal");
        const modalInstance = bootstrap.Modal.getInstance(modelModal);
        if (modalInstance) {
          modalInstance.hide();
        }
      } else {
        console.error("Failed to add model:", await response.text());
      }
    } catch (error) {
      console.error("Error submitting model:", error);
    }
  });
});


