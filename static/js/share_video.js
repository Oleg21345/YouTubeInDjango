document.querySelectorAll('.share-btn').forEach(btn => {
    btn.addEventListener('click', e => {
        e.preventDefault();
        const videoUrl = btn.dataset.url;
        document.getElementById('shareLink').innerHTML =
            `<a href="${videoUrl}" target="_blank">${videoUrl}</a>`;
        document.getElementById('copyBtn').dataset.url = videoUrl;

        const modal = new bootstrap.Modal(document.getElementById('shareModal'));
        modal.show();
    });
});

document.getElementById('copyBtn').addEventListener('click', async (e) => {
    const link = e.target.dataset.url;
    try {
        await navigator.clipboard.writeText(link);
        const btn = document.getElementById('copyBtn');
        btn.innerHTML = "✅ Copied!";
        setTimeout(() => btn.innerHTML = '<i class="bi bi-clipboard"></i> Copy link', 2000);
    } catch (err) {
        alert("❌ Failed to copy the link.");
    }
});