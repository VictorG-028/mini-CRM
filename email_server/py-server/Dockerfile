FROM python:3.12-slim

# Solve pt-br locale.Error: unsupported locale setting
RUN apt-get update && apt-get install -y locales && \
    sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8
#######################################################

# Instala as dependências Python
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Expõe a porta em que a aplicação FastAPI será executada.
# O padrão para Uvicorn é 8000, mas o Railway geralmente usa a variável de ambiente PORT.
# Você pode definir um valor padrão aqui, mas o Railway irá sobrescrevê-lo.
EXPOSE 8000

# Comando para iniciar a aplicação quando o contêiner for executado.
# 'uvicorn' é o servidor ASGI para FastAPI.
# 'main:app' indica para Uvicorn que ele deve encontrar o objeto 'app' no módulo 'main.py'.
# '--host 0.0.0.0' faz com que o servidor escute em todas as interfaces de rede disponíveis.
# ${PORT:-8000} significa "use a variável PORT se existir, senão use 8000".
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
