

# Preparação de ambiente, build e deploy

1. Garanta que o conda está em um ambiente com permissão para baixar pacotes
ou não utilize nenhum gerenciador de ambientes virtuais python.

2. [<u>opcional para windows e obrigatório para ambiente Linux</u>] baixe o binário ´zip´ usando Chocolatey (´choco install zip´) ou sudo (´sudo apt install zip´) e 
garanta que o caminho para o binário está na string **path** das 
variáveis de ambiente Windows. 

3. Execute o script bash
```bash
cd aws_lambda
./build_lambda.sh
```

4. Faça log in na AWS, entre no serviço de lambda, selecione ou crie a 
lamba e arraste a selecione deploy com pasta zip.
