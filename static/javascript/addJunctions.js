/* For the junction page */
document.addEventListener("DOMContentLoaded", async () => {
    /* Gets the junction form */
    const junctionForm = document.getElementById("addJunctionForm");

    document.addEventListener("DOMContentLoaded", async () => {
      /* Get junctions folder */
      const junctionsFolder = document.getElementById("junctionsFolder");

      /* Function to show junctions in junctions folder */
      const renderJunctions = (junctions) => {
        junctionsFolder.innerHTML = "";

        /* Create cards for each junction to show to frontend */
        junctions.forEach((junction) => {
          const junctionCard = document.createElement("div");
          junctionCard.className = "col";
          junctionCard.innerHTML = `
            <div class="card h-100" style="outline: 2px solid #2B7A78;">
              <div class="card-body">
                <h5 class="card-title">${junction.junctionname}</h5>
              </div>
            </div>`;
  
          /* Append card to the junction folder */
          junctionsFolder.appendChild(junctionCard);
        });
      };
  
      /* Fetch junction data from API */
      const fetchJunctions = async () => {
        /* Use URL to get model id */
        const urlParams = new URLSearchParams(window.location.search);
        const modelId = urlParams.get("modelId");
        if (!modelId) {
          console.error("Missing modelId in URL");
          return;
        }

        /* Call function in backend to get all junctions and show to frontend */
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
      
      /* Call function */
      fetchJunctions();
    });

    fetchJunctions();

    // define the limits
    const limits = {
      junctionLanes: { min: 1, integer: true },
      junctionSideLength: { min: 0 }, 
  
      pedestrianCrossingDuration: { min: 0, integer: true },
      pedestrianCrossingRequests: { min: 0, integer: true },
  
      northboundOrder: { min: 1, integer: true },
      southboundOrder: { min: 1, integer: true },
      eastboundOrder: { min: 1, integer: true },
      westboundOrder: { min: 1, integer: true },
  
      northboundDuration: { min: 1, integer: true },
      southboundDuration: { min: 1, integer: true },
      eastboundDuration: { min: 1, integer: true },
      westboundDuration: { min: 1, integer: true },
  
      specialLaneRatio: { min: 0, max: 1 } 
    };
  
    // Helper: get currently visible step's number inputs
    function getActiveStepInputFields() {
      const activeStep = document.querySelector("#addJunctionForm .step:not(.d-none)");
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
          const limit = limits[fieldId] || { min: 0, max: Infinity };
      
          // if it's pedestrianCrossing step, skip first
          if (fieldId === "pedestrianCrossingDuration" || fieldId === "pedestrianCrossingRequests") {
            return;
          }
      
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
          if (
            isNaN(value) ||
            value < limit.min ||
            (limit.max !== undefined && value > limit.max)
          ) {
            if (limit.max !== undefined && limit.max !== Infinity) {
              warningMessage.innerText = `Value must be between ${limit.min} and ${limit.max}`;
            } else {
              warningMessage.innerText = `Value must be greater than ${limit.min}`;
            }
            warningMessage.style.display = "block";
            input.style.border = "2px solid red";
            allValid = false;
          } else {
            if (limit.integer && !Number.isInteger(value)) {
              warningMessage.innerText = "Value must be an integer.";
              warningMessage.style.display = "block";
              input.style.border = "2px solid red";
              allValid = false;
            } else {
              warningMessage.style.display = "none";
              input.style.border = "";
            }
          }
        });
      
        // validate the pedestrian crossing part
        const crossingYes = document.getElementById("pedestrianCrossingYes");
        const crossingNo = document.getElementById("pedestrianCrossingNo");
        const durationInput = document.getElementById("pedestrianCrossingDuration");
        const requestsInput = document.getElementById("pedestrianCrossingRequests");
      
        if (
          crossingYes && crossingNo && durationInput && requestsInput &&
          durationInput.closest(".step:not(.d-none)") && requestsInput.closest(".step:not(.d-none)")
        ) {
          let warningMessage = durationInput.nextElementSibling;
          if (!warningMessage || !warningMessage.classList.contains("warning-message")) {
            warningMessage = document.createElement("p");
            warningMessage.className = "warning-message";
            warningMessage.style.color = "red";
            durationInput.parentNode.insertBefore(warningMessage, durationInput.nextSibling);
          }
      
          const durationValStr = durationInput.value.trim();
          const requestsValStr = requestsInput.value.trim();
      
          if (crossingNo.checked) {
            // if choose 'No', input must be 0
            const durationVal = parseFloat(durationValStr);
            const requestsVal = parseFloat(requestsValStr);
            if (durationValStr === "" || durationVal !== 0) {
              warningMessage.innerText = 'When pedestrian crossing is No, duration must be 0.';
              warningMessage.style.display = "block";
              durationInput.style.border = "2px solid red";
              allValid = false;
            } else {
              warningMessage.style.display = "none";
              durationInput.style.border = "";
            }
            if (requestsValStr === "" || requestsVal !== 0) {
              warningMessage.innerText = 'When pedestrian crossing is No, requests must be 0.';
              warningMessage.style.display = "block";
              requestsInput.style.border = "2px solid red";
              allValid = false;
            } else {
              warningMessage.style.display = "none";
              requestsInput.style.border = "";
            }
          } else if (crossingYes.checked) {
            // if 'Yes', input must suit the limit
            if (durationValStr === "") {
              warningMessage.innerText = "Value is required.";
              warningMessage.style.display = "block";
              durationInput.style.border = "2px solid red";
              allValid = false;
            } else {
              const durationVal = parseFloat(durationValStr);
              if (isNaN(durationVal) || durationVal <= 0) {
                warningMessage.innerText = "Must be a positive number.";
                warningMessage.style.display = "block";
                durationInput.style.border = "2px solid red";
                allValid = false;
              } else {
                warningMessage.style.display = "none";
                durationInput.style.border = "";
              }
            }
            if (requestsValStr === "") {
              warningMessage.innerText = "Value is required.";
              warningMessage.style.display = "block";
              requestsInput.style.border = "2px solid red";
              allValid = false;
            } else {
              const requestsVal = parseFloat(requestsValStr);
              if (isNaN(requestsVal) || requestsVal <= 0) {
                warningMessage.innerText = "Must be a positive number.";
                warningMessage.style.display = "block";
                requestsInput.style.border = "2px solid red";
                allValid = false;
              } else {
                warningMessage.style.display = "none";
                requestsInput.style.border = "";
              }
            }
            const durationVal = parseFloat(durationValStr);
            const requestsVal = parseFloat(requestsValStr);
            if (!isNaN(durationVal) && !isNaN(requestsVal) && requestsVal > 0) {
              const limitCheck = 60 / requestsVal;
              if (durationVal >= limitCheck) {
                warningMessage.innerText = `Duration must be < (60 / crossingRequests) ≈ ${limitCheck.toFixed(2)}`;
                warningMessage.style.display = "block";
                durationInput.style.border = "2px solid red";
                allValid = false;
              }
            }
          }
        }
      
        //update next button
        const nextButton = document.getElementById("next");
        if (nextButton) {
          nextButton.disabled = !allValid;
          nextButton.style.backgroundColor = allValid ? "" : "#d3d3d3";
          nextButton.style.cursor = allValid ? "pointer" : "not-allowed";
        }
      
        return allValid;
      }
  
    const allNumberInputs = junctionForm.querySelectorAll("input[type='number']");
    allNumberInputs.forEach((input) => {
      input.addEventListener("input", validateCurrentStep);
    });
  
    // 将验证函数暴露到全局，方便多步导航脚本调用
    window.validateCurrentStep = validateCurrentStep;
    
    // ---------------------------
    // 6. 处理表单提交（Save 按钮）
    // ---------------------------

    /* Handle junctions form */
    junctionForm.addEventListener("submit", async (event) => {
      /* Get data from junction form */
      event.preventDefault();
      const formData = new FormData(junctionForm);
      const junctionData = Object.fromEntries(formData);

      /* Get model id from url */
      const urlParams = new URLSearchParams(window.location.search);
      const modelId = urlParams.get("modelId");
      if (!modelId) {
        console.error("Missing modelId in URL");
        alert("Missing modelId in URL");
        return;
      }
      junctionData.modelId = modelId;

      try {
        /* Add the junction in backend */
        const response = await fetch("/addJunction", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(junctionData),
        });

        if (response.ok) {
          /* After adding new junction, fetch the new junction, and hide the modal after adding junction */
          await fetchJunctions(); 
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
});

