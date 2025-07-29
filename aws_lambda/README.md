

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

# (alternativa de deploy) Utilziar AWS Toolkit para VS Code

1. Faça login na AWS > selecione o serviço IAM > selecione Usuários.
2. Crie um usuário novo e atribua a ele um grupo de administrador com permissões completas para todas as operações.
3. Clique no usuário recem criado que deve aparecer na lista de usuários dentro do serviço IAM
4. Selecione Credenciais de Segurança > Criar Chave de Acesso
5. Salve a secret e access keys (essas 2 chaves são necessárias para login com usuário IAM)
6. Baixe a extensão AWS Tollkit dentro do VS Code
7. Faça login IAM ocm o nome de usuário e as duas chaves.
8. Coloque o novo arquivo python com o código da função lambda
9. Execute ´pip install -r requirements.txt --target .´
