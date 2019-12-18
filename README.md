# Desafio Magalu

#### Candidato: João Medrado Gondim

Esta documentação tem como objetivo auxiliar na execução da API criada.

 - Ambiente virtual:
	 - Para garantir o correto funcionamento da aplicação, utilize o ambiente virtual que foi enviado junto com o repositório. Para instalação, executar:
		 - `pip install virtualenv`
	 - dentro da pasta da API, digitar
		 - `source desafiomagalu/bin/activate`
	 - Instale as libs usadas na API com o comando
		 - `pip install requirements.txt`
	- Rode a aplicação com o comando:
		- `python app.py`

- A aplicação:

A aplicação consiste em três arquivos principais:
- app.py que contem as rotas para uso da API e acesso ao banco (feito utilizando o SQLAlchemy junto com SQLite3);
- models/clients.py com os modelos necessários para o devido funcionamento do cliente;
- resources/clients.py que possui todas as funções de GET, POST, PUT e DEL tanto para o CRUD de cliente quando para a criação de sua lista de produtos bem como a adição de produtos à mesma.

Exemplos de requisição:

- /signup para criar usuários
	- o body da requisição deve conter um json com email e nome do usuário;
- /clients para acessar uma lista com todos os clientes, seus nomes, email e lista de produtos;
- /showClientProduct/\<email>/\<id> para mostrar o produto de \<id> do usuário de \<email>;
- /client/\<email> para acessar um cliente específico;
- /login para fazer login com um usuário
	- o body da requisição deve conter um json com o email e o nome do usuário;
	- **a resposta da requisição vai conter um token que deve ser utilizado para as próximas requisições**
- /update/\<email> para atualizar o nome de um usuário;
- /delete/\<email> para excluir um usuário;
- /addProduct/\<email> para adicionar um produto ao usuário de \<email>;
	- o body da requisição deve conter: price, image, brand, id, title e reviewScore (não obrigatório);

###TO DO:
 - [ ] Pegar dados do produto pela url + id;
 - [ ] Utilizar outro banco (Mongo, MySQL) no lugar de SQLite3;
 - [ ] Separar códigos de lista de produto para melhor visualização da aplicação.
