#!/bin/bash
echo "Started executing $0"

# Preparação da pasta
mkdir -p package
pip install -r requirements.txt --target package/
cp requirements.txt package/
cp lambda_function.py package/
cd package

# Compactação com fallback
if command -v zip &> /dev/null; then
  echo "Usando o comando zip..."
  zip -r ../builded_lambda.zip .
else
  echo "Comando zip não encontrado. Tentando usar PowerShell..."

  powershell.exe -Command '
    $items = Get-ChildItem -Recurse -Force | Where-Object { -not $_.PSIsContainer } | Select-Object -ExpandProperty FullName;
    Compress-Archive -Path $items -DestinationPath "../builded_lambda.zip" -Force
  '

  if [ $? -ne 0 ]; then
    echo "Falha ao criar o ZIP com PowerShell."
    echo "Baixe o binário ´zip´ usando Chocolatey (´choco install zip´) e garanta que o caminho está no PATH."
    exit 1
  fi
fi

cd ..
echo "Finished executing $0"
