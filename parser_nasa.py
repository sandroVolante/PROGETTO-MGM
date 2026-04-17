'''import asyncio
import re  # <--- AGGIUNGI QUESTO IMPORT
from crawl4ai import AsyncWebCrawler, BrowserConfig
from bs4 import BeautifulSoup
from markdownify import markdownify

def pulisci_e_tokenizza(testo):
    # Rimuove punteggiatura e trasforma in minuscolo per un confronto equo
    testo = re.sub(r'[^\w\s]', '', testo.lower())
    return testo.split()

def token_level_eval(testo_gs, testo_pars):
    token_estratti = set()
    token_gs = set()
    for parolaGs in testo_gs:
        token_gs.add(parolaGs)
    for parolaPs in testo_pars:
        token_estratti.add(parolaPs)
    precision = len(token_estratti.intersection(token_gs))/ len(token_estratti)
    recall = len(token_estratti.intersection(token_gs)) / len(token_gs)
    f1 = 2*precision*recall/(precision+recall)
    print(f"precision : {precision}, recall: {recall}, f1: {f1}")



async def main():
    testo_gs = """The primary objective of Apollo 11 was to complete a national goal set by President John F. Kennedy on May 25, 1961: perform a crewed lunar landing and return to Earth.

Mission Type

Lunar Landing
astronauts

Neil Armstrong, Buzz Aldrin, Michael Collins
Launch

July 16, 1969
SPLASHDOWN

July 24, 1969"""
    browser_cfg = BrowserConfig(headless=True, text_mode=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url="https://www.nasa.gov/mission/apollo-11/")
        soup = BeautifulSoup(result.html, 'html.parser')
        content = soup.find('main') or soup.find('article') or soup.find('body')
        
        if content: 
            for header_id in ['Discover More Topics From NASA','Latest News','Key Source','NASA+']:
                header = content.find('span', id=header_id)
                if header:
                    parent = header.parent 
                    for sibling in parent.find_next_siblings():
                        sibling.decompose()
                    parent.decompose() 
            for header_id in ['Discover More Topics From NASA','Latest News','Key Source','NASA+']:
                header = content.find(id=header_id)
                if header:
                    target = header.parent if header.name not in ['h2', 'h3', 'div'] else header
                    for elemento_successivo in target.find_all_next():
                        elemento_successivo.decompose()
                        

                    target.decompose()
            elementi_da_rimuovere = content.select('.hds-secondary-nav-mobile-button,button,.hds-gallery-preview,.wp-block-nasa-blocks-featured-link-list,.hds-featured-link-list,.wp-block-nasa-blocks-content-lists,.page-numbers,.dots,.entry-footer,.wp-block-nasa-blocks-news-manual,.wp-block-nasa-blocks-meet-the,.wp-block-nasa-blocks-callout,.hds-mission-header,.hds-secondary-navigation,.button-primary,.hds-featured-story,.hds-credits,.hds-card-grid,.wp-block-nasa-blocks-listicle,.hds-card-inner,.section-heading-sm,.wp-block-nasa-blocks-article-intro,.article-meta-item,.hds-caption-text,.wp-block-nasa-blocks-news-automated,.wp-block-nasa-blocks-topic-cards')
            for elemento in elementi_da_rimuovere:
                elemento.decompose()   
            testo_pulito = markdownify(str(content), strip=['a', 'img']) 
            
            testo_pulito = testo_pulito.replace('*', '')
            
            testo_pulito = re.sub(r'^\s*[#,-,=,_]{2,}\s*$', '', testo_pulito, flags=re.MULTILINE)
            token_gs = pulisci_e_tokenizza(testo_gs)
            token_pars = pulisci_e_tokenizza(testo_pulito)
            #token_level_eval(token_gs,token_pars)
            print(testo_pulito)

if __name__ == "__main__":
    asyncio.run(main())'''
import asyncio
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode # <--- AGGIUNTI IMPORT
from bs4 import BeautifulSoup
from markdownify import markdownify

def pulisci_e_tokenizza(testo):
    # Rimuove punteggiatura e trasforma in minuscolo per un confronto equo
    testo = re.sub(r'[^\w\s]', '', testo.lower())
    return testo.split()

def token_level_eval(testo_gs, testo_pars):
    token_estratti = set(testo_pars)
    token_gs = set(testo_gs)
    
    if len(token_estratti) == 0 or len(token_gs) == 0:
        print("Uno dei due testi è vuoto, impossibile calcolare f1.")
        return

    precision = len(token_estratti.intersection(token_gs)) / len(token_estratti)
    recall = len(token_estratti.intersection(token_gs)) / len(token_gs)
    
    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0
        
    print(f"precision: {precision:.4f}, recall: {recall:.4f}, f1: {f1:.4f}")

async def main():
    testo_gs = """In Brief:
As the ocean warms and land ice melts, ocean circulation — the movement of heat around the planet by currents — could be impacted. Research with NASA satellites and other data is currently underway to learn more.

Dynamic and powerful, the ocean plays a vital role in Earth’s climate. It helps regulate Earth’s temperature, absorbs carbon dioxide (CO2) from the atmosphere, and fuels the water cycle. One of the most important functions of the ocean is to move heat around the planet via currents.
Winds and Earth’s rotation create large-scale surface currents in the ocean. Warm, fast currents along the western edges of ocean basins move heat from the equator toward the North and South Poles. One such current is the Gulf Stream, which travels along the eastern coast of North America as it carries warm waters from the tropics toward Europe. This warm water, and the heat it releases into the atmosphere, is the primary reason Europe experiences a more temperate climate than the northeastern U.S. and Canada. For example, compare the climates of New York City and Madrid, Spain, which are both about the same distance north of the equator.
Differences in density drive slow-moving ocean currents in the deep ocean. Density is an object’s mass (how much matter it has) per unit of volume (how much space it takes up). Both temperature and saltiness (salinity) affect the density of water. Cold water is denser than warm water, and salty water is denser than fresh water. Thus, deep currents are typically made of cold and salty water that sank from the surface.
One location where surface water sinks into the deep ocean is in the North Atlantic. When water evaporates and gives up some heat to the air, the sea gets colder and a little saltier. Plus, when sea ice forms, it freezes the surface water leaving behind salt, which makes the remaining seawater saltier. Once this colder, saltier water becomes dense enough, it sinks to the deep ocean. Warmer, less dense water from the Gulf Stream rushes in to replace the water that sinks. This motion helps power a global “conveyor belt” of ocean currents – known as thermohaline circulation – that moves heat around Earth. Scientists measure the flow of Atlantic waters north and south, at the surface and in the deep, to assess the strength of this Atlantic Meridional Ocean Circulation (AMOC).
The Atlantic Ocean's currents play an especially important role in our global climate. The movement of water north and south throughout the Atlantic might be weakening due to climate change, which could become a problem. To help understand why, let’s explore what drives large-scale ocean circulation.
When and how much the AMOC will weaken is an area of ongoing research. Satellites such as the Gravity Recovery and Climate Experiment (GRACE), GRACE-FO, and ocean height-measuring altimeters can observe ocean features related to the AMOC — complementing measurements from ocean buoys and ships.
As the concentration of carbon dioxide rises in the atmosphere from human actions, global air and ocean temperatures heat up. Warmer water is less dense, and thus harder to sink. At the same time, Greenland’s ice sheet is melting due to warming air and ocean temperatures, and the melted ice is adding fresh water into the North Atlantic. This change reduces the water’s saltiness, making it less dense and harder to sink.
When and how much the AMOC will weaken is an area of ongoing research. Satellites such as the Gravity Recovery and Climate Experiment (GRACE), GRACE-FO, and ocean height-measuring altimeters can observe ocean features related to the AMOC — complementing measurements from ocean buoys and ships.
If enough water stops sinking, then the AMOC will weaken. Depending on how much the AMOC weakens, it can change regional weather patterns, such as rainfall, and affect where and how well crops can grow. According to the latest report from the International Panel on Climate Change (IPCC) — which includes research from hundreds of scientists — the AMOC is “very likely to weaken over the 21st century” due to climate change.

Scientists using temperature and sea level records have inferred the AMOC’s strength over the past century, and the evidence suggests that it might have already weakened. However, direct measurements over the past 30 years have not yet confirmed such a decline.
Current projections from the IPCC show that the AMOC is unlikely to stop, or collapse, before the year 2100. However, “if such a collapse were to occur," the IPCC says, "it would very likely cause abrupt shifts in regional weather patterns and the water cycle.” These could include “a southward shift in the tropical rain belt, weakening of the African and Asian monsoons, strengthening of Southern Hemisphere monsoons, and drying in Europe,” impacts that would greatly alter food production worldwide.

As more data are gathered and analyzed, scientists will be able to better predict current changes and impacts of those changes in the future.
"""

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
        result = await crawler.arun(url="https://science.nasa.gov/earth/earth-atmosphere/slowdown-of-the-motion-of-the-ocean/", config=run_cfg)
        
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
            token_gs = pulisci_e_tokenizza(testo_gs)
            token_pars = pulisci_e_tokenizza(testo_pulito)
            
            token_level_eval(token_gs, token_pars)
            
            print("\n--- TESTO ESTRATTO ---\n")
            print(testo_pulito)
        else:
            print("Errore: impossibile trovare il blocco principale.")

if __name__ == "__main__":
    asyncio.run(main())