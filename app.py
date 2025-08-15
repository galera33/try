from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from datetime import datetime
import json
import os
import uvicorn

app = FastAPI()

ARQUIVO_JSON = "dados.json"

# Funções utilitárias
def carregar_dados():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_dados(lista):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

# Página HTML principal (formulário + tabela)
@app.get("/", response_class=HTMLResponse)
def form_page():
    usuarios = carregar_dados()

    tabela_html = """
    <table border="1" style="width:100%; border-collapse: collapse; margin-top: 20px;">
        <tr style="background-color: #ddd;">
            <th>CPF</th>
            <th>Nome</th>
            <th>Email</th>
            <th>Telefone</th>
            <th>Data Cadastro</th>
        </tr>
    """
    for u in usuarios:
        tabela_html += f"""
        <tr>
            <td>{u['cpf']}</td>
            <td>{u['nome']}</td>
            <td>{u['email']}</td>
            <td>{u['telefone']}</td>
            <td>{u['data_cadastro']}</td>
        </tr>
        """
    tabela_html += "</table>" if usuarios else "<p style='color:white;'>Nenhum usuário cadastrado ainda.</p>"

    return f"""
    <html>
        <head>
            <style>
                body {{
                    background-color: #000000;
                    font-family: Arial, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    margin: 0;
                    padding: 20px;
                    color: white;
                }}
                .form-container {{
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
                    width: 400px;
                }}
                .logo-container {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .logo {{
                    max-width: 300px;
                    max-height: 200px;
                }}
                h2 {{
                    color: #333333;
                    text-align: center;
                    margin-top: 0;
                    margin-bottom: 20px;
                }}
                table td, table th {{
                    padding: 8px;
                    text-align: center;
                    border: 1px solid #ccc;
                }}
                label {{
                    font-weight: bold;
                    color: #333333;
                }}
                input[type="text"],
                input[type="email"] {{
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #dddddd;
                    border-radius: 4px;
                    box-sizing: border-box;
                }}
                button {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    width: 100%;
                    font-size: 16px;
                    margin-top: 10px;
                }}
                button:hover {{
                    background-color: #45a049;
                }}
                .tabela-container {{
                    width: 90%;
                    margin-top: 40px;
                }}
            </style>
        </head>
        <body>
            <div class="form-container">
                <div class="logo-container">
                    <img src="/PIC.png" alt="Logo da Empresa" class="logo">
                </div>
                <h2>Cadastro de Usuário</h2>
                <form action="/cadastrar" method="post">
                    <table>
                        <tr>
                            <td><label>CPF:</label></td>
                            <td><input type="text" name="cpf" required></td>
                        </tr>
                        <tr>
                            <td><label>Nome:</label></td>
                            <td><input type="text" name="nome" required></td>
                        </tr>
                        <tr>
                            <td><label>Email:</label></td>
                            <td><input type="email" name="email" required></td>
                        </tr>
                        <tr>
                            <td><label>Telefone:</label></td>
                            <td><input type="text" name="telefone" required></td>
                        </tr>
                    </table>
                    <button type="submit">Cadastrar</button>
                </form>
            </div>
            <div class="tabela-container">
                {tabela_html}
            </div>
        </body>
    </html>
    """

# Rota para servir logo
@app.get("/PIC.png")
async def get_logo():
    return FileResponse("PIC.png")

# Cadastrar usuário
@app.post("/cadastrar", response_class=HTMLResponse)
def cadastrar(cpf: str = Form(...), nome: str = Form(...), email: str = Form(...), telefone: str = Form(...)):
    dados = carregar_dados()

    novo_usuario = {
        "cpf": cpf,
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    dados.append(novo_usuario)
    salvar_dados(dados)

    return """
    <html>
        <head>
            <meta http-equiv="refresh" content="5;url=/" />
            <style>
                body {
                    background-color: #000000;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    color: white;
                    text-align: center;
                }
                .message-container {
                    background-color: rgba(0, 0, 0, 0.7);
                    padding: 30px;
                    border-radius: 10px;
                    max-width: 500px;
                }
                h3 {
                    color: #4CAF50;
                }
            </style>
        </head>
        <body>
            <div class="message-container">
                <h3>Usuário cadastrado com sucesso!</h3>
                <p>Você será redirecionado para cadastrar um novo usuário em 5 segundos...</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
