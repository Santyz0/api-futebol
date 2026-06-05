import httpx
from bs4 import BeautifulSoup

def buscar_informacoes_clube(nome_clube: str):
    # Formatamos o nome para o padrão de links da Wikipedia (substituindo espaços por underlines)
    nome_formatado = nome_clube.strip().replace(" ", "_")
    url = f"https://pt.wikipedia.org/wiki/{nome_formatado}"
    
    headers = {
        "User-Agent": "BotDeEstudosFutebol_Sandro/1.0 (sandro@estudos.com)"
    }
    
    try:
        resposta = httpx.get(url, headers=headers, follow_redirects=True, timeout=10.0)
        if resposta.status_code != 200:
            return None
    except httpx.RequestError:
        return None

    sopa = BeautifulSoup(resposta.text, 'html.parser')

    titulo_elemento = sopa.find('h1', id='firstHeading')
    nome_real = titulo_elemento.text if titulo_elemento else nome_clube

    estadio = "Não encontrado"
    infobox = sopa.find('table', class_='infobox')
    
    if infobox:
        for linha in infobox.find_all('tr'):
            # 1. Buscamos todas as células da linha, não importa se é título (th) ou dado (td)
            celulas = linha.find_all(['th', 'td'])
            
            # 2. Uma linha válida para nós tem que ter pelo menos o rótulo e o valor (2 células)
            if len(celulas) >= 2:
                # 3. Limpamos os espaços e deixamos tudo minúsculo para não errar na comparação
                rotulo = celulas[0].get_text(strip=True).lower()
                
                # 4. Buscamos variações da palavra
                if any(termo in rotulo for termo in ['estádio', 'estadio', 'arena', 'mando']):
                    # 5. Pegamos o conteúdo da segunda célula (onde fica o nome do estádio)
                    # O separator=" " evita que palavras grudem se tiverem quebras de linha no HTML
                    texto_bruto = celulas[1].get_text(separator=" ", strip=True)
                    
                    # 6. Usamos o split('[') para ignorar as referências da Wikipedia (ex: "[1]")
                    estadio = texto_bruto.split('[')[0].strip()
                    break
    infobox = sopa.find('table', class_='infobox')
    
    if infobox:
        for linha in infobox.find_all('tr'):
            cabecalho = linha.find('th')
            # A Wikipedia pode usar "Estádio", "Arena" ou "Mando de campo"
            if cabecalho and any(termo in cabecalho.text for termo in ['Estádio', 'Arena', 'Mando']):
                celula_dado = linha.find('td')
                if celula_dado:
                    estadio = celula_dado.text.strip()
                    break

    return {
        "clube": nome_real,
        "estadio": estadio,
        "url_fonte": url
    }