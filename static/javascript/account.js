/* JavaScript code for login page */
document.addEventListener("DOMContentLoaded", () => {
    /* Get these html elements */
    const toggleForm = document.getElementById("toggleForm");
    const formTitle = document.getElementById("formTitle");
    const actionInput = document.getElementById("action");

    /* If we choose to sign up or login, it'll change the text to reflect the information required from the user */
    toggleForm.addEventListener("click", (event) => {
        event.preventDefault();
        if (actionInput.value === "login") {
            formTitle.innerText = "Sign Up";
            toggleForm.innerText = "Already have an account? Login";
            actionInput.value = "signup";
        } else {
            formTitle.innerText = "Login";
            toggleForm.innerText = "Don't have an account? Sign up";
            actionInput.value = "login";
        }
    });
});