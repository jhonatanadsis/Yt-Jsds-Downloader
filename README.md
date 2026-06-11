# YTDown

Downloader do YouTube com interface web — abre direto no navegador.

## Opção 1 — Rodar via Python

```bash
pip install -r requirements.txt
python app.py
```

Acesse: http://localhost:5000

---

## Opção 2 — Gerar .exe (recomendado)

Rode o script abaixo uma única vez na sua máquina Windows:

```bash
build.bat
```

O executável será gerado em `dist/YTDown.exe`.  
Basta clicar duas vezes — o navegador abre automaticamente.

---

## Senha padrão

`jsds2024`

Para trocar, edite o `.env`:
```
YTDOWN_SENHA=sua_senha_aqui
SECRET_KEY=chave_aleatoria
```

> O `.env` não é incluído no repositório por segurança.
