document.addEventListener("DOMContentLoaded", () => {
    const deleteForms = document.querySelectorAll("form[action*='/delete']");
    deleteForms.forEach((form) => {
        form.addEventListener("submit", (e) => {
            if (!confirm("Esta acción es irreversible. ¿Continuar?")) {
                e.preventDefault();
            }
        });
    });
});