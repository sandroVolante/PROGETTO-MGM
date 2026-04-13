import asyncio
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
    testo_gs = """Guthrum, che si fece battezzare col nome di Aethelstan (Danimarca, 835 – Anglia Orientale, 890), fu re vichingo del Danelaw e dell'Anglia orientale nel IX secolo.

Biografia
Lo jarl giunse a capo dell'esercito chiamato "l'armata d'estate", il quale si unì alla Grande armata guidata dai Ragnarsson. Non si sa come Guthrum sia riuscito a consolidare il suo dominio sugli altri capi danesi del Danelaw (nome del territorio dominato da questo popolo in Inghilterra), ma a partire dall'874 egli fu in grado di muovere guerra al Wessex, soprattutto nel periodo di regno di Alfredo il Grande. Dall'876 conquistò diverse parti della Mercia e della Northumbria, per poi iniziare a premere di nuovo contro il Wessex. Il primo scontro con Alfredo avvenne poco fuori dai confini del Galles.

Vicino al Galles, Guthrum fece navigare il suo esercito intorno al porto di Poole, mentre un'altra armata vichinga invadeva la zona tra i fiumi Trent e Frome, che era sotto il controllo di Alfredo. Secondo lo storico Asser, la prima battaglia tra Guthrum e Alfredo fu vinta dal danese. Fu stipulata una pace, che venne però rotta a partire dall'877, quando l'esercito di Guthrum compì nuove scorrerie nel Wessex, costringendo Alfredo a ingaggiare altre scaramucce, sempre però a lui sfavorevoli.

Nell'878, però, Guthrum fu sconfitto da Alfredo nella battaglia di Ethandun: il suo esercito fu costretto a ritirarsi nell'accampamento, dove fu assediato dal sovrano del Wessex. Secondo la Cronaca anglosassone, l'esercito di Guthrum giunse a un accordo di pace conosciuto come trattato di Wedmore. Alfredo ricevette ostaggi, il giuramento che gli invasori avrebbero lasciato il suo regno e la promessa che Guthrum si sarebbe fatto battezzare. Tre settimane dopo il re danese si recò dal vincitore e accettò il sacramento.

Questa conversione al cristianesimo ebbe risvolti sia politici sia religiosi, poiché gli diede una patente di legittimità, rassicurando così i suoi nuovi sudditi cristiani.

Morì 11 anni dopo nell'890, si presume di vecchiaia.

Cultura di massa
È l'antagonista principale della Ballata del Cavallo Bianco di Gilbert Keith Chesterton. È rappresentato come un uomo colto e di profonda intelligenza, che esprime il punto di vista dell'ateismo disilluso e affronta la vita e la morte consapevole della vanità di tutte le cose.
Compare nel videogioco Assassin's Creed: Valhalla come alleato.
Nell'ultimo episodio di Vikings si scopre che Hvitserk si basa su due dei figli di Ragnar (Hvítserkr ed Halfdan Ragnarsson) e su Guthrum in quanto, dopo la morte di Ivar ad Ethandun, viene battezzato e (diventando presumibilmente re dell'Anglia Orientale) prende il nome di Athelstan."""
    browser_cfg = BrowserConfig(headless=True, text_mode=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url="https://en.wikipedia.org/wiki/Guthrum")
        soup = BeautifulSoup(result.html, 'html.parser')
        content = soup.find(id="content")
        
        if content: 
            # Rimuove le sezioni Bibliography, References e External Links e tutto il loro contenuto
            for header_id in ['Bibliography', 'References', 'External_links']:
                header = content.find('span', id=header_id)
                if header:
                    parent = header.parent # Trova l'h2 o h3
                    # Rimuove tutti i fratelli successivi (liste, paragrafi, ecc.) finché non finisce il contenitore
                    for sibling in parent.find_next_siblings():
                        sibling.decompose()
                    parent.decompose() # Rimuove l'intestazione stessa
            for header_id in ['References', 'Bibliography', 'External_links', 'Further_reading']:
                # Cerca l'ID su QUALSIASI tag (non solo span)
                header = content.find(id=header_id)
                if header:
                    # Risale al contenitore principale del titolo (h2, div, ecc.)
                    target = header.parent if header.name not in ['h2', 'h3', 'div'] else header
                    
                    # Elimina TUTTI i tag HTML che esistono nel documento dopo questo titolo
                    for elemento_successivo in target.find_all_next():
                        elemento_successivo.decompose()
                        
                    # Elimina il titolo stesso
                    target.decompose() 
            elementi_da_rimuovere = content.select('.infobox, .sidebar, #siteNotice, .vector-dropdown, #vector-variant-dropdown,nav,.mw-editsection,figcaption,.mw-logo-wordmark,hr,.hatnote-content,.mw-page-title-main,#mwog,#catlinks,#mwoQ,#mwkQ,#mwiQ,#External_links,#References,.thumbcaption,.mw-heading ,.mw-heading3,.mw-references-wrap, .mw-references-columns,.mw-heading, .mw-heading2,.reference,.navbox,.bibliography')
            for elemento in elementi_da_rimuovere:
                elemento.decompose()   
            testo_pulito = markdownify(str(content), strip=['a', 'img']) 
            
            # --- AGGIUNGI QUESTE TRE RIGHE ---
            
            # 1. Elimina tutti gli asterischi (usati per grassetto e corsivo)
            testo_pulito = testo_pulito.replace('*', '')
            
            testo_pulito = re.sub(r'^\s*[#,-,=]{2,}\s*$', '', testo_pulito, flags=re.MULTILINE)
            #testo_pulito = re.split(r'(?i)bibliography|external links', testo_pulito)[0]
            # ---------------------------------
            token_gs = pulisci_e_tokenizza(testo_gs)
            token_pars = pulisci_e_tokenizza(testo_pulito)
            #token_level_eval(token_gs,token_pars)
            print(testo_pulito)

if __name__ == "__main__":
    asyncio.run(main())