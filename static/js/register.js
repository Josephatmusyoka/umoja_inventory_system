document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registrationForm");
    
    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent the default form submission

        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        // Validate passwords
        if (password !== confirmPassword) {
            alert("Passwords do not match. Please try again.");
            return;
        }

        // Gather form data
        const formData = new FormData(form);
        
        // Send data to server (example URL, adjust as needed)
        fetch("/register", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                alert("Registration successful!"); // Success message
                form.reset(); // Reset form after submission
            } else {
                alert("Registration failed. Please try again."); // Error message
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again."); // Handle fetch error
        });
    });
});
