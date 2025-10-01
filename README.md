# Aplicativo de Classificação de E-mails com IA
[🚀 Acessar o site](https://site-para-classificar-email-com-ia.onrender.com/)


Este projeto é um teste técnico que consiste em uma aplicação web simples para classificar e-mails em duas categorias: **Produtivo** ou **Improdutivo**, usando técnicas de Inteligência Artificial. O backend é feito em Python com Flask, e o frontend com HTML, CSS e JavaScript.

---

## 🗂️ Estrutura de Pastas

```
.
├── app.py
├── requirements.txt
├── templates/
│   └── (arquivos HTML do frontend)
├── static/
│   ├── css/
│   ├── js/
│   └── (outros recursos estáticos: imagens, etc.)
└── .gitignore
```

Breve explicação:

- **app.py** — ponto de entrada da aplicação Flask (rotas, lógica de classificação, etc.).  
- **requirements.txt** — dependências do projeto (bibliotecas Python necessárias).  
- **templates/** — contém os templates HTML usados pelo Flask para renderizar páginas.  
- **static/** — recursos estáticos (CSS, JavaScript, imagens).  
- **.gitignore** — define arquivos/pastas que não devem ser versionados (ex: `__pycache__`, arquivos temporários, etc.).

---

## 🛠️ Pré-requisitos

Para executar localmente, você vai precisar de:

- Python 3.7+ instalado  
- `pip` (gerenciador de pacotes Python)  
- (Opcional) um ambiente virtual (venv, virtualenv) para isolar dependências  

---

## 🚀 Como executar localmente

Siga os passos:

1. Clone o repositório  
   ```bash
   git clone https://github.com/jvsilva12600009/teste-tecnico-app-de-classificacao-email-usando-IA.git
   cd teste-tecnico-app-de-classificacao-email-usando-IA
   ```

2. (Opcional, mas recomendado) Crie e ative um ambiente virtual  
   ```bash
   python3 -m venv venv
   # no Linux/macOS:
   source venv/bin/activate
   # no Windows:
   venv\Scripts\activate
   ```

3. Instale as dependências  
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação  
   ```bash
   python app.py
   ```

5. Abra o navegador e vá para `http://127.0.0.1:5000/` (ou outro endereço exibido no terminal) para interagir com a aplicação.

---

## 📋 Uso / Fluxo da aplicação

- O usuário insere o conteúdo de um e-mail (assunto, corpo, etc.).  
- A aplicação envia esse texto para o backend, que processa e classifica via modelo de IA (ou heurística).  
- O resultado (“Produtivo” ou “Improdutivo”) é retornado e exibido ao usuário.  
- (Se aplicável) o backend pode armazenar logs, métricas, etc. — dependendo da implementação.

---

## 🔧 Dependências principais

O arquivo `requirements.txt` já lista as bibliotecas necessárias. Exemplos que provavelmente estarão lá:

- Flask  
- bibliotecas de NLP / machine learning (por exemplo: scikit-learn, nltk, etc., se usadas)  
- Outras utilitárias conforme a necessidade do projeto  

Certifique-se de rodar:

```bash
pip install -r requirements.txt
```

---


