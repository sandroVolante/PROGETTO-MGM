import asyncio
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode 
from bs4 import BeautifulSoup
from markdownify import markdownify



async def parser_espn(url : str):
        # 1. MODIFICA CRITICA: headless=False aprirà il browser così possiamo VEDERE cosa succede
    browser_cfg = BrowserConfig(headless=True)

    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, 
        exclude_external_links=True,
        magic=True,
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url)
        soup = BeautifulSoup(result.html, 'html.parser')
        
        content = soup.find('div', class_='article-body') or soup.find('article') or soup.find('main') or soup.find('body')
        
        if content: 
            selettori_css = ('aside,.content-reactions,.single-author,.article-meta, .contentItem__contentWrapper')
            elementi_da_rimuovere = content.select(selettori_css)
            for elemento in elementi_da_rimuovere:
                elemento.decompose()   
                
            testo_pulito = markdownify(str(content), strip=['a', 'img', 'script', 'style']) 
            
            testo_pulito = testo_pulito.replace('*', '')
            testo_pulito = re.sub(r'^\s*[#\-\=_]{2,}\s*$', '', testo_pulito, flags=re.MULTILINE)
            testo_pulito = re.sub(r'^\s*(start|end)\s*$', '', testo_pulito, flags=re.MULTILINE | re.IGNORECASE)
            testo_pulito = re.sub(r'\n\s*\n', '\n\n', testo_pulito).strip()
            
            return testo_pulito
           
        else:
            print("Errore: impossibile trovare il blocco principale.")
