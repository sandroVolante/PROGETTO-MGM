import asyncio
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode # <--- AGGIUNTI IMPORT
from bs4 import BeautifulSoup
from markdownify import markdownify


async def parser_nasa(url : str):

    # 1. Configurazione del Browser (Rimane invariata)
    browser_cfg = BrowserConfig(headless=True, text_mode=True, light_mode=True)

    # 2. NUOVO: Configurazione specifica per questo scraping
    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, # Ignora la cache locale, utile durante lo sviluppo
        # Qui potresti aggiungere altri parametri utili in futuro, come:
        # wait_for="css:.alghe-classe",
        exclude_external_links=True
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # 3. NUOVO: Passiamo run_cfg tramite il parametro 'config'
        result = await crawler.arun(url)
        
        soup = BeautifulSoup(result.html, 'html.parser')
        content = soup.find('main') or soup.find('article') or soup.find('body')
        
        if content: 
            # 1. CERCA PER TESTO INVECE CHE PER ID
            testi_da_tagliare = ['Discover More Topics From NASA', 'Latest News', 'Key Source','Biography']
            
            for testo_intestazione in testi_da_tagliare:
                nodo_testo = content.find(string=re.compile(testo_intestazione, re.IGNORECASE))
                if nodo_testo:
                    target = nodo_testo.parent
                    for elemento_successivo in target.find_all_next():
                        elemento_successivo.decompose()
                    target.decompose()
                    
            # 2. RIMOZIONE ELEMENTI SPORCHI E TESTI NASCOSTI
            selettori_css = (
                '.sr-only, .screen-reader-text, .visually-hidden, ' 
                '.hds-secondary-nav-mobile-button, button, .hds-gallery-preview, '
                '.wp-block-nasa-blocks-featured-link-list, .hds-featured-link-list, '
                '.wp-block-nasa-blocks-content-lists, .page-numbers, .dots, .entry-footer, '
                '.wp-block-nasa-blocks-news-manual, .wp-block-nasa-blocks-meet-the, '
                '.wp-block-nasa-blocks-callout, .hds-secondary-navigation, '
                '.button-primary, .hds-featured-story, .hds-credits, .hds-card-grid, '
                '.hds-card-inner, .section-heading-sm, '
                '.wp-block-nasa-blocks-article-intro, .article-meta-item, .hds-caption-text, '
                '.wp-block-nasa-blocks-news-automated, .wp-block-nasa-blocks-topic-cards,'
                '.wp-block-nasa-blocks-featured-link'
            )
            elementi_da_rimuovere = content.select(selettori_css)
            for elemento in elementi_da_rimuovere:
                elemento.decompose()   
                
            # 3. CONVERSIONE IN MARKDOWN
            testo_pulito = markdownify(str(content), strip=['a', 'img']) 
            
            # Pulizia stringhe extra
            testo_pulito = testo_pulito.replace('*', '')
            testo_pulito = re.sub(r'^\s*[#\-\=_]{2,}\s*$', '', testo_pulito, flags=re.MULTILINE)
            
            # NUOVA PULIZIA: Rimuove righe "start" o "end"
            testo_pulito = re.sub(r'^\s*(start|end)\s*$', '', testo_pulito, flags=re.MULTILINE | re.IGNORECASE)
            
            # Rimuovi righe vuote in eccesso per una stampa pulita
            testo_pulito = re.sub(r'\n\s*\n', '\n\n', testo_pulito).strip()
            
            # 4. VALUTAZIONE
            return testo_pulito
        else:
            print("Errore: impossibile trovare il blocco principale.")
