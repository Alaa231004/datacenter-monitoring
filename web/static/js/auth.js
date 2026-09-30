// ============================================================
// MESSAGE
// ============================================================

function showMessage(message, success = false) {

    const element =
        document.getElementById("message");

    element.textContent = message;

    element.className =
        success
            ? "message success"
            : "message error";
}


// ============================================================
// REGISTER
// ============================================================

const registerForm =
    document.getElementById("register-form");


if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const username =
                document.getElementById(
                    "username"
                ).value.trim();

            const email =
                document.getElementById(
                    "email"
                ).value.trim();

            const password =
                document.getElementById(
                    "password"
                ).value;

            const confirmPassword =
                document.getElementById(
                    "confirm-password"
                ).value;


            if (password !== confirmPassword) {

                showMessage(
                    "Les mots de passe ne correspondent pas."
                );

                return;
            }


            try {

                const response =
                    await fetch(
                        "/api/auth/register",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                username,
                                email,
                                password
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    showMessage(
                        data.message ||
                        "Erreur lors de l'inscription."
                    );

                    return;
                }


                showMessage(
                    data.message,
                    true
                );


                setTimeout(
                    () => {

                        window.location.href =
                            data.redirect ||
                            "/verify-email";

                    },
                    800
                );

            }

            catch (error) {

                console.error(error);

                showMessage(
                    "Impossible de contacter le serveur."
                );

            }

        }
    );

}


// ============================================================
// VERIFY
// ============================================================

const verifyForm =
    document.getElementById("verify-form");


if (verifyForm) {

    verifyForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const code =
                document.getElementById(
                    "verification-code"
                ).value.trim();


            try {

                const response =
                    await fetch(
                        "/api/auth/verify",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                code
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    showMessage(
                        data.message ||
                        "Code incorrect."
                    );

                    return;
                }


                showMessage(
                    "Email vérifié avec succès.",
                    true
                );


                setTimeout(
                    () => {

                        window.location.href =
                            "/login";

                    },
                    1000
                );

            }

            catch (error) {

                console.error(error);

                showMessage(
                    "Impossible de contacter le serveur."
                );

            }

        }
    );

}


// ============================================================
// LOGIN
// ============================================================

const loginForm =
    document.getElementById("login-form");


if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();


            const identifier =
                document.getElementById(
                    "identifier"
                ).value.trim();

            const password =
                document.getElementById(
                    "password"
                ).value;


            try {

                const response =
                    await fetch(
                        "/api/auth/login",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                identifier,
                                password
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    showMessage(
                        data.message ||
                        "Erreur de connexion."
                    );


                    if (data.redirect) {

                        setTimeout(
                            () => {

                                window.location.href =
                                    data.redirect;

                            },
                            800
                        );

                    }

                    return;
                }


                showMessage(
                    "Connexion réussie.",
                    true
                );


                setTimeout(
                    () => {

                        window.location.href =
                            data.redirect || "/";

                    },
                    500
                );

            }

            catch (error) {

                console.error(error);

                showMessage(
                    "Impossible de contacter le serveur."
                );

            }

        }
    );

}
