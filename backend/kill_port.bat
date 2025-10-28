@echo off
echo Killing processes using port 8000...

FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') DO (
    echo Killing process with PID: %%P
    taskkill /F /PID %%P
)

echo Done.
