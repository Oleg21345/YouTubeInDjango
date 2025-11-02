document.addEventListener("DOMContentLoaded", function () {
    const playlistLinks = document.querySelectorAll(".open-playlist-modal");
    const playlistModalEl = document.getElementById("playlistModal");
    const playlistModal = new bootstrap.Modal(playlistModalEl);
    const modalBody = document.getElementById("playlistModalBody");

    playlistLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            const url = this.dataset.url;

            modalBody.innerHTML = '<div class="text-center py-3"><div class="spinner-border text-primary" role="status"></div></div>';
            playlistModal.show();

            fetch(url)
                .then(response => response.text())
                .then(html => {
                modalBody.innerHTML = html;

                const form = modalBody.querySelector("form");
                if (form) {
                    form.addEventListener("submit", function (e) {
                        e.preventDefault();
                        const formData = new FormData(form);

                        fetch(url, {
                            method: "POST",
                            body: formData,
                            headers: { "X-Requested-With": "XMLHttpRequest" }
                        })
                            .then(resp => resp.json())
                            .then(data => {
                            if (data.success) {
                                playlistModal.hide();
                            } else {
                                modalBody.innerHTML = data.form_html;
                            }
                            if (data.success) {
                                playlistModal.hide();

                                const toast = document.createElement("div");
                                toast.className = "alert alert-success position-fixed bottom-0 end-0 m-3";
                                toast.style.zIndex = 1055; // щоб був поверх модалки
                                toast.textContent = data.message;
                                document.body.appendChild(toast);
                                setTimeout(() => toast.remove(), 2500);
                            }

                        });
                    });
                }
            });
        });
    });
});
