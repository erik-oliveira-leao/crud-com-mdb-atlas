## CRUD com mongodb atlas

crie um arquivo chado server.py e instale a biblioteca do flask e mongo
```bash
pip install flask pymongo dnspython
```
### Passo 1: Criar a Conta no MongoDB Atlas
1. Acesse o site oficial: mongodb.com.
2. Clique no botão "Start Free" (Começar Grátis).
3. Preencha o formulário com seus dados ou clique em "Sign up with Google" para agilizar o processo.
4. Aceite os termos de serviço e clique em "Create your Atlas account".
5. O MongoDB enviará um e-mail de verificação. Acesse sua caixa de entrada e clique no link de confirmação.
### Passo 2: Criar o Projeto e Responder ao Questionário Inicial
Ao entrar pela primeira vez, o Atlas fará algumas perguntas para configurar seu perfil (seu cargo, linguagem de programação de preferência, etc.).
1. Responda às perguntas iniciais e avance.
2. Na tela de boas-vindas, o Atlas geralmente cria um projeto padrão chamado "Project 0".
3. Se quiser criar um novo projeto com um nome personalizado:
- Clique no menu suspenso de projetos no topo esquerdo da tela.
- Selecione "New Project".
- Dite o nome do projeto (ex: MeuProjetoXAMPP) e clique em "Next".
- Clique em "Create Project".
### Passo 3: Criar o Cluster (Banco de Dados)
Dentro do projeto criado, você será direcionado para a tela de implantação do banco de dados.
1. Clique no botão "Create" (ou "Build a Database").
2. Na tela de escolha de planos, selecione a opção M0 (Free), que é a versão 100% gratuita.
3. Configure os detalhes do seu cluster gratuito:
- Provider (Provedor): Escolha AWS, Google Cloud ou Azure (a AWS costuma ser a mais popular).
- Region (Região): Escolha uma região marcada como Free Tier Available mais próxima de você (ex: N. Virginia (us-east-1) ou São Paulo (sa-east-1) se disponível no plano gratuito).
- Name (Nome do Cluster): Você pode deixar como Cluster0 ou dar um nome de sua preferência.
4. Clique no botão "Create" (ou "Create Deployment") no final da página.
5. Resolva o rápido teste de segurança (Captcha), se solicitado. O Atlas levará de 1 a 3 minutos para provisionar seu servidor.
### Passo 4: Configuração Essencial de Segurança (Não pule este passo)
Enquanto o cluster é criado, a tela de Security Quickstart será exibida para que você possa se conectar ao banco depois:
1. Criar Usuário do Banco:
- Digite um Username (Usuário) e uma Password (Senha).
- Clique em "Create Database User". Guarde essa senha, você precisará dela na sua aplicação.
2. Configurar Rede (IP Access List):
- Para testar da sua máquina local, clique em "Add My Current IP Address" (Adicionar meu endereço de IP atual).
- Se preferir liberar o acesso de qualquer lugar para fins de testes, adicione o IP 0.0.0.0/0.
- Clique em "Add Entry".
3. Clique em "Finish and Close" no final da página.

### Pegando a string de conexão

1. Acessar a Tela de Conexão
- Acesse o painel do MongoDB Atlas
- Clique em "Database" no menu lateral esquerdo
- Localize o seu cluster (ex: Cluster0)
- Clique no botão "Connect"
2. Escolher o Método de Conexão
- Escolha a opção "Drivers" (conectar sua aplicação usando a linguagem de programação)
- Selecione o seu Driver (ex: Node.js, Python, PHP, Java)
- no nosso caso é o python
- Escolha a versão do driver instalado no seu projeto
3. Copiar e Ajustar a String
- Copie o código exibido no campo "Connection String"
- O formato padrão será semelhante a este:
```bash
textmongodb+srv://<db_username>:<db_password>@cluster0.xxxx.mongodb.net/?retryWrites=true&w=majority
```
- Substitua <db_username> pelo usuário que você criou no Passo 4
- Substitua <db_password> pela senha gerada para esse usuário
- Remova os símbolos < e > ao preencher os dados



### Como fazer a operação

1. Inicie o servidor:
```bash
python server.py
```
2. No Thunder Client:

- Crie uma request nova
- Método: *POST*
- URL: *http://127.0.0.1:5000/produtos*
- Body: selecione JSON
3. Use este JSON de exemplo:
```bash
{
  "nome": "Camiseta",
  "preco": 49.9,
  "categoria": "Roupas"
}
```
4. Envie. Se der certo, você verá algo como:

```bash
{
  "mensagem": "Produto adicionado com sucesso!",
  "id": "..."
}
```
5. Para verificar se gravou no Atlas, faça outra request:
- Método: *GET*
- URL: *http://127.0.0.1:5000/produtos*
Se você receber uma lista com o produto criado, a conexão com o Atlas está funcionando.