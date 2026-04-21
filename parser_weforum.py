import asyncio
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode 
from bs4 import BeautifulSoup
from markdownify import markdownify

async def parser_weforum(url : str):
    browser_cfg = BrowserConfig(headless=True)

    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, 
        exclude_external_links=True,
        magic=True,
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        
        result = await crawler.arun(url)

        soup = BeautifulSoup(result.html, 'html.parser')
        
        content =  soup.find('article') #or soup.find('div') or soup.find('article') or soup.find('main') or soup.find('body') or soup.find('div')
        
        if content: 
            selettori_css = ('figcaption,.jw-wrapper,.jw-video, .jw-reset.report__meta,.tout-list-container,.article-story__header,.wef-pw060m,.wef-18lbtgg,.wef-19w4mes,.wef-odo13n,.wef-uo6d0e,.iframe-fallback__container,video,.wef-1s108tt,.wef-1brtsvq,.wef-1evq9jb')
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