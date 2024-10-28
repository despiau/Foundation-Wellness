const svg = document.getElementById('audio-waves');
const waves = svg.querySelectorAll('.wave');
const colors = ['#FFDD00', '#FF0000', '#00BFFF', '#00FF00'];
let colorIndex = 0;

function changeColor() {
    waves.forEach(wave => {
        wave.setAttribute('stroke', colors[colorIndex]);
    });
    colorIndex = (colorIndex + 1) % colors.length;
}

function adjustWaveAnimation(wave, scaleY) {
    wave.style.transform = `scaleY(${scaleY})`;
}

const recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;

const liveTranscriptElement = document.getElementById('live-transcript');

recognition.onresult = function(event) {
    const result = event.results[event.results.length - 1];
    const transcript = result[0].transcript.trim();
    liveTranscriptElement.innerText = transcript;

    // Adjust animation based on input length
    const scaleY = Math.min(2, 1 + transcript.length * 0.05);
    waves.forEach(wave => adjustWaveAnimation(wave, scaleY));
};

recognition.onstart = function() {
    liveTranscriptElement.style.display = 'block';
    waves.forEach(wave => wave.style.animationDuration = '0.5s'); // Accelerate animation
};

recognition.onend = function() {
    liveTranscriptElement.style.display = 'none';
    waves.forEach(wave => wave.style.animationDuration = '2s'); // Reset animation
};

recognition.start();

// Change colors every second
setInterval(changeColor, 1000);
