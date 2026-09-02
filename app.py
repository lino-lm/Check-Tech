from flask import Flask, request, jsonify, render_template, session, redirect
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Chave da sessão
# Para produção, vamos colocar uma chave própria em variável de ambiente.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "checktech-v1-chave-local"
)

# Firebase Realtime Database
link = "https://checktech-8845c-default-rtdb.firebaseio.com"

# Computadores disponíveis na V1
COMPUTADORES = [f"PC-{i:02d}" for i in range(1, 31)]


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def firebase_get(caminho):
    return requests.get(
        link + caminho,
        timeout=10
    )


def firebase_post(caminho, dados):
    return requests.post(
        link + caminho,
        json=dados,
        timeout=10
    )


def resposta_erro(mensagem, status=400):
    return jsonify({
        "sucesso": False,
        "mensagem": mensagem
    }), status


def valor_problema(valor):
    """
    No CheckTech:
    true  = item funcionando
    false = item com problema

    Portanto, quando o valor for false,
    o item deve entrar como problema.
    """

    if isinstance(valor, bool):
        return not valor

    if isinstance(valor, str):
        valor = valor.strip().lower()

        if valor in ["false", "nao", "não", "problema", "ruim"]:
            return True

        if valor in ["true", "sim", "ok", "bom"]:
            return False

    return False

# def valor_problema(valor):
#     """
#     Aceita valores booleanos e algumas strings
#     que podem vir do front.
#     """

#     if isinstance(valor, bool):
#         return valor

#     if isinstance(valor, str):
#         return valor.strip().lower() in [
#             "false",
#             "nao",
#             "não",
#             "problema",
#             "ruim"
#         ]

#     return False


def descobrir_problemas(dados):

    problemas = []

    # Aceita tanto:
    #
    # "itens": {
    #     "mouse": false
    # }
    #
    # quanto os campos diretamente no JSON.

    itens = dados.get("itens")

    if isinstance(itens, dict):
        origem = itens
    else:
        origem = dados

    if valor_problema(origem.get("notebook")):
        problemas.append("Notebook")

    if valor_problema(origem.get("bateria")):
        problemas.append("Bateria")

    if valor_problema(origem.get("carregador")):
        problemas.append("Carregador")

    if valor_problema(origem.get("mouse")):
        problemas.append("Mouse")

    if valor_problema(origem.get("mouse_carregado")):
        problemas.append("Mouse descarregado")

    return problemas


# ==========================================
# PÁGINAS
# ==========================================

@app.route("/")
def inicio():
    return render_template("login.html")


# Mantemos /login como endereço alternativo
@app.route("/login")
def pagina_login():
    return render_template("login.html")


@app.route("/cadastro")
def pagina_cadastro():
    return render_template("cadastro.html")


@app.route("/verificacao")
def pagina_checklist():
    return render_template("checklist.html")


# Nome mais novo do fluxo
@app.route("/checklist")
def pagina_checklist_alias():
    return render_template("checklist.html")


@app.route("/login-professor")
def pagina_login_professor():
    return render_template("professor_login.html")

@app.route("/cadastro-professor")
def pagina_cadastro_professor():
    return render_template("professor_cadastro.html")

@app.route("/professor")
def pagina_professor():

    usuario = session.get("usuario")

    if not usuario or usuario.get("tipo") != "professor":
        return redirect("/login-professor")

    return render_template("professor.html")

@app.route("/computador")
def pagina_computador():
    return render_template("computador.html")


@app.route("/sucesso")
def pagina_sucesso():
    return render_template("sucesso.html")

# ==========================================
# COMPUTADORES
# ==========================================

@app.route("/api/computadores", methods=["GET"])
def computadores():

    return jsonify({
        "sucesso": True,
        "computadores": COMPUTADORES
    })


# ==========================================
# CADASTRO DE ALUNO
# ==========================================

@app.route("/api/cadastro", methods=["POST"])
def cadastro():

    dados = request.get_json(silent=True) or {}

    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""
    serie = dados.get("serie")

    if not email or not senha or not serie:
        return resposta_erro(
            "Preencha todos os campos."
        )

    if not email.endswith("@al.educacao.sp.gov.br"):
        return resposta_erro(
            "Use seu email institucional de aluno."
        )

    if len(senha) < 6:
        return resposta_erro(
            "A senha deve ter pelo menos 6 caracteres."
        )

    if serie not in ["2D1", "2D2", "2D3"]:
        return resposta_erro(
            "Série inválida."
        )

    try:

        resposta = firebase_get(
            "/usuarios.json"
        )

        if resposta.status_code != 200:
            return resposta_erro(
                "Erro ao acessar o sistema.",
                500
            )

        usuarios = resposta.json() or {}

        # Evita cadastro duplicado
        for usuario in usuarios.values():

            if usuario.get("email") == email:

                return resposta_erro(
                    "Este email já está cadastrado.",
                    409
                )

        dados_usuario = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "serie": serie,
            "tipo": "aluno"
        }

        resposta = firebase_post(
            "/usuarios.json",
            dados_usuario
        )

        if resposta.status_code == 200:

            return jsonify({
                "sucesso": True,
                "mensagem": "Usuário cadastrado com sucesso!"
            })

        return resposta_erro(
            "Erro ao cadastrar usuário.",
            500
        )

    except requests.RequestException:

        return resposta_erro(
            "Não foi possível conectar ao Firebase.",
            503
        )


# ==========================================
# LOGIN DO ALUNO
# ==========================================

@app.route("/api/login", methods=["POST"])
def login():

    dados = request.get_json(silent=True) or {}

    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""
    serie = dados.get("serie")

    if not email or not senha or not serie:

        return resposta_erro(
            "Preencha todos os campos."
        )

    if not email.endswith("@al.educacao.sp.gov.br"):

        return resposta_erro(
            "Use seu email institucional."
        )

    if len(senha) < 6:

        return resposta_erro(
            "Senha inválida."
        )

    if serie not in ["2D1", "2D2", "2D3"]:

        return resposta_erro(
            "Série inválida."
        )

    try:

        resposta = firebase_get(
            "/usuarios.json"
        )

        if resposta.status_code != 200:

            return resposta_erro(
                "Erro ao acessar o sistema.",
                500
            )

        usuarios = resposta.json() or {}

        for id_usuario, usuario in usuarios.items():

            if (
                usuario.get("email") == email
                and usuario.get("senha") == senha
                and usuario.get("serie") == serie
                and usuario.get("tipo") == "aluno"
            ):

                # Guarda os dados básicos da sessão
                session["usuario"] = {
                    "id": id_usuario,
                    "nome": usuario.get("nome", ""),
                    "email": email,
                    "serie": serie,
                    "tipo": "aluno"
                }

                return jsonify({

                    "sucesso": True,

                    "mensagem":
                        "Login realizado com sucesso!",

                    "nome":
                        usuario.get("nome", ""),

                    "email":
                        email,

                    "serie":
                        serie
                })

        return resposta_erro(
            "Email, senha ou série incorretos.",
            401
        )

    except requests.RequestException:

        return resposta_erro(
            "Não foi possível conectar ao Firebase.",
            503
        )


# ==========================================
# LOGIN DO PROFESSOR
# ==========================================

@app.route("/api/login-professor", methods=["POST"])
def login_professor():

    dados = request.get_json(silent=True) or {}

    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    if not email or not senha:

        return resposta_erro(
            "Preencha todos os campos."
        )

    if not email.endswith(
        "@prof.educacao.sp.gov.br"
    ):

        return resposta_erro(
            "Use seu email institucional de professor."
        )

    if len(senha) < 6:

        return resposta_erro(
            "Senha inválida."
        )

    try:

        resposta = firebase_get(
            "/usuarios.json"
        )

        if resposta.status_code != 200:

            return resposta_erro(
                "Erro ao acessar o sistema.",
                500
            )

        usuarios = resposta.json() or {}

        for id_usuario, usuario in usuarios.items():

            if (
                usuario.get("email") == email
                and usuario.get("senha") == senha
                and usuario.get("tipo") == "professor"
            ):

                session["usuario"] = {
                    "id": id_usuario,
                    "nome": usuario.get("nome", ""),
                    "email": email,
                    "tipo": "professor"
                }

                return jsonify({

                    "sucesso": True,

                    "mensagem":
                        "Login de professor realizado com sucesso!",

                    "nome":
                        usuario.get("nome", ""),

                    "email":
                        email
                })

        return resposta_erro(
            "Email ou senha incorretos.",
            401
        )

    except requests.RequestException:

        return resposta_erro(
            "Não foi possível conectar ao Firebase.",
            503
        )
# ==========================================
# CADASTRO DE PROFESSOR
# ==========================================

@app.route("/api/cadastro-professor", methods=["POST"])
def cadastro_professor():

    dados = request.get_json(silent=True) or {}

    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""
    codigo = (dados.get("codigo") or "").strip()

    if not nome or not email or not senha or not codigo:
        return resposta_erro(
            "Preencha todos os campos."
        )

    if not email.endswith("@prof.educacao.sp.gov.br"):
        return resposta_erro(
            "Use seu email institucional de professor."
        )

    if len(senha) < 6:
        return resposta_erro(
            "A senha deve ter pelo menos 6 caracteres."
        )

    # Código necessário para criar uma conta de professor.
    # No deploy, podemos colocar isso em variável de ambiente.
    codigo_correto = os.environ.get(
        "PROFESSOR_CODIGO",
        "CHECKTECH2026"
    )

    if codigo != codigo_correto:
        return resposta_erro(
            "Código de acesso do professor incorreto.",
            401
        )

    try:

        resposta = firebase_get(
            "/usuarios.json"
        )

        if resposta.status_code != 200:
            return resposta_erro(
                "Erro ao acessar o sistema.",
                500
            )

        usuarios = resposta.json() or {}

        # Verifica se o email já existe
        for usuario in usuarios.values():

            if usuario.get("email") == email:

                return resposta_erro(
                    "Este email já está cadastrado.",
                    409
                )

        dados_professor = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "tipo": "professor"
        }

        resposta = firebase_post(
            "/usuarios.json",
            dados_professor
        )

        if resposta.status_code == 200:

            return jsonify({
                "sucesso": True,
                "mensagem": "Professor cadastrado com sucesso!"
            })

        return resposta_erro(
            "Erro ao cadastrar professor.",
            500
        )

    except requests.RequestException:

        return resposta_erro(
            "Não foi possível conectar ao Firebase.",
            503
        )

# ==========================================
# LOGOUT
# ==========================================

@app.route("/api/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "sucesso": True,
        "mensagem": "Sessão encerrada."
    })


# ==========================================
# ENVIAR CHECKLIST
# ==========================================

@app.route("/api/checklist", methods=["POST"])
def checklist():

    dados = request.get_json(silent=True) or {}

    computador = dados.get("computador")

    if computador not in COMPUTADORES:

        return resposta_erro(
            "Computador inválido."
        )

    # Aceitamos dois formatos:
    #
    # Formato atual:
    # {
    #   "notebook": true,
    #   "mouse": false
    # }
    #
    # Formato organizado:
    # {
    #   "itens": {
    #       "notebook": true,
    #       "mouse": false
    #   }
    # }

    itens = dados.get("itens")

    if isinstance(itens, dict):

        notebook = itens.get("notebook")
        mouse = itens.get("mouse")
        bateria = itens.get("bateria")
        carregador = itens.get("carregador")
        mouse_carregado = itens.get(
            "mouse_carregado"
        )

    else:

        notebook = dados.get("notebook")
        mouse = dados.get("mouse")
        bateria = dados.get("bateria")
        carregador = dados.get("carregador")
        mouse_carregado = dados.get(
            "mouse_carregado"
        )

    observacoes = (
        dados.get("observacoes") or ""
    ).strip()

    problemas = descobrir_problemas(dados)

    tem_problema = len(problemas) > 0

    usuario = session.get(
        "usuario",
        {}
    )

    aluno = (
        dados.get("aluno")
        or usuario.get("nome")
        or usuario.get("email", "")
    )

    serie = (
        dados.get("serie")
        or usuario.get("serie", "")
    )

    dados_checklist = {

        "computador": computador,

        "aluno": aluno,

        "serie": serie,

        "notebook": notebook,

        "mouse": mouse,

        "bateria": bateria,

        "carregador": carregador,

        "mouse_carregado":
            mouse_carregado,

        # Comentários dos alunos no Hub
        "observacoes": observacoes,

        "problema": tem_problema,

        "problemas": problemas,

        "data":
            datetime.now().isoformat(
                timespec="seconds"
            )
    }

    try:

        resposta = firebase_post(
            "/checklists.json",
            dados_checklist
        )

        if resposta.status_code == 200:

            return jsonify({

                "sucesso": True,

                "mensagem":
                    "Checklist enviado com sucesso!",

                "id":
                    resposta.json().get("name")
            })

        return resposta_erro(
            "Erro ao enviar o checklist.",
            500
        )

    except requests.RequestException:

        return resposta_erro(
            "Não foi possível conectar ao Firebase.",
            503
        )


# ==========================================
# PAINEL DO PROFESSOR
# ==========================================

@app.route(
    "/api/professor/dashboard",
    methods=["GET"]
)
def professor_dashboard():

    usuario = session.get("usuario")

    if not usuario or usuario.get("tipo") != "professor":
        return resposta_erro(
            "Acesso não autorizado.",
            403
        )

    try:

        resposta = firebase_get(
            "/checklists.json"
        )

        if resposta.status_code != 200:

            return resposta_erro(
                "Erro ao acessar os checklists.",
                500
            )

        checklists = resposta.json() or {}

    except requests.RequestException:

        return resposta_erro(
            "Não foi possível conectar ao Firebase.",
            503
        )

    # Nenhum checklist ainda
    if not checklists:
        return jsonify({

        "sucesso": True,

        "professor": {
            "nome": usuario.get("nome", "Professor"),
            "email": usuario.get("email", "")
        },

        "total_pcs":
            len(COMPUTADORES),

            "problemas_pcs": 0,

            "ultima_checagem": None,

            "problemas": [],

            "comentarios": [],

            "ultimas_verificacoes": []
        })

    # ==========================================
    # ÚLTIMO CHECKLIST DE CADA PC
    # ==========================================

    ultimo_por_pc = {}

    for id_checklist, dados in checklists.items():

        computador = dados.get(
            "computador"
        )

        data = dados.get(
            "data"
        ) or ""

        if computador not in COMPUTADORES:
            continue

        anterior = ultimo_por_pc.get(
            computador
        )

        if (
            anterior is None
            or data > anterior.get(
                "data",
                ""
            )
        ):

            ultimo_por_pc[computador] = {
                **dados,
                "id": id_checklist
            }

    problemas = []

    comentarios = []

    ultimas_verificacoes = []

    # ==========================================
    # PROCESSAR DADOS
    # ==========================================

    for computador, dados in ultimo_por_pc.items():

        itens_problema = dados.get(
            "problemas"
        )

        if not isinstance(
            itens_problema,
            list
        ):

            itens_problema = descobrir_problemas(
                dados
            )

        tem_problema = (
            len(itens_problema) > 0
        )

        registro = {

            "computador":
                computador,

            "aluno":
                dados.get(
                    "aluno",
                    ""
                ),

            "serie":
                dados.get(
                    "serie",
                    ""
                ),

            "problemas":
                itens_problema,

            "observacoes":
                dados.get(
                    "observacoes",
                    ""
                ),

            "data":
                dados.get(
                    "data"
                )
        }

        ultimas_verificacoes.append(
            registro
        )

        if tem_problema:

            problemas.append(
                registro
            )

        # "Comentários dos alunos"
        # = campo "observacoes"
        if dados.get("observacoes"):

            comentarios.append({

                "computador":
                    computador,

                "aluno":
                    dados.get(
                        "aluno",
                        ""
                    ),

                "observacoes":
                    dados.get(
                        "observacoes"
                    ),

                "data":
                    dados.get(
                        "data"
                    )
            })

    # Mais recentes primeiro
    ultimas_verificacoes.sort(
        key=lambda x:
            x.get("data") or "",
        reverse=True
    )

    problemas.sort(
        key=lambda x:
            x.get("data") or "",
        reverse=True
    )

    comentarios.sort(
        key=lambda x:
            x.get("data") or "",
        reverse=True
    )

    ultima_checagem = None

    if ultimas_verificacoes:

        ultima_checagem = (
            ultimas_verificacoes[0]
            .get("data")
        )

    return jsonify({

    "sucesso": True,

    "professor": {
        "nome": usuario.get("nome", "Professor"),
        "email": usuario.get("email", "")
    },

    "total_pcs":
        len(COMPUTADORES),

        # PCs cujo ÚLTIMO checklist
        # apresenta problema
        "problemas_pcs":
            len(problemas),

        "ultima_checagem":
            ultima_checagem,

        "problemas":
            problemas,

        "comentarios":
            comentarios[:10],

        "ultimas_verificacoes":
            ultimas_verificacoes[:10]
    })


# ==========================================
# COMPATIBILIDADE COM ROTA ANTIGA
# ==========================================

@app.route(
    "/api/professor/verificacoes",
    methods=["GET"]
)
def professor_verificacoes():

    return professor_dashboard()


# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)