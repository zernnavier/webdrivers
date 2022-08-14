@ECHO OFF


IF /I %1 EQU /? ECHO Automatically downloads the latest driver for given browser verion and puts it in the specified directory.
IF /I %1 EQU --help ECHO %~nx0 ^<Browser-Version:Driver-Version^> ^<Driver-Architecture^> ^<Destination-Directory^>
IF /I %1 EQU --help EXIT /B
IF /I %1 EQU /? ECHO Automatically downloads the latest driver for given browser verion and puts it in the specified directory.
IF /I %1 EQU /? ECHO %~nx0 ^<Browser-Version:Driver-Version^> ^<Driver-Architecture^> ^<Destination-Directory^>
IF /I %1 EQU /? EXIT /B


FOR /F "tokens=1-2 delims=:" %%a IN ("%1") DO @(
    del %3\geckodriver.exe
    curl -kL https://github.com/mozilla/geckodriver/releases/download/v%%b/geckodriver-v%%b-%2.zip -o geckodriver_%%a.zip
    mkdir geckodriver_%%a
    tar -xf geckodriver_%%a.zip -C geckodriver_%%a
    copy .\geckodriver_%%a\geckodriver.exe %3\geckodriver.exe
    rmdir /s /q geckodriver_%%a
    del geckodriver_%%a.zip
)


