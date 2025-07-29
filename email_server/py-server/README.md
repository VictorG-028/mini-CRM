
# Preparar ambiente
```bash
cd email_server/py-server/
conda create -n crm python=3.12
conda activate crm
pip install -r requirements.txt
conda deactivate
```

# Ligar o servidor
```bash
cd email_server/py-server/
conda activate crm
uvicorn main:app --reload --host 0.0.0.0 --port 7999
```
