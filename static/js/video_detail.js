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
  const settingsMenu = document.getElementById("settings-menu");
  const qualityBtn = document.getElementById("quality-btn");
  const speedBtn = document.getElementById("speed-btn");
  const qualityOptions = document.getElementById("quality-options");
  const speedOptions = document.getElementById("speed-options");
  const controls = document.querySelector(".controls");

  let videoFocused = false;

  function formatTime(sec) {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  }

  video.addEventListener("mouseenter", () => (videoFocused = true));
  video.addEventListener("mouseleave", () => (videoFocused = false));
  video.addEventListener("click", togglePlay);
  video.addEventListener("loadedmetadata", () => { duration.textContent = formatTime(video.duration); });
  video.addEventListener("timeupdate", () => { progress.value = (video.currentTime / video.duration) * 100; currentTime.textContent = formatTime(video.currentTime); });
  progress.addEventListener("input", () => { video.currentTime = (progress.value / 100) * video.duration; });

  function togglePlay() {
    if (video.paused) { video.play(); playPause.textContent = "⏸"; }
    else { video.pause(); playPause.textContent = "▶"; }
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

  fullscreen.addEventListener("click", () => {
    if (!document.fullscreenElement) video.parentElement.requestFullscreen();
    else document.exitFullscreen();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key.toLowerCase() === "f" && videoFocused) { e.preventDefault(); if (!document.fullscreenElement) video.parentElement.requestFullscreen(); else document.exitFullscreen(); }
  });

  settingsBtn.addEventListener("click", (e) => {
    settingsMenu.style.display = settingsMenu.style.display === "block" ? "none" : "block";
    qualityOptions.style.display = "none";
    speedOptions.style.display = "none";
  });

  qualityBtn.addEventListener("click", () => {
    qualityOptions.style.display = qualityOptions.style.display === "block" ? "none" : "block";
    speedOptions.style.display = "none";
  });

  speedBtn.addEventListener("click", () => {
    speedOptions.style.display = speedOptions.style.display === "block" ? "none" : "block";
    qualityOptions.style.display = "none";
  });

  qualityOptions.querySelectorAll("li").forEach(li => {
    li.addEventListener("click", () => {
      const newSrc = li.getAttribute("data-src");
      if (!newSrc) return;
      const current = video.currentTime;
      const wasPlaying = !video.paused;
      video.src = newSrc;
      video.load();
      video.currentTime = current;
      if (wasPlaying) video.play();
      qualityOptions.querySelectorAll("li").forEach(el => el.classList.remove("active"));
      li.classList.add("active");
      qualityOptions.style.display = "none";
      settingsMenu.style.display = "none";
    });
  });

  speedOptions.querySelectorAll("li").forEach(li => {
    li.addEventListener("click", () => {
      const rate = parseFloat(li.getAttribute("data-speed"));
      video.playbackRate = rate;
      speedOptions.querySelectorAll("li").forEach(el => el.classList.remove("active"));
      li.classList.add("active");
      speedOptions.style.display = "none";
      settingsMenu.style.display = "none";
    });
  });

  document.addEventListener("click", e => {
    if (!settingsBtn.contains(e.target) && !settingsMenu.contains(e.target) &&
        !qualityOptions.contains(e.target) && !speedOptions.contains(e.target)) {
      settingsMenu.style.display = "none";
      qualityOptions.style.display = "none";
      speedOptions.style.display = "none";
    }
  });
});
