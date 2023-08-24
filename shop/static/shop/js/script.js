document.addEventListener("DOMContentLoaded", function () {
    const removeButtons = document.querySelectorAll(".remove-button");

    removeButtons.forEach((button) => {
        button.addEventListener("click", function (event) {
            const confirmation = confirm("Are you sure you want to remove this item from your cart?");
            if (!confirmation) {
                event.preventDefault();
            }
        });
    });

    const passwordToggle = document.querySelector(".password-toggle");
    const passwordInput = document.getElementById("id_password");

    if (passwordToggle && passwordInput) {
        passwordToggle.addEventListener("click", function () {
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
            } else {
                passwordInput.type = "password";
            }
        });
    }

    const editProfileBtn = document.querySelector(".btn-primary");
    if (editProfileBtn) {
        editProfileBtn.addEventListener("click", function () {
            // Здесь вы можете добавить логику для обработки нажатия на кнопку "Edit Profile"
            console.log("Edit Profile button clicked");
        });
    }

    const deleteProfileButton = document.getElementById("deleteProfileButton");
    if (deleteProfileButton) {
        deleteProfileButton.addEventListener("click", function () {
            const confirmation = confirm("Are you sure you want to delete your profile?");
            if (confirmation) {
                window.location.href = "/accounts/profile/delete/";
            }
        });
    }
});
