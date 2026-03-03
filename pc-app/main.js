const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

// Глобальная обработка необработанных ошибок
process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

let mainWindow;
let backendProcess;
let isBackendRunning = false;

// Определение корневой директории - используем абсолютный путь
const appRoot = path.resolve(__dirname, '..', '..');

// Поиск Python
function findPython() {
    const paths = [
        path.join(appRoot, 'backend', 'venv', 'Scripts', 'python.exe'),
        path.join(process.cwd(), 'venv', 'Scripts', 'python.exe'),
        'python',
        'python3'
    ];

    for (let p of paths) {
        try {
            const resolved = path.resolve(p);
            if (fs.existsSync(resolved)) {
                console.log('Found Python at:', resolved);
                return resolved;
            }
        } catch {}
    }
    console.log('Python not found, using default');
    return 'python';
}

// Запуск бэкенда
function startBackend() {
    if (isBackendRunning) return;
    
    const python = findPython();
    const backendDir = path.join(appRoot, 'backend');
    const uvicornScript = path.join(backendDir, 'venv', 'Scripts', 'uvicorn.exe');

    console.log('Starting backend with:', python);
    console.log('Backend dir:', backendDir);
    console.log('Python exists:', fs.existsSync(python));
    console.log('Backend dir exists:', fs.existsSync(backendDir));
    console.log('app.main.py exists:', fs.existsSync(path.join(backendDir, 'app', 'main.py')));
    console.log('uvicorn.exe exists:', fs.existsSync(uvicornScript));

    // Проверяем всё перед запуском
    if (!fs.existsSync(python)) {
        console.error('Python executable not found!');
        return;
    }
    if (!fs.existsSync(backendDir)) {
        console.error('Backend directory not found!');
        return;
    }

    // Запускаем через uvicorn.exe напрямую
    try {
        backendProcess = spawn(uvicornScript, ['app.main:app', '--host', '127.0.0.1', '--port', '8000'], {
            cwd: backendDir,
            stdio: ['ignore', 'pipe', 'pipe'],
            detached: false,
            env: process.env
        });

        backendProcess.on('error', (err) => {
            console.error('Failed to start backend:', err.message);
            console.error('Error code:', err.code);
            console.error('Error syscall:', err.syscall);
        });

        backendProcess.on('exit', (code) => {
            console.log('Backend exited with code:', code);
            isBackendRunning = false;
        });

        isBackendRunning = true;
        console.log('Backend process started with PID:', backendProcess.pid);
    } catch (err) {
        console.error('Exception starting backend:', err.message);
        return;
    }

    if (backendProcess) {
        backendProcess.stdout.on('data', (data) => {
            console.log(`Backend: ${data}`);
        });

        backendProcess.stderr.on('data', (data) => {
            console.error(`Backend Error: ${data}`);
        });
    }
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1280,
        height: 800,
        minWidth: 400,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        },
        backgroundColor: '#f5f5f7'
    });

    // Ждём 2 секунды для запуска бэкенда, затем пробуем загрузить
    setTimeout(() => {
        mainWindow.loadURL('http://127.0.0.1:8000').catch(err => {
            console.error('Failed to load URL:', err);
            // Фолбэк на локальный файл не сработает для SPA с API calls
        });
    }, 2000);

    // Меню
    const menu = Menu.buildFromTemplate([
        {
            label: 'Daily Rise',
            submenu: [
                { 
                    label: 'О программе', 
                    click: () => {
                        const { dialog } = require('electron');
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            title: 'Daily Rise',
                            message: 'Daily Rise v1.0.0',
                            detail: 'Трекер привычек\n\nСоздавай привычки. Достигай целей.'
                        });
                    }
                },
                { type: 'separator' },
                { label: 'Выход', accelerator: 'Alt+F4', click: () => app.quit() }
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
    createWindow();
    // Запускаем бэкенд после создания окна с небольшой задержкой
    setTimeout(() => {
        startBackend();
    }, 500);
});

app.on('window-all-closed', () => {
    if (backendProcess && !backendProcess.killed) {
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

app.on('will-quit', (event) => {
    if (backendProcess && !backendProcess.killed) {
        backendProcess.kill();
        // Даём время на завершение
        setTimeout(() => {}, 100);
    }
});
