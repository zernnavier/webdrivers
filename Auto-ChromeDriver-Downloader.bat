@ECHO OFF


IF /I %1 EQU --help ECHO Automatically downloads the matching driver for given browser verion and puts it in the specified directory.
IF /I %1 EQU --help ECHO %~nx0 ^<Browser-Version^> ^<Driver-Architecture^> ^<Destination-Directory^>
IF /I %1 EQU --help EXIT /B
IF /I %1 EQU /? ECHO Automatically downloads the matching driver for given browser verion and puts it in the specified directory.
IF /I %1 EQU /? ECHO %~nx0 ^<Browser-Version^> ^<Driver-Architecture^> ^<Destination-Directory^>
IF /I %1 EQU /? EXIT /B


FOR /F "tokens=1-4 delims=." %%a IN ("%1") DO @curl -k https://chromedriver.storage.googleapis.com/LATEST_RELEASE_%%a.%%b.%%c | FOR /F "tokens=*" %%k IN ('more') DO @(
	del %3\chromedriver.exe
	curl -kL https://chromedriver.storage.googleapis.com/%%k/chromedriver_%2.zip -o chromedriver_%%k.zip
	mkdir chromedriver_%%k
	tar -xf chromedriver_%%k.zip -C chromedriver_%%k
	copy .\chromedriver_%%k\chromedriver.exe %3\chromedriver.exe
	rmdir /s /q chromedriver_%%k
	del chromedriver_%%k.zip
)
