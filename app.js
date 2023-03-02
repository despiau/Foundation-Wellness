const recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;

const outputDiv = document.getElementById('output');
const toggleButton = document.getElementById('toggleButton');

let isRecording = false;
let transcript = '';

toggleButton.addEventListener('click', function() {
  if (isRecording) {
    recognition.stop();
    toggleButton.classList.remove('recording');
    toggleButton.innerText = 'Let\'s talk! 🗣️';
    saveTranscript(transcript);
  } else {
    recognition.start();
    toggleButton.classList.add('recording');
    toggleButton.innerText = 'Stop talking 🤫';
    transcript = '';
  }
  isRecording = !isRecording;
  
  if (!isRecording) {
    outputDiv.style.display = 'none';
  } else {
    outputDiv.style.display = 'block';
  }
});

recognition.onresult = function(event) {
  const result = event.results[event.results.length - 1];
  const words = result[0].transcript.split(' ');
  for (const word of words) {
    transcript += word + ' ';
  }
  outputDiv.innerHTML = '';
  for (const word of words) {
    const span = document.createElement('span');
    span.innerText = word + ' ';
    outputDiv.appendChild(span);
  }
};

function saveTranscript(transcript) {
  const element = document.createElement('a');
  const file = new Blob([transcript], {type: 'text/plain'});
  element.href = URL.createObjectURL(file);
  element.download = 'transcript.txt';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}
