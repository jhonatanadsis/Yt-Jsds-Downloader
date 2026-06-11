from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pytubefix import YouTube
from pathlib import Path
from dotenv import load_dotenv
import threading
import uuid
import os
import webbrowser

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ytdown_secret_local_2024")

SENHA = os.environ.get("YTDOWN_SENHA", "jsds2024")

progresso = {}

def baixar_video(url, destino, task_id, modo):
    try:
        progresso[task_id] = 0

        def callback(stream, chunk, bytes_remaining):
            total = stream.filesize
            baixado = total - bytes_remaining
            pct = int((baixado / total) * 100)
            progresso[task_id] = pct

        yt = YouTube(url, on_progress_callback=callback)
        titulo = yt.title

        if modo == "audio":
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()

        destino_path = Path(destino)
        destino_path.mkdir(parents=True, exist_ok=True)

        arquivo = stream.download(output_path=destino_path)

        if modo == "audio":
            base = os.path.splitext(arquivo)[0]
            novo = base + ".mp3"
            os.rename(arquivo, novo)
            arquivo = novo

        progresso[task_id] = 100
        progresso[task_id + "_titulo"] = titulo
        progresso[task_id + "_arquivo"] = arquivo

    except Exception as e:
        progresso[task_id] = -1
        progresso[task_id + "_erro"] = str(e)


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        senha = request.form.get("senha", "")
        if senha == SENHA:
            session["autenticado"] = True
            return redirect(url_for("index"))
        else:
            erro = "Senha incorreta."
    return render_template("login.html", erro=erro)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    if not session.get("autenticado"):
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/iniciar", methods=["POST"])
def iniciar():
    if not session.get("autenticado"):
        return jsonify({"erro": "Não autorizado"}), 401

    data = request.json
    url = data.get("url", "").strip()
    destino = data.get("destino", "").strip()
    modo = data.get("modo", "video")

    if not url:
        return jsonify({"erro": "URL inválida"}), 400

    if not destino:
        destino = str(Path.home() / "Downloads")

    task_id = str(uuid.uuid4())
    t = threading.Thread(target=baixar_video, args=(url, destino, task_id, modo), name=task_id)
    t.start()

    return jsonify({"task_id": task_id})


@app.route("/status/<task_id>")
def status(task_id):
    if not session.get("autenticado"):
        return jsonify({"erro": "Não autorizado"}), 401

    pct = progresso.get(task_id, 0)
    titulo = progresso.get(task_id + "_titulo", "")
    erro = progresso.get(task_id + "_erro", "")
    return jsonify({"progresso": pct, "titulo": titulo, "erro": erro})


def abrir_navegador():
    webbrowser.open("http://localhost:5000")


if __name__ == "__main__":
    # Abre o navegador automaticamente após 1 segundo
    t = threading.Timer(1.0, abrir_navegador)
    t.start()
    app.run(debug=False, port=5000)
