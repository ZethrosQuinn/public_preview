@echo off
cls

echo Compiling Java files...
javac -d out *.java apps/*.java

if %errorlevel% neq 0 (
    echo Compilation failed!
    exit /b %errorlevel%
)

echo Creating JAR file...
jar cfe Toolbox.jar Toolbox -C out .

if %errorlevel% neq 0 (
    echo JAR creation failed!
    exit /b %errorlevel%
)

echo Build complete! Toolbox.jar is ready.