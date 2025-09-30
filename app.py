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

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# ------------------ extrair o texto do pdf ou txt -------------------------
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

# --- função com o prompt para classificar o email em produto ou improdutivo --------------
def classificar_texto(texto):
    modelo = genai.GenerativeModel("gemini-2.5-flash")
    prompt_cat = f"""
    Classifique o texto abaixo como "Produtivo" (se for um email/texto de trabalho, pedido de informação, solicitação)
    ou "Improdutivo" (se for apenas cumprimento, agradecimento, felicitação, sem necessidade de ação).
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

# --- principal rota do Flask recebe o input do usuario e mostra o resultado ------
@app.route("/", methods=["GET", "POST"])
def index():
    categoria, resposta = None, None
    if request.method == "POST":
        texto_email = request.form.get("email_text")
        arquivo = request.files.get("file")
        if texto_email:
            categoria, resposta = classificar_texto(texto_email)
        elif arquivo and arquivo.filename != "":
            nome_arquivo = secure_filename(arquivo.filename)
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)
            arquivo.save(caminho)
            texto = extrair_texto(caminho)
            if texto.strip():
                categoria, resposta = classificar_texto(texto)
            else:
                categoria, resposta = "Erro", "Não foi possível extrair texto do arquivo."
    return render_template("index.html", category=categoria, resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
