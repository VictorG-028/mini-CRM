# Como criar usuário IAM e suas credenciais ?

1. Faça login na AWS > selecione o serviço IAM > selecione Usuários.
2. Crie um usuário novo e atribua a ele um grupo de administrador com permissões completas para todas as operações.
3. Clique no usuário recem criado que deve aparecer na lista de usuários dentro do serviço IAM
4. Selecione Credenciais de Segurança > Criar Chave de Acesso
5. Salve a secret e access keys (essas 2 chaves são necessárias para login com usuário IAM)

# Como subir a infra na AWS

1. Baixe a AWS CLI (`choco install awscli -y`)
2. Execute `aws configure` e faça login com usuário IAM
3. Verifique a região da AWS desejada e execute o comando abaixo
```bash
aws cloudformation deploy \
  --template-file infra.yaml \
  --stack-name send-periodicaly-discount-emails-IaC \
  --capabilities CAPABILITY_NAMED_IAM \
  --region eu-north-1
```

# Formas de deploy

## Deploy manual

1. Garanta que o conda está ativado em um ambiente com permissão para baixar 
pacotes ou não utilize nenhum gerenciador de ambientes virtuais python.

```bash
# Dica: esse comando faz o conda não iniciar automaticamente no terminal
conda config --set auto_activate_base false
```

2. [<u>opcional para windows e obrigatório para ambiente Linux</u>] baixe o binário ´zip´ usando Chocolatey (´choco install zip´) ou sudo (´sudo apt install zip´) e 
garanta que o caminho para o binário está na string **path** das 
variáveis de ambiente Windows. 

3. Execute o script bash
```bash
./build_lambda.sh
```

4. Faça log in na AWS, entre no serviço de lambda, selecione ou crie a 
lamba e arraste a selecione deploy com pasta zip.

## (alternativa de deploy) Utilziar AWS Toolkit para VS Code

1. Crie um usuário IAM e pegue suas credênciais
2. Baixe a extensão AWS Tollkit dentro do VS Code
3. Faça login IAM ocm o nome de usuário e as duas chaves.
4. Coloque o novo arquivo python com o código da função lambda
5. Execute ´pip install -r requirements.txt --target .´

## Deploy automático

1. Crie um usuário IAM e pegue suas credênciais
2. No repositório do GitHub, acesse Settings > Secrets and variables > Actions > New repository secret
3. Coloque as credênciais IAM (`AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`) nos segredos da conta do github 
4. Ao atualizar qualquer arquivo dentro de `aws_lamdba/src`, ou o arquivo `requirements.txt`, ou `auto-update-lambda.yml`, o GitHub action irá automaticamente executar o build + deploy do código fonte lambda.
5. Confira e garanta que a região da AWS desejada está sendo utilizada no arquivo `auto-update-lambda.yml`. 
