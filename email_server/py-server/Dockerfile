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

EXPOSE 7999

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7999"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:7999"]
