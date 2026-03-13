@echo off
SETLOCAL

:: Caminho do ambiente virtual
SET VENV_DIR=venv

echo [1/4] Criando ambiente virtual em %VENV_DIR%...
python -m venv %VENV_DIR%
IF ERRORLEVEL 1 (
    echo Erro ao criar o ambiente virtual.
    EXIT /B 1
)

echo [2/4] Atualizando pip...
%VENV_DIR%\Scripts\python.exe -m pip install --upgrade pip
IF ERRORLEVEL 1 (
    echo Erro ao atualizar pip.
    EXIT /B 1
)

echo [3/3] Instalando dependências do requirements.txt...
IF EXIST requirements.txt (
    %VENV_DIR%\Scripts\pip.exe install -r requirements.txt
    IF ERRORLEVEL 1 (
        echo Erro ao instalar dependências.
        EXIT /B 1
    )
    echo Dependências instaladas com sucesso.
) ELSE (
    echo Arquivo requirements.txt não encontrado. Nenhuma dependência instalada.
)

echo ✅ Setup concluído com sucesso.
ENDLOCAL
