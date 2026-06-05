from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import buscar_informacoes_clube

app = FastAPI(
    title="API de Estatísticas de Futebol",
    description="API assíncrona de web scraping para consulta de dados de clubes.",
    version="1.1.0"
)

# Definimos o nosso Modelo de Dados (Schema)
# Isso documenta a API e valida o tipo de cada campo automaticamente
class ClubeResponse(BaseModel):
    clube: str
    estadio: str
    url_fonte: str

# Rota dinâmica usando Path Parameters (igual ao /:nomeClube do Express)
# Indicamos que a resposta deve seguir rigorosamente o formato do ClubeResponse
@app.get("/clube/{nome_clube}", response_model=ClubeResponse)
def obter_dados_clube(nome_clube: str):
    print(f"Procurando dados do clube: {nome_clube}")
    
    dados = buscar_informacoes_clube(nome_clube)
    
    # Se o scraper não encontrar a página ou der erro, lançamos um erro HTTP 404
    if not dados:
        raise HTTPException(status_code=404, detail="Clube não encontrado na base de dados externa.")
        
    return dados