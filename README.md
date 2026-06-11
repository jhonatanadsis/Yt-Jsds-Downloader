# YTDown

Downloader do YouTube com interface web local (Flask).

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Copie o arquivo de exemplo e edite com sua senha:

```bash
cp .env.example .env
```

Edite o `.env`:
```
YTDOWN_SENHA=sua_senha_aqui
SECRET_KEY=uma_chave_secreta_aleatoria
```

## Rodar

```bash
python app.py
```

Acesse: http://localhost:5000

## Expor via Ngrok (acesso externo)

```bash
ngrok http 5000
```
