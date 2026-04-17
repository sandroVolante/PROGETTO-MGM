import asyncio
import re
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode 
from bs4 import BeautifulSoup
from markdownify import markdownify

def pulisci_e_tokenizza(testo):
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
    testo_gs = ''' The fashion industry produces a lot of waste, but physical AI can significantly reduce this.
Physical AI systems offer fast, precise, on-demand production, making manufacturers more adaptable, while reducing waste and unsold stock.
With fashion's waste crisis accelerating, physical AI is creating a viable path forward, moving beyond the overproduction model that has defined the industry for decades.
The fashion industry produces 92 million tonnes of waste annually, not as a side effect, but as a result of how production systems are designed.

This is beginning to change. On factory floors across the world, a new class of AI is emerging that doesn’t just produce text or images, it actually interacts with materials, senses its environment and adapts in real time. Physical AI is starting to crack problems that have plagued textile manufacturing for decades. This is a different kind of AI innovation: sophisticated manufacturing automation that shortens production lead times, enables faster iteration, reduces overstock and cuts waste at source

Why is traditional automation not enough for the fashion industry?
While consumer preferences shift in days, traditional production cycles take months from design to store. This mismatch forces brands to over produce because missing a trend costs more than excess inventory in the short term. These unwanted clothes are then discarded from warehouses and often sent to landfills as manufacturers fail to respond fast enough to actual demand.

The fashion industry produced up to an estimated 5 billion excess stock items in 2023, worth up to $140 billion in lost sales. But overproduction is only part of the problem. Fabric cutting also generates waste, creating offcuts with no practical use, and defects discovered late in production mean entire batches become scrap.

The textile industry has turned to automation to reduce costs and boost efficiency, but traditional systems hit a fundamental barrier: they can't handle fabric. Most automated machines can perform single, repetitive tasks – like cutting along predetermined lines or moving rigid materials – but they still require human operators to manipulate, align and position fabric. This 'cobot' approach increases worker output without significantly improving production speed or reducing waste generation, as the machines are not sophisticated enough to handle soft, deformable materials that behave differently depending on fabric type, weave and environmental conditions.

Through sophisticated cameras and sensors, physical AI systems work on a feedback loop – sense, think, act, learn – offering a path to fast, precise, on-demand production, making manufacturers more adaptable, while reducing waste and unsold stock. This means it can achieve:

Real-time defect detection: Traditional quality control happens after garment assembly and all the material, labour and energy invested in defective items turns to waste. Physical AI can spot defects the instant they occur, catching problems early to prevent waste from compounding through the production stages.
Material optimization: Standard garment patterns leave substantial fabric offcuts with no practical use. Physical AI systems can analyze fabric properties dynamically and optimize cutting patterns in real time to reduce wasted fabric. Take the case of Unspun, a start-up company backed by The Mills Fabrica, it uses 3D weaving to produce tubular, contour-woven fabrics that match the final garment's shape. Instead of cutting flat fabric into pattern pieces and sewing them together, it creates fabric already formed to the product's contours to avoid cutting waste and making better-fitting garments.
More responsive production: By reducing waste and defects across the production process, physical AI makes smaller, more frequent production runs economically viable, helping brands reduce speculative orders and produce close to actual demand. Brands can produce smaller batches aligned with actual trends to directly address the overproduction problem that sends millions of unsold garments to landfills.
Lower emissions and costs: By making it economically viable to manufacture closer to end markets, physical AI dramatically reduces shipping distances. This cuts transport emissions, shortens logistics time and reduces freight and tariff-related expenses.
What does it take to scale physical AI?
While the benefits are immense, making physical AI systems operate reliably for thousands of production hours across different fabric types in real factory conditions is another challenge entirely. Unlike generative AI, which can scale digitally, physical AI needs real testing environments, access to factory floors for data collection and partnerships with manufacturers willing to test robotic systems in their production lines.

This means progress depends on a cross-sector collective effort, with entrepreneurs, manufacturers and investors working together to test, refine and validate solutions in real production conditions.

At The Mills Fabrica, we invest in techstyle and agrifood startups across the world and we evaluate solutions through a business/technology-impact lens. The most promising investments combine three elements: strong technical foundations built on deep domain expertise, proven ability to integrate with real factory conditions and measurable environmental and commercial returns. Task-specific applications, such as automated cutting, fabric handling and defect detection, tend to outperform generic platforms and applications.

How is Asia leading the shift to physical AI?
The application of physical AI across the textile industry is pertinent as this sector faces multiple pressures, including: unsustainable levels of waste and overproduction; supply chain issues, forcing new sourcing strategies; and rising consumer demand to reduce environmental impact. Asia manufactures most of the world's textiles and manufacturers here are navigating extraordinary turbulence. Brands have had to increasingly source and manufacture from new geographies in light of evolving trade policies and tariffs, squeezing margins and transferring costs to the end consumer. Uncertain political environments continue to demand supply chain resilience from manufacturers, who are increasingly diversifying their sourcing capabilities.

Physical AI offers precisely what these times need: speed, flexibility, quality assurance and verifiable sustainability. As global brands seek manufacturing partners who can deliver smaller batches faster, closer to home, with lower environmental impact, it will continue to demonstrate its clear ROI through reduced waste, improved quality and faster throughput, systematically embedding efficiency gains directly into production processes.

Physical AI systems are already operating in factories. Sustained success requires understanding not just the technical aspects, but the realities of Asian manufacturing, which means integrating with legacy infrastructure. The manufacturers who will lead this shift are working with innovation platforms and technology developers to iterate systems that work in real conditions, not just controlled labs. With fashion's waste crisis accelerating, physical AI is well on its way to creating a viable path forwards and moving beyond the overproduction model that has defined the industry for decades.


'''    
    browser_cfg = BrowserConfig(headless=True)

    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, 
        exclude_external_links=True,
        magic=True,
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        
        result = await crawler.arun(url="https://www.weforum.org/stories/2026/03/physical-ai-fashion-manufacturing-water-waste/", config=run_cfg)

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
            
            token_gs_list = pulisci_e_tokenizza(testo_gs)
            token_pars_list = pulisci_e_tokenizza(testo_pulito)
            
            
            
            print("\n--- TESTO ESTRATTO ---\n")
            print(testo_pulito)
            token_level_eval(token_gs_list, token_pars_list)
        else:
            print("Errore: impossibile trovare il blocco principale.")

if __name__ == "__main__":
    asyncio.run(main())