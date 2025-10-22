document.addEventListener("DOMContentLoaded", () => {
  const video = document.getElementById("custom-video");
  const playPause = document.getElementById("play-pause");
  const progress = document.getElementById("progress");
  const currentTime = document.getElementById("current-time");
  const duration = document.getElementById("duration");
  const mute = document.getElementById("mute");
  const volume = document.getElementById("volume");
  const fullscreen = document.getElementById("fullscreen");
  const settingsBtn = document.getElementById("settings-btn");
  const qualityMenu = document.getElementById("quality-options");
  const qualityOptions = qualityMenu.querySelectorAll("li");
  const controls = document.querySelector(".controls");

  let videoFocused = false;

  function formatTime(sec) {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }

  video.addEventListener("mouseenter", () => (videoFocused = true));
  video.addEventListener("mouseleave", () => (videoFocused = false));
  video.addEventListener("click", () => {
    videoFocused = true;
    togglePlay();
  });

  video.addEventListener("loadedmetadata", () => {
    duration.textContent = formatTime(video.duration);
  });

  video.addEventListener("timeupdate", () => {
    progress.value = (video.currentTime / video.duration) * 100;
    currentTime.textContent = formatTime(video.currentTime);
  });

  progress.addEventListener("input", () => {
    video.currentTime = (progress.value / 100) * video.duration;
  });

  function togglePlay() {
    if (video.paused) {
      video.play();
      playPause.textContent = "⏸";
    } else {
      video.pause();
      playPause.textContent = "▶";
    }
  }

  playPause.addEventListener("click", togglePlay);

  volume.addEventListener("input", () => {
    video.volume = volume.value;
    mute.textContent = video.volume === 0 ? "🔇" : "🔊";
  });

  mute.addEventListener("click", () => {
    video.muted = !video.muted;
    mute.textContent = video.muted ? "🔇" : "🔊";
  });

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      video.parentElement.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }

  fullscreen.addEventListener("click", toggleFullscreen);

  document.addEventListener("keydown", (e) => {
    if (e.key.toLowerCase() === "f" && videoFocused) {
      e.preventDefault();
      toggleFullscreen();
    }
  });

  document.addEventListener("fullscreenchange", () => {
    if (document.fullscreenElement) {
      controls.style.position = "absolute";
      controls.style.bottom = "0";
      controls.style.opacity = "1";
    } else {
      controls.style.opacity = "1";
    }
  });

  settingsBtn.addEventListener("click", () => {
    qualityMenu.style.display = qualityMenu.style.display === "block" ? "none" : "block";
  });

  qualityOptions.forEach((li) => {
    li.addEventListener("click", () => {
      const newSrc = li.getAttribute("data-src");
      if (!newSrc) return;
      const current = video.currentTime;
      const wasPlaying = !video.paused;
      video.src = newSrc;
      video.load();
      video.currentTime = current;
      if (wasPlaying) video.play();
      qualityOptions.forEach((el) => el.classList.remove("active"));
      li.classList.add("active");
      qualityMenu.style.display = "none";
    });
  });

  document.addEventListener("click", (e) => {
    if (!settingsBtn.contains(e.target) && !qualityMenu.contains(e.target)) {
      qualityMenu.style.display = "none";
    }
  });
});