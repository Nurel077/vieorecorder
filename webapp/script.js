// Укажите URL вашего backend FastAPI:
const API_URL = "https://your-backend-url.app/videos";

async function loadVideos() {
    try {
        const response = await fetch(API_URL);
        const videos = await response.json();

        const list = document.getElementById("video-list");
        list.innerHTML = "";

        videos.forEach(video => {
            const btn = document.createElement("button");
            btn.className = "video-button";
            btn.innerText = video.title;

            btn.onclick = () => {
                const player = document.getElementById("player");
                player.src = video.url;
                player.play();
            };

            list.appendChild(btn);
        });

    } catch (e) {
        console.error("Ошибка загрузки видео:", e);
    }
}

loadVideos();
