#Alejandro Huller | Barbara de Argolo | Caroline Stelitano | Lucas da Silva | Victor Enriquetto

import os 
from flask import Flask, jsonify, request, render_template
import json
import sqlite3
import sqlite3 as sql

app = Flask(__name__)


@app.route('/', methods=['GET'])
def raiz():
    return render_template('index.html')

@app.route('/pessoas', methods=['GET'])
def pessoa():
  #Connecting to sqlite
  conn = sqlite3.connect('banco.db')
  #Habilita o acesso das colunas por nome
  conn.row_factory = sqlite3.Row 
  #Creating a cursor object using the cursor() method
  cursor = conn.cursor()
  #Retrieving data
  cursor.execute('''SELECT * from Pessoa''')
  #Fetching 1st row from the table
  result = cursor.fetchall();
  #Commit your changes in the database
  conn.commit()
  #Closing the connection
  conn.close()
  #devolvendo o resultado do cursor já convertido em formato JSON
  return jsonify([dict(ix) for ix in result])

#Função de autenticação
def autenticar(request):
  token = request.args.get('token')
  if request.method != 'GET':
    token = request.form.get('token')
  return token == 'xyz02'
  
#Procurar pessoa por cpf
@app.route('/pessoa/<cpf>', methods=['GET'])
def pessoaCPF(cpf):
  if autenticar(request) == False:
    return render_template('naoAutenticado.html')
  conn = sqlite3.connect('banco.db')
  conn.row_factory = sqlite3.Row 
  cursor = conn.cursor()
  cursor.execute("SELECT * from Pessoa where cpf =?",[cpf])
  result = cursor.fetchall();
  conn.commit()
  conn.close()
  return jsonify([dict(ix) for ix in result]) 

#inserir pessoa
@app.route('/inserirpessoa', methods=['GET'])
def inserirpessoaForm():
   return render_template('pessoa.html')
  
@app.route('/inserirpessoa', methods=['POST'])
def inserirpessoa():
  if autenticar(request) == False:
    return render_template('naoAutenticado.html')
  resultado = ""
  try:
    cpf = request.form["cpf"]
    nome = request.form["nome"]
    sobrenome = request.form["sobrenome"]
    data_nasc = request.form["data_nasc"]
    
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    result = cursor.execute("SELECT count(*) as total from Pessoa where cpf=?", [cpf])
    result = result.fetchall()
  
    if result[0]['total'] > 0:
      resultado = "CPF já cadastrado."
    else:
      cursor.execute("INSERT INTO pessoa (cpf, nome,sobrenome,data_nasc) VALUES (?,?,?,?)",(cpf, nome, sobrenome, data_nasc))
      conn.commit()
      resultado = "Pessoa adicionada com sucesso." 
  except Exception as e: 
    print(e)
    conn.rollback()
    resultado = "Erro ao inserir pessoa."
  finally:
    return render_template("resultado.html",resultado = resultado)  
    conn.close()

#atualizar pessoa
@app.route('/atualizarpessoa/<cpf>', methods=['GET'])
def atualizarpessoaForm(cpf):
  if autenticar(request) == False:
    return render_template('naoAutenticado.html')
  conn = sqlite3.connect('banco.db')
  conn.row_factory = sqlite3.Row 
  cursor = conn.cursor()
  cursor.execute("SELECT cpf, nome, sobrenome, data_nasc from Pessoa where cpf=?", [cpf])
  result = cursor.fetchone();
  conn.commit()
  conn.close()

  return render_template('atualizarPessoa.html', cpf=result[0], nome=result[1], sobrenome=result[2], data_nasc=result[3])
      
@app.route('/atualizarpessoa/<cpf>', methods= ['POST'])
def atualizarpessoa(cpf):
  if autenticar(request) == False:
    return render_template('naoAutenticado.html')
  conn = sqlite3.connect('banco.db')
  cursor = conn.cursor()
  cpf = request.form ["cpf"]
  nome = request.form ["nome"]
  sobrenome = request.form ["sobrenome"]
  data_nasc = request.form ["data_nasc"]
  cursor.execute("UPDATE pessoa SET cpf = ?, nome = ?, sobrenome = ?, data_nasc = ? WHERE cpf=? ", [cpf, nome, sobrenome, data_nasc, cpf])
  conn.commit()
  conn.close()
  return render_template("resultado.html", resultado="Pessoa atualizada com sucesso.")
  
#Remover pessoa por cpf
#Colocamos métodos GET para rodar na web e o DELETE no Postman
@app.route('/removerpessoa/<cpf>', methods=['GET', 'DELETE'])
def removerpessoa(cpf):
  if autenticar(request) == False:
    return render_template('naoAutenticado.html')
  resultado = ""
  try:
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    result = cursor.execute("SELECT count(*) as total from Pessoa where cpf=?", [cpf])
    result = result.fetchall()
    
    if result[0]['total'] > 0:
      cursor.execute("DELETE FROM pessoa WHERE cpf=?", [cpf])
      conn.commit()
      resultado = "Pessoa removida com sucesso."
    else:
      resultado = "Pessoa não encontrada."
  except Exception as e: 
    print(e)
    conn.rollback()
    resultado = "Erro ao remover pessoa."
  finally:
    return render_template("resultado.html", resultado=resultado)
    conn.close()
  
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)