
document.getElementById('habit-choice').addEventListener('change', function () {
    var textInput = document.getElementById('textInput');
    if (this.value === 'other') {
        textInput.style.display = 'block';
    } else {
        textInput.style.display = 'none';
        textInput.value = '';
    }
});

document.getElementById('frequency-choice').addEventListener('change', function () {
    var frequencyInput = document.getElementById('frequencyInput');
    if (this.value === 'other') {
        frequencyInput.style.display = 'block';
    } else {
        frequencyInput.style.display = 'none';
        frequencyInput.value = '';
    }
});

document.getElementById('habit-form').addEventListener('submit', function () {
    var habitChoice = document.getElementById('habit-choice');
    var hiddenName = document.getElementById('hidden-name');
    if (habitChoice.value === 'other') {
        hiddenName.value = document.getElementById('textInput').value;
    } else {
        hiddenName.value = habitChoice.value;
    }

    var frequencyChoice = document.getElementById('frequency-choice');
    var hiddenFrequency = document.getElementById('hidden-frequency');
    if (frequencyChoice.value === 'other') {
        hiddenFrequency.value = document.getElementById('frequencyInput').value;
    } else {
        hiddenFrequency.value = frequencyChoice.value;
    }
});

