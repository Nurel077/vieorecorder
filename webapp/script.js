// Конфигурация API
const API_URL = window.location.origin + "/api/videos";

// Элементы DOM
const videoList = document.getElementById("video-list");
const videoPlayer = document.getElementById("player");
const videoTitle = document.getElementById("video-title");
const videoDescription = document.getElementById("video-description");
const loadingElement = document.getElementById("loading");
const errorElement = document.getElementById("error");

// Загрузка видео списка
async function loadVideos() {
    try {
        showLoading();
        hideError();
        
        const response = await fetch(API_URL);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const videos = await response.json();
        
        displayVideos(videos);
        hideLoading();
        
    } catch (error) {
        console.error("Ошибка загрузки видео:", error);
        showError(`Не удалось загрузить видео: ${error.message}`);
        hideLoading();
    }
}

// Отображение списка видео
function displayVideos(videos) {
    videoList.innerHTML = "";
    
    if (videos.length === 0) {
        videoList.innerHTML = '<div class="video-button">Видео не найдены</div>';
        return;
    }
    
    videos.forEach(video => {
        const button = document.createElement("button");
        button.className = "video-button";
        button.innerHTML = `
            <strong>${video.title}</strong>
            ${video.description ? `<br><small>${video.description}</small>` : ''}
        `;
        
        button.onclick = () => playVideo(video);
        
        videoList.appendChild(button);
    });
}

// Воспроизведение видео
function playVideo(video) {
    // Обновляем плеер
    videoPlayer.src = video.url;
    videoTitle.textContent = video.title;
    videoDescription.textContent = video.description || "Описание отсутствует";
    
    // Обновляем активную кнопку
    document.querySelectorAll('.video-button').forEach(btn => {
        btn.classList.remove('playing');
    });
    event.target.classList.add('playing');
    
    // Автовоспроизведение
    videoPlayer.play().catch(error => {
        console.log("Автовоспроизведение заблокировано:", error);
    });
}

// Утилиты для UI
function showLoading() {
    loadingElement.style.display = 'block';
}

function hideLoading() {
    loadingElement.style.display = 'none';
}

function showError(message) {
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

function hideError() {
    errorElement.style.display = 'none';
}

// Обработчики событий плеера
videoPlayer.addEventListener('error', function(e) {
    console.error("Ошибка видео:", e);
    showError("Ошибка воспроизведения видео. Проверьте ссылку или подключение к интернету.");
});

videoPlayer.addEventListener('loadstart', function() {
    videoTitle.textContent = "Загрузка...";
});

videoPlayer.addEventListener('loadeddata', function() {
    videoTitle.textContent = document.querySelector('.video-button.playing')?.querySelector('strong')?.textContent || "Видео";
});

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadVideos();
});

// Обновление списка каждые 30 секунд
setInterval(loadVideos, 30000);