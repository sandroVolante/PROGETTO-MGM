import asyncio
import re  # <--- AGGIUNGI QUESTO IMPORT
from crawl4ai import AsyncWebCrawler, BrowserConfig
from bs4 import BeautifulSoup
from markdownify import markdownify


async def parser_wiki(url : str):
    browser_cfg = BrowserConfig(headless=True, text_mode=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url)
        soup = BeautifulSoup(result.html, 'html.parser')
        content = soup.find(id="content")
        
        if content: 
            for header_id in ['Bibliography', 'References', 'External_links']:
                header = content.find('span', id=header_id)
                if header:
                    parent = header.parent 
                    for sibling in parent.find_next_siblings():
                        sibling.decompose()
                    parent.decompose() 
            for header_id in ['References', 'Bibliography', 'External_links', 'Further_reading']:
                header = content.find(id=header_id)
                if header:
                    target = header.parent if header.name not in ['h2', 'h3', 'div'] else header
                    for elemento_successivo in target.find_all_next():
                        elemento_successivo.decompose()
                        

                    target.decompose() 
            elementi_da_rimuovere = content.select('.infobox, .sidebar, #siteNotice, .vector-dropdown, #vector-variant-dropdown,nav,.mw-editsection,figcaption,.mw-logo-wordmark,hr,.hatnote-content,.mw-page-title-main,#mwog,#catlinks,#mwoQ,#mwkQ,#mwiQ,#External_links,#References,.thumbcaption,.mw-heading ,.mw-heading3,.mw-references-wrap, .mw-references-columns,.mw-heading, .mw-heading2,.reference,.navbox,.bibliography')
            for elemento in elementi_da_rimuovere:
                elemento.decompose()   
            testo_pulito = markdownify(str(content), strip=['a', 'img']) 
            
            testo_pulito = testo_pulito.replace('*', '')
            
            testo_pulito = re.sub(r'^\s*[#,-,=]{2,}\s*$', '', testo_pulito, flags=re.MULTILINE)

            return testo_pulito