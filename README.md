# CRUD_Python_Flask
## Sistemas Móveis Distribuídos - Projeto Final

SENAC - Análise e Desenvolvimento de Sistemas (3Sem)
Grupo: Alejandro Huller | Barbara de Argolo | Caroline Stelitano | Lucas da Silva | Victor Enriquetto


## Descritivo do Sistema
Exemplo de microsserviços em Flask referente a requisições HTTP manipulando um modelo de dados em SQLite.

Enpoints implementados para testes. Entrada e saída de dados em formato JSON:

-  /pessoas [GET]: retorna com a lista de todas as pessoas
-  /pessoa/cpf [GET]: retorna os dados de uma pessoa pelo CPF. Exemplo: /pessoa/38746283574?token=xyz02
-  /inserirpessoa [GET]: retorna o formulário. 
-  /inserirpessoa [POST]: uma nova pessoa é inserida caso o CPF já não esteja cadastrado no banco. 
- /atualizarpessoa/cpf [GET]:  retorna o formulário com o CPF solicitado, caso o CPF seja encontrado. 
- /atualizarpessoa/cpf [POST]:  atualiza uma pessoa tendo com corpo de entrada um objeto JSON. Se o CPF mencionado for encontrado, os dados são atualizados. Exemplo: atualizarpessoa/38746283574?token=xyz02
-  /removerpessoa/cpf  [DELETE]: remove um CPF tendo retorno 'Pessoa removida com sucesso' se removido ou 'Pessoa não encontrada' se o CPF não for encontrado. Exemplo: /removerpessoa/00000000089?token=xyz02
Nota: o sistema de remover pessoa foi implementado nos métodos GET e DELETE para rodar tanto na web quanto no Postman.

Foi implementado um sistema de verificação de token necessário para executar todos os serviços.

## Projeto

Link no Replit: https://replit.com/@carolegal/ProvaFinal-v1#main.py  
https://provafinal-v1.carolegal.repl.co/
