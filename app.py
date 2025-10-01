# Autor João Victor e Silva





# ============================================================
#  FLASK APP - CLASSIFICADOR DE TEXTOS
#  Organização do código:
#     1 - Configurações iniciais
#     2 - Funções auxiliares
#     3 - Funções principais
#     4 - Rotas
#     5 - Inicialização
# ============================================================

 
# -------------------------- 1 - Configuraçoes Inciais -----------------------
from flask import Flask, render_template, request
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename
import fitz
from dotenv import load_dotenv




load_dotenv()
app = Flask(__name__)

PASTA_UPLOADS = "uploads"
os.makedirs(PASTA_UPLOADS, exist_ok=True)
app.config["UPLOAD_FOLDER"] = PASTA_UPLOADS

EXTENSOES_PERMITIDAS = {".pdf", ".txt"}


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ----------------- 2 - Funções auxiliares --------------------


# o objetivo dessa função e nao deixar inserir arquivos que nao sejam PDF ou TXT
def arquivo_permitido(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in EXTENSOES_PERMITIDAS




# o objetivo dessa funcao e salvar os arquivos e enviar para a pasta uploads
def salvar_arquivo(uploaded_file):
    nome_arquivo = secure_filename(uploaded_file.filename)
    caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)
    uploaded_file.save(caminho)
    return caminho


# ----------------- 3 - Funções principais --------------------



#o objetivo dessa funcao é extrair o texto do PDF ou do TXT para a IA poder ler
def extrair_texto(arquivo_caminho):
    
    if arquivo_caminho.endswith(".pdf"):
        texto = ""
        doc = fitz.open(arquivo_caminho)
        for pagina in doc:
            texto += pagina.get_text("text")
        doc.close()
        return texto

    elif arquivo_caminho.endswith(".txt"):
        with open(arquivo_caminho, "r", encoding="utf-8") as f:
            return f.read()

    return ""





# o objetivo dessa funcao é criar um prompt para a IA Gemini poder ler o email 
# e baseado no prompt o email sera classificado como produtivo ou improdutivo
def classificar_texto(texto):
    modelo = genai.GenerativeModel("gemini-2.5-flash")
    prompt_cat = f"""
    Classifique o texto abaixo como "Produtivo" (se for um email/texto de trabalho,
    pedido de informação, solicitação) ou "Improdutivo" (se for apenas cumprimento,
    agradecimento, felicitação, sem necessidade de ação).
    Texto: {texto}
    Responda apenas com a categoria.
    """
    resp_cat = modelo.generate_content([{"parts": [{"text": prompt_cat}]}])
    categoria = resp_cat.text.strip()

    if "Produtivo" in categoria:
        resposta = modelo.generate_content(
            [{"parts": [{"text": f"Escreva uma resposta profissional e educada para este texto de trabalho: {texto}"}]}]
        ).text
    else:
        resposta = modelo.generate_content(
            [{"parts": [{"text": f"Escreva uma resposta curta e simpática agradecendo este texto social: {texto}"}]}]
        ).text
    return categoria, resposta




# ----------------- 4 - Rotas --------------------
@app.route("/", methods=["GET", "POST"])
def index():
    categoria, resposta = None, None
    if request.method == "POST":
        texto_email = request.form.get("email_text")
        arquivo = request.files.get("file")
        if texto_email:
            categoria, resposta = classificar_texto(texto_email)
        elif arquivo and arquivo.filename != "":
            if not arquivo_permitido(arquivo.filename):
                categoria, resposta = "Erro", "Tipo de arquivo não permitido. Use apenas PDF ou TXT."
            else:
                caminho = salvar_arquivo(arquivo)
                texto = extrair_texto(caminho)

                if texto.strip():
                    categoria, resposta = classificar_texto(texto)
                else:
                    categoria, resposta = "Erro", "Não foi possível extrair texto do arquivo."

    return render_template("index.html", category=categoria, resposta=resposta)





# ----------------- 5. Inicialização --------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



