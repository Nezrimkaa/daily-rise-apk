const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const os = require('os');
const fs = require('fs');

let mainWindow;
let backendProcess;

// Запуск FastAPI бэкенда
function startBackend() {
    const platform = os.platform();
    let pythonCmd = 'python';
    
    if (platform === 'win32') {
        // Пробуем найти Python в стандартных путях
        const possiblePaths = [
            'C:\\Python314\\python.exe',
            'C:\\Python313\\python.exe',
            'C:\\Python312\\python.exe',
            'C:\\Python311\\python.exe',
            'C:\\Python310\\python.exe',
            process.env.PYTHON_PATH || 'python'
        ];
        
        for (const p of possiblePaths) {
            if (fs.existsSync(p)) {
                pythonCmd = p;
                break;
            }
        }
    }
    
    console.log('Using Python:', pythonCmd);
    console.log('Working directory:', path.join(__dirname, '..'));
    
    backendProcess = spawn(pythonCmd, ['-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000', '--reload'], {
        cwd: path.join(__dirname, '..'),
        shell: true,
        windowsHide: false,
        env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });

    backendProcess.stdout.on('data', (data) => {
        console.log(`Backend: ${data}`);
    });

    backendProcess.stderr.on('data', (data) => {
        console.error(`Backend Error: ${data}`);
    });
    
    backendProcess.on('close', (code) => {
        console.log(`Backend process exited with code ${code}`);
    });
    
    backendProcess.on('error', (err) => {
        console.error('Failed to start backend:', err);
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 400,
        minHeight: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true
        },
        icon: path.join(__dirname, '../app/static/icon.svg'),
        title: 'Daily Rise',
        backgroundColor: '#f5f5f7'
    });

    // Загрузка приложения
    mainWindow.loadURL('http://127.0.0.1:8000');

    // Меню приложения
    const menu = Menu.buildFromTemplate([
        {
            label: 'Daily Rise',
            submenu: [
                { label: 'О приложении', click: () => {
                    require('electron').dialog.showMessageBox(mainWindow, {
                        type: 'info',
                        title: 'Daily Rise',
                        message: 'Daily Rise v1.0.0\nТрекер привычек',
                        detail: 'Создавай привычки. Достигай целей.'
                    });
                }},
                { type: 'separator' },
                { label: 'Выход', accelerator: 'CmdOrCtrl+Q', click: () => app.quit() }
            ]
        },
        {
            label: 'Вид',
            submenu: [
                { role: 'reload' },
                { role: 'toggleDevTools' },
                { type: 'separator' },
                { role: 'zoomIn' },
                { role: 'zoomOut' },
                { role: 'resetZoom' }
            ]
        }
    ]);

    Menu.setApplicationMenu(menu);

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.whenReady().then(() => {
    startBackend();

    // Ждём запуска бэкенда (5 секунд)
    setTimeout(() => {
        createWindow();
        // Открываем DevTools для отладки
        mainWindow.webContents.openDevTools();
    }, 5000);
});

app.on('window-all-closed', () => {
    if (backendProcess) {
        backendProcess.kill();
    }
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

app.on('will-quit', () => {
    if (backendProcess) {
        backendProcess.kill();
    }
});
