const { spawn } = require('child_process');
const path = require('path');

// Function to start a Python script with pipenv
function startPythonScript(scriptName) {
    const scriptPath = path.join(__dirname, scriptName);
    console.log(`Starting ${scriptName}...`);
    
    // Use the full path to pipenv
    const pipenvPath = process.platform === 'win32' ? 'pipenv.cmd' : 'pipenv';
    
    const pythonProcess = spawn(pipenvPath, ['run', 'python', scriptPath], {
        stdio: 'inherit',
        shell: true,
        cwd: __dirname  // Set the working directory to the script's location
    });

    pythonProcess.on('error', (err) => {
        console.error(`Failed to start ${scriptName}:`, err);
    });

    return pythonProcess;
}

// Start all servers
console.log('Starting all servers...');

// Start voice_of_the_patient.py
const voiceServer = startPythonScript('voice_of_the_patient.py');

// Start brain_of_the_doctor.py
const brainServer = startPythonScript('brain_of_the_doctor.py');

// Handle process termination
process.on('SIGINT', () => {
    console.log('\nShutting down servers...');
    voiceServer.kill();
    brainServer.kill();
    process.exit();
});

console.log('All servers started. Press Ctrl+C to stop all servers.'); 