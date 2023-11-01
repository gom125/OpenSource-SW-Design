# OpenSource-SW-Design

2023.11.01
# Install Win-pyenv
## 1. 초코 플랫폼 설치
### CMD에서 설치
> @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

### PowerShell에서 설치
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
> 
> Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

## 2. (powerShell에서) pyenv 설치<br>
  PowerShell 관리자 권한 실행
  choco install pyenv-win

## 3. (powerShell에서) 권한 설정<br>
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
>
> Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"

## 4. path 설정<br>
> [System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
> [System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
> [System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

23.11.01
# ACME unicode 에러
> unicodedecodeerror: 'cp949' codec can't decode byte 0xe2 in position 3591: illegal multibyte sequence
>
> 제어판
> 시계 및 국가의 날짜, 시간 또는 숫자 형식 변경 클릭
> 관리자 옵션 클릭
> 시스템 로캘 변경(C)... 클릭
> Beat: 세계 언어 지원을 위해 Unicode UTF-8 사용 체크

