from pydantic import BaseModel
from crawl4ai import BrowserConfig, CrawlerRunConfig, AsyncWebCrawler, CacheMode
from typing import List
from parser_espn import parser_espn
from parser_nasa import parser_nasa
from parser_weforum import parser_weforum
from parser_wikipedia import parser_wiki
import re 
import os
import json
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException

def match_regex(url):

    domain = urlparse(url).netloc
    match = re.search(r'(?:www\.)?([\w\.-]+)', domain)
    if match:
        return match.group(1)
    return domain

def pulisci_e_tokenizza(testo):
    # Rimuove punteggiatura e trasforma in minuscolo per un confronto equo
    testo = re.sub(r'[^\w\s]', '', testo.lower())
    return testo.split()

def token_level_eval(testo_gs, testo_pars):
    res = []
    token_estratti = set()
    token_gs = set()
    if len(token_estratti) == 0 or len(token_gs) == 0:
        return (0.0, 0.0, 0.0)
    for parolaGs in testo_gs:
        token_gs.add(parolaGs)
    for parolaPs in testo_pars:
        token_estratti.add(parolaPs)
    precision = len(token_estratti.intersection(token_gs))/ len(token_estratti)
    recall = len(token_estratti.intersection(token_gs)) / len(token_gs)
    f1 = 2*precision*recall/(precision+recall)
    res.append(precision)
    res.append(recall)
    res.append(f1)
    return res

import re

def text_to_single_line(text: str) -> str:
    """
    Rimuove i ritorni a capo, le tabulazioni e gli spazi multipli
    restituendo il testo su un'unica riga.
    """
    if not text:
        return ""
    
    # Sostituisce ogni sequenza di whitespace (spazi, tab, \n, \r) con un singolo spazio
    single_line = re.sub(r'\s+', ' ', text)
    
    # Rimuove eventuali spazi vuoti all'inizio o alla fine
    return single_line.strip()

app = FastAPI()
accepted_domains = ["wikipedia.org", "nasa.gov", "espn.com", "weforum.org"]
class output_parse(BaseModel):
    url : str
    domain : str
    title : str
    html_text : str
    parsed_text : str

class output_gs(BaseModel):
    url : str
    domain : str
    title : str
    html_text : str
    gold_text : str

class EvalRequest(BaseModel):
    parsed_text : str
    gold_text : str


class EvalResponse(BaseModel):
    precision : float
    recall : float
    f1 : float


@app.get("/parse", response_model = output_parse)
async def get_parse(url : str):
    domain_finded=match_regex(url)
    if domain_finded not in accepted_domains:
        raise HTTPException(status_code=400, detail="Dominio non supportato")
    
    # 2. Configura Crawl4AI come da Slide 12
    browser_cfg = BrowserConfig(headless=True) # Headless=True così non apre la finestra visibile
    crawler_cfg = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
    
    # 3. Scarica la pagina in modo asincrono
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url=url, config=crawler_cfg)
        
        # Se la pagina non esiste o è bloccata, restituisci errore
        if not result.success:
            raise HTTPException(status_code=400, detail=f"Errore nel download della pagina: {result.error_message}")
        
        # Ecco il tuo HTML grezzo!
        html_text_finded = text_to_single_line(result.html)
        # 4. Estrai il titolo dall'HTML usando le Regex
        match_title = re.search(r'<title>(.*?)</title>', html_text_finded, re.IGNORECASE)
        title_finded = match_title.group(1).strip() if match_title else "Titolo non trovato"

    if url is None:
        raise HTTPException(status_code=404, detail="Url inesistente")
    if domain_finded == "nasa.gov":
        testo_parsed_wip = parser_nasa(url)
    elif domain_finded == "espn.com":
        testo_parsed_wip = parser_espn(url)
    elif domain_finded == "wikipedia.org":
        testo_parsed_wip = parser_wiki(url)
    elif domain_finded =="weforum.org":
        testo_parsed_wip = parser_weforum(url)
    else:
        raise HTTPException(status_code=404, detail="Url non trattato")

    testo_parsed = text_to_single_line(testo_parsed_wip)
    return output_parse(url=url, domain=domain_finded, title=title_finded,html_text=html_text_finded, parsed_text=testo_parsed)

@app.get("/domains")
def get_domains():
    return {"domains": accepted_domains}

@app.get("/gold_standard", response_model=output_gs)
def get_gold_standard(url: str):
    
    directory = "gs_data"
    
    if not os.path.exists(directory):
        raise HTTPException(status_code=500, detail="Cartella gs_data non trovata")

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                data = json.load(f) 

                for entry in data:
                    if entry["url"] == url:
                        return entry 
    
    raise HTTPException(status_code=404, detail="URL non trovato nel Gold Standard")

@app.get("/full_gold_standard")
def get_full_gold_standard(domain : str):
    gs_list=[]
    directory = "gs_data"
    
    if not os.path.exists(directory):
        raise HTTPException(status_code=500, detail="Cartella gs_data non trovata")

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                data = json.load(f) 

                for entry in data:
                    if entry["domain"] == domain:
                        gs_list.append(entry) 

    return {"gold_standard": gs_list}
    
@app.post("/evaluate", response_model = EvalResponse)
def evaluate(req : EvalRequest):
    parsed_text = req.parsed_text
    gold_text = req.gold_text
    token_estratti = pulisci_e_tokenizza(parsed_text)
    token_gs = pulisci_e_tokenizza(gold_text)
    res = token_level_eval(token_gs, token_estratti)
    return EvalResponse(precision = res[0], recall = res[1], f1 = res[2])

@app.get("/full_gs_eval")
def get_full_gs_eval(domain: str):
    # 1. Verifica dominio
    if domain not in accepted_domains:
        raise HTTPException(status_code=400, detail="Dominio non supportato")
    
    # 2. Carica i dati del Gold Standard per questo dominio
    # Assumiamo che tu abbia file chiamati "wikipedia.org_gs.json", ecc.
    gs_filepath = f"gs_data/{domain}_gs.json"
    
    if not os.path.exists(gs_filepath):
        raise HTTPException(status_code=404, detail="File GS non trovato per questo dominio")
        
    with open(gs_filepath, "r", encoding="utf-8") as f:
        gs_data = json.load(f)
        
    if len(gs_data) == 0:
        raise HTTPException(status_code=400, detail="Il Gold Standard è vuoto")

    # 3. Variabili per accumulare i punteggi
    total_precision = 0.0
    total_recall = 0.0
    total_f1 = 0.0
    conteggio = len(gs_data)

    # 4. Esegui il parsing e valuta ogni singola pagina
    for entry in gs_data:
        # A. Prendi l'HTML grezzo dal GS o riscarica l'URL
        html_da_parsare = entry["html_text"]
        testo_gold = entry["gold_text"]
        
        # B. ESEGUI IL PARSER (Richiama la tua logica di parsing)
        # NOTA: Qui dovrai chiamare il tuo parser_wikipedia, parser_nasa, ecc.
        # passando l'HTML grezzo o l'URL. 
        if domain == "nasa.gov":
            testo_parsato = parser_nasa(html_da_parsare) # Assumendo accetti l'HTML
        elif domain == "wikipedia.org":
            testo_parsato = parser_wiki(html_da_parsare)
        elif domain == "weforum.org":
            testo_parsato = parser_weforum(html_da_parsare)
        elif domain == "espn.com":
            testo_parsato = parser_espn(html_da_parsare)
        else:
            testo_parsato = ""

        token_estratti = pulisci_e_tokenizza(testo_parsato)
        token_gs = pulisci_e_tokenizza(testo_gold)   
        # C. Calcola le metriche per questa specifica pagina
        res = token_level_eval(token_gs, token_estratti)
        p = res[0]
        r = res[1]
        f1 = res[2]
        
        # D. Somma i risultati
        total_precision += p
        total_recall += r
        total_f1 += f1
        
    # 5. Calcola la media finale e arrotonda (es. 2 o 4 decimali)
    avg_precision = round(total_precision / conteggio, 4)
    avg_recall = round(total_recall / conteggio, 4)
    avg_f1 = round(total_f1 / conteggio, 4)
    
    # 6. Restituisci il formato esatto richiesto dalla Slide 30
    return {
        "token_level_eval": {
            "precision": avg_precision,
            "recall": avg_recall,
            "f1": avg_f1
        }
    }