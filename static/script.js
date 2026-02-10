const form = document.getElementById('download-form');
const statusContainer = document.getElementById('status-container');
const errorContainer = document.getElementById('error-container');
const btnLoader = document.getElementById('btn-loader');
const downloadBtn = document.getElementById('download-btn');
const btnText = downloadBtn.querySelector('.btn-text');
const btnIcon = downloadBtn.querySelector('ion-icon');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Reset UI
    statusContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
    setLoadingState(true);

    const formData = new FormData(form);

    try {
        const response = await fetch('/download', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            startPolling(data.video_id);
        } else {
            showError(data.error || 'An error occurred');
            setLoadingState(false);
        }

    } catch (error) {
        showError('Network error. Please try again.');
        setLoadingState(false);
    }
});

function setLoadingState(isLoading) {
    downloadBtn.disabled = isLoading;
    if (isLoading) {
        btnText.textContent = 'Processing...';
        btnIcon.style.display = 'none';
        btnLoader.style.display = 'inline-block';
    } else {
        btnText.textContent = 'Data Fetch';
        btnIcon.style.display = 'inline-block';
        btnLoader.style.display = 'none';
    }
}

function startPolling(videoId) {
    statusContainer.classList.remove('hidden');

    // Smooth scroll to status
    statusContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    const pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`/progress/${videoId}`);
            const data = await response.json();

            updateProgress(data);

            if (data.status === 'finished' || data.status === 'error') {
                clearInterval(pollInterval);
                setLoadingState(false);
                if (data.status === 'finished') {
                    document.getElementById('status-message').textContent = 'Download Complete!';
                    document.getElementById('percentage').textContent = '100%';
                    document.getElementById('progress-fill').style.width = '100%';
                    btnText.textContent = 'Data Fetch';
                }
            }

        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 1000);
}

function updateProgress(data) {
    if (data.status === 'downloading') {
        const percent = data.percentage || 0;
        document.getElementById('progress-fill').style.width = `${percent}%`;
        document.getElementById('percentage').textContent = `${percent.toFixed(1)}%`;
        document.getElementById('status-message').textContent = `Downloading: ${limitText(data.filename, 30)}`;
        document.getElementById('speed').textContent = data.speed;
        document.getElementById('eta').textContent = `ETA: ${data.eta}`;
    }
}

function limitText(text, limit) {
    if (!text) return '';
    return text.length > limit ? text.substring(0, limit) + '...' : text;
}

function showError(message) {
    errorContainer.classList.remove('hidden');
    document.getElementById('error-message').textContent = message;
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
