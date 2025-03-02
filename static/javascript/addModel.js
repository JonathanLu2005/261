// static/javascript/addModel.js

document.addEventListener("DOMContentLoaded", async () => {
  //load some important elements
  const modelForm = document.getElementById("addModelForm");
  const nextButton = document.getElementById("next");
  const submitButton = document.getElementById("submitModel");
  const modelsFolder = document.getElementById("modelsFolder"); 

  //render function
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


  try {
    const response = await fetch("/api/models");
    const models = await response.json();
    renderModels(models);
  } catch (error) {
    console.error("Error fetching models:", error);
  }

  // define the limits
  const limits = {
    vehicleTopSpeed: { min: 0, max: 30 },

    maxWaitTimeWeight: { min: 0, max: 1 },
    averageWaitTimeWeight: { min: 0, max: 1 },
    maxQueueLengthWeight: { min: 0, max: 1 },

    simulationTime: { min: 0, max: 99999 },
    northBoundNorth: { min: 0, max: 99999 },
    northBoundEast: { min: 0, max: 99999 },
    northBoundWest: { min: 0, max: 99999 },
    southBoundSouth: { min: 0, max: 99999 },
    southBoundEast: { min: 0, max: 99999 },
    southBoundWest: { min: 0, max: 99999 },
    westBoundWest: { min: 0, max: 99999 },
    westBoundNorth: { min: 0, max: 99999 },
    westBoundSouth: { min: 0, max: 99999 },
    eastBoundEast: { min: 0, max: 99999 },
    eastBoundNorth: { min: 0, max: 99999 },
    eastBoundSouth: { min: 0, max: 99999 },

    vehicleReactionTime: { min: 0, max: 99999 },
    vehicleStationaryDistance: { min: 0, max: 99999 }
  };

  //get the input fields at current step and use it to validate
  function getActiveStepInputFields() {
    const activeStep = document.querySelector(".step:not(.d-none)");
    if (!activeStep) return [];
    return activeStep.querySelectorAll("input[type='number']");
  }

  //validate current step
  function validateCurrentStep() {
    let allValid = true;
    const fields = getActiveStepInputFields();

    fields.forEach((input) => {
      const valueStr = input.value.trim();
      const fieldId = input.id;
      const limit = limits[fieldId] || { min: 0, max: 99999 };

      //create warning message
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

  //check the input fields all the time
  const allNumberInputs = modelForm.querySelectorAll("input[type='number']");
  allNumberInputs.forEach((input) => {
    input.addEventListener("input", () => {
      validateCurrentStep();
    });
  });

  window.validateCurrentStep = validateCurrentStep;

  //saving the model
  modelForm.addEventListener("submit", async (event) => {

    const valid = validateCurrentStep();
    if (!valid) {
      event.preventDefault();
      alert("Please correct the errors before submitting.");
      return;
    }

    event.preventDefault();
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

