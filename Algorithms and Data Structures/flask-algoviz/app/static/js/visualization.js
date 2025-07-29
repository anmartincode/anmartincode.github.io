document.addEventListener('DOMContentLoaded', function() {
    const stepBtn = document.getElementById('step-btn');
    const opLog = document.getElementById('op-log');
    const svg = document.getElementById('viz-canvas');

    if (stepBtn) {
        stepBtn.addEventListener('click', function() {
            fetch('/api/step', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({})})
                .then(res => res.json())
                .then(data => {
                    // Example: add operation to log
                    if (data.step) {
                        const li = document.createElement('li');
                        li.textContent = JSON.stringify(data.step);
                        opLog.appendChild(li);
                        // TODO: update SVG
                    }
                });
        });
    }
});
