@ECHO OFF

IF /I %1 EQU --help ECHO Automatically downloads the matching driver for given browser verion and puts it in the specified directory.
IF /I %1 EQU --help ECHO %~nx0 ^<Browser-Version^> ^<Driver-Architecture^> ^<Destination-Directory^>
IF /I %1 EQU --help EXIT /B
IF /I %1 EQU /? ECHO Automatically downloads the matching driver for given browser verion and puts it in the specified directory.
IF /I %1 EQU /? ECHO %~nx0 ^<Browser-Version^> ^<Driver-Architecture^> ^<Destination-Directory^>
IF /I %1 EQU /? EXIT /B


del %3\msedgedriver.exe
curl -kL https://msedgedriver.azureedge.net/%1/edgedriver_%2.zip -o edgedriver_%1.zip
mkdir edgedriver_%1
tar -xf edgedriver_%1.zip -C edgedriver_%1
copy .\edgedriver_%1\msedgedriver.exe %3\msedgedriver.exe
rmdir /s /q edgedriver_%1
del edgedriver_%1.zip
