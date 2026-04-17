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
    testo_gs = '''2026 NFL draft rankings: Field Yates' top 150 prospects


A week away from the 2026 NFL draft, my prospect rankings are complete! I released my top 25 rankings in January, expanded the list to 50 in March and am now up to 150.
Remember that this ranking isn't representative of where I think players will ultimately be drafted. This is simply my personal ranking of how I stack the prospects based on their overall talent and what I see on tape. It doesn't factor in team needs or positional value.
With that disclaimer out of the way, here is my ranking for the top 150 prospects in the 2026 class -- including scouting reports for each player in the top 50. Every prospect has a round grade, and my rankings by position are listed at the bottom.


1. Fernando Mendoza, QB, Indiana
Height: 6-5 | Weight: 236 | Grade: Round 1
Fresh off a Heisman Trophy winning season, Mendoza is an experienced quarterback with functional athleticism. He has ideal body armor for an NFL quarterback at his size, which he used in college to stay tough and durable against aggressive defenses.
With a powerful, accurate arm that can stretch to any level of the field, Mendoza completed 73% of his passes in 2025 (third highest in FBS). That included 19 touchdowns on throws outside the numbers. Mendoza showed improved pocket awareness in his lone season at Indiana, and he was outstanding in the red zone (27 touchdowns and zero interceptions).


2. Jeremiyah Love, RB, Notre Dame
Height: 6-0 | Weight: 212 | Grade: Round 1
Put your positional value conversations aside while discussing Love, as the Notre Dame star has every necessary skill for an elite running back. He has excellent speed and overall acceleration, posting a 4.36 40-yard dash at the combine and averaging nearly 7.0 yards per carry over the past two seasons.
Love is also a patient runner, using his exceptional vision and lateral agility to make defenders miss in the hole. He is inarguably the best receiving back in this class, averaging 10.4 yards per catch in 2025 from a variety of positional alignments. On top of it all, he did not lose a fumble in three college seasons and prides himself in his pass protection skills.


3. David Bailey, Edge, Texas Tech
Height: 6-4 | Weight: 251 | Grade: Round 1
Bailey capped off his college career at Texas Tech after three seasons at Stanford, during which he tied for the most sacks in the FBS with 14.5. His most dominant traits as a rusher are his explosive first step and aggressive approach to the game; he gets both around and through offensive tackles in pass protection.
Bailey routinely hurled offensive tackles onto their heels last season, allowing him to barrel through with brute force at the point of attack. He's not a dominant force yet defending the run, but he has the size to improve in that area. He posted an astonishing 71 pressures in 2025 to go along with three forced fumbles, bringing him to eight over the past two seasons.


4. Arvell Reese, Edge, Ohio State
Height: 6-4 | Weight: 241 | Grade: Round 1
One of the most distinctive defenders in the class, Reese is following a recent path for NFL stars: inside linebacker to edge rusher. He logged only 17 snaps rushing the passer in 2024, seeing that number boost to 97 in 2025. His range as an inside linebacker pops on the tape, while his explosiveness as a rusher really showed up in the first half of the 2025 season (6.5 sacks in the first eight games).
Reese still needs time to develop, relying more on athleticism than crafty pass-rush moves at this juncture. But that's an understandable reality given his lack of experience as a pass rusher. His upside is extremely enticing given how fluidly he moves at his size.


5. Sonny Styles, LB, Ohio State
Height: 6-5 | Weight: 244 | Grade: Round 1
Though Styles' profile has risen to new heights after a combine performance for the ages (including a 43½-inch vertical jump), the former safety is much more than just an athletic dynamo. His game is also highlighted by forceful tackling, a quick trigger defending the run and natural coverage instincts.
Tackling was one of Styles' most improved traits in 2025. He had only two missed tackles compared to 17 in 2024. Styles brings pass-rush ability to the table too, recording six sacks in 2024. Positional value will be considered by every team on him, but the quick-study linebacker is one of the cleanest prospects in the class.


6. Caleb Downs, S, Ohio State
Height: 6-0 | Weight: 206 | Grade: Round 1
Downs spent one year at Alabama before two at Ohio State, holding massive roles as a tone-setter at both stops. He has solid size for the position, packing an extensive punch as a tackler and force player.
Downs was used in a litany of ways throughout his college career, as he has the versatility to patrol in the center of the field or function as a linebacker in the box against the run. His physicality at the point of attack stands out, as he has impressive power blended with a tenacious mentality. He picked off two passes in each of his three seasons, with strong ball skills and an opportunistic mindset.


7. Carnell Tate, WR, Ohio State
Height: 6-2 | Weight: 192 | Grade: Round 1
To cap off this run of Ohio State players is Tate, who made the most of his opportunities in a jam-packed wide receiver room this past season. He set career highs in receiving yards per game (79.5), contested catches (10) and touchdowns (nine).
Tate has wiry strength and plays faster than his 40-yard dash time of 4.53 seconds. His superpowers are his hands (one drop in 2025 and 10¼-inch hands), disciplined route running and body control. He averaged 17.2 yards per reception this past season, with strong vertical tracking skills and catch strength on the sidelines. Tate also has versatility to play in a big slot role in the NFL.


8. Francis Mauigoa, OT, Miami
Height: 6-6 | Weight: 329 | Grade: Round 1
Maugioa started in every game over three college seasons, playing all but 11 snaps at right tackle. He has a strong, thick lower half, with exceptional balance and footwork in pass protection. He is light, fluid and reactive enough to handle elusive edge rushers. Plus, he's strong enough at the point of attack to make a big difference in the run game.
Mauigoa surrendered a mere two sacks over the past two seasons, and he finished with the lowest pressure percentage allowed out of all FBS tackles in 2025 (1.2%). He has shown plenty of evidence that he can be a right tackle in the NFL, though some evaluators believe his best long-term fit could be at guard.


9. Jordyn Tyson, WR, Arizona State
Height: 6-2 | Weight: 203 | Grade: Round 1
Tyson possesses a dynamic skill set that is led by his explosiveness. He had a down season in 2025 production-wise, but that was due to a lingering hamstring injury and shoddy quarterback play.
Tyson's final six games of the 2024 season were the kind that scouts don't forget when looking at a player: 50 catches, 732 yards and six touchdowns. Teams will have their own evaluation of his injury history (a torn ACL, broken collarbone and the aforementioned hamstring injury), but there's little doubt how he can impact an offense at 100%. He's a threat for a big play on every snap, with unique ability to make plays at all levels of the field.


10. Mansoor Delane, CB, LSU
Height: 6-0 | Weight: 187 | Grade: Round 1
After three seasons at Virginia Tech, Delane transferred to LSU for his final college season and boosted his draft profile in the process. He has good size for a cornerback, though there are some questions about his straight-line speed. He silenced some of those doubts with a 4.38 in the 40-yard dash at LSU's pro day.
Delane has excellent man-to-man technique, playing through the receiver's hands at the catch point with excellent timing. Opposing quarterbacks completed only 27.7% of their passes when he was the targeted defender, the third-lowest rate in the country.


11. Monroe Freeling, OT, Georgia
Height: 6-7 | Weight: 315 | Grade: Round 1
With only 18 starts, Freeling is a greener prospect than almost any other player so far in this ranking. That's a testament to his enticing skill set and exciting measurables (34¾-inch arms, 4.93 40-yard dash and 33.5-inch vertical jump).
Freeling showed dramatic improvement over the course of the 2025 season, and he's a smooth mover who covers a ton of surface area despite his frame. Freeling needs to further improve his body control and strength, so he would be best suited in a situation in which he could develop before being thrust into a starting role.
I am bullish that Freeling has as much upside as any offensive lineman in this class; he has all the skills to be a longtime left tackle.


12. Spencer Fano, OT, Utah
Height: 6-6 | Weight: 311 | Grade: Round 1
Fano spent the past two seasons at right tackle after previously holding down the left tackle spot at Utah. He is exceptionally light on his feet, with terrific redirect skills and a unique ability to get out into space and control second-level defenders.
Fano measured at just 32⅛-inch arms at the combine, so he profiles as a much stronger fit in a zone scheme where he can tap into his foot quickness and body control. His lateral skills allowed him to really shine as a pass protector over the past two seasons, surrendering 13 pressures and only one sack.


13. Rueben Bain Jr., Edge, Miami
Height: 6-2 | Weight: 263 | Grade: Round 1
One of the headliners in this class, Bain won ACC Defensive Player of the Year after posting 9.5 sacks for Miami during its run to the CFP National Championship game. His undersized frame has been a talking point in the predraft process, as he has sub-31-inch arms. Per ESPN Research, no edge rusher over the past two decades has been drafted in the first round with those measurements.
But Bain more than makes up for his frame with his hands. He is at his best when engaging with offensive tackles and barreling through them, plus he can contribute as a violent run defender (nine run stops in 2025). Bain isn't a premier athlete, but he's a full-tilt rusher who wears down opponents and would be best in an even front at the NFL level.


14. Kadyn Proctor, OT, Alabama
Height: 6-7 | Weight: 352 | Grade: Round 1
Proctor has been on the NFL's radar since his arrival as a massive recruit in Alabama, where he started all 40 games that he appeared in. He has outstanding size and stood out at the combine with a 32-inch vertical and 5.22 40-yard dash (a good number for someone of his stature).
Proctor's foot quickness was overmatched by edge rushers at times this past season, as his massive frame left a large strike zone for players to get underneath and use leverage against him. But he is best described as a human forklift when he gets hands on a defender. He barrels through players in the running game, and he can use his length to drive rushers away from the quarterback. There's major upside for the 20-year old tackle.


15. Olaivavega Ioane, G, Penn State
Height: 6-4 | Weight: 320 | Grade: Round 1
There are few prospects as reliable and consistent as Ioane, who started 27 games over the past two seasons and took snaps at every O-line position. The rugged, powerful Ioane uses his strong frame to get after defenders in the running game with force and accurate striking at all levels.
Penn State used Ioane on the move often, as he's able to maintain his body control or find work in space while run blocking. He is also excellent in pass protection, as he did not give up a sack over the past two seasons. While best fit at guard, Ioane's versatility further stamps him as one of the highest-floor players in the class.


16. Jermod McCoy, CB, Tennessee
Height: 6-1 | Weight: 188 | Grade: Round 1
McCoy has only two years of tape to work with, as he sat out the 2025 season after tearing his ACL last January. His lone season at Tennessee in 2024 was outstanding, showcasing the totality of his 77-inch wingspan with seven pass breakups and four interceptions. He is a confident man-to-man coverage player with terrific balance, patience and ball skills.
McCoy is at his best blanketing perimeter wideouts who want to stretch the field vertically; he's a big-play neutralizer on his own. After not working out at the combine, he posted a 4.38-second 40-yard dash, a 38-inch vertical jump and a 10-foot-7 broad jump at Tennessee's pro day.

17. Makai Lemon, WR, USC
Height: 5-11 | Weight: 192 | Grade: Round 1
Few prospects are more enjoyable to watch than Lemon, a fierce competitor who makes up for his pedestrian size with toughness, strong hands and run-after-catch skills. He had a dominant final season at USC, setting career highs in catches (79), yards (1,156) and touchdowns (11). He also dropped only one pass for the third straight season.
Lemon had 20 contested catches over the past two seasons, displaying a catch radius that one would associate with a dominant perimeter wideout. He's instinctive after the catch with strong contact balance that will bode well for manufactured opportunities near the line of scrimmage.


18. Kenyon Sadiq, TE, Oregon
Height: 6-3 | Weight: 241 | Grade: Round 1
There is great depth in this tight end class, led by the overwhelmingly dynamic Sadiq. He had to be patient to make his mark, but he worked his way from Oregon's special teams snaps leader in 2024 to the FBS leader in receiving touchdowns by a tight end in 2025 (eight).
Sadiq blazed a 4.39 40-yard dash at the combine, and he's at his very best with his ball in his hands after the catch. Plus, he's a willing blocker who can be moved all over the offensive formation because of his athletic skills. The one thing Sadiq needs to clean up is the drops, as he had six in 2025.


19. Dillon Thieneman, S, Oregon
Height: 6-0 | Weight: 201 | Grade: Round 1
Like the tight end class, there's good depth at safety. Thieneman stands atop as the best ball-hawking center fielder among them. He snagged six interceptions as a true freshman with Purdue in 2023 before two with the Ducks in 2025. He has a strong ability to diagnose plays, and has great vision and hands that would grade out well if he were a receiver.
Few players performed better at the combine than Thieneman, who ran a 4.35 40-yard dash and crushed the on-field workouts. He showed improvement as a tackler in 2025, finishing with eight missed tackles compared to 22 in 2024. That's an area he can further solidify with more strength at the NFL level.



20. Akheem Mesidor, Edge, Miami
Height: 6-3 | Weight: 259 | Grade: Round 1/2
Mesidor finished up his six-year college career with four seasons at Miami, ebbing back and forth from a defensive tackle to edge alignment. Playing a much heavier edge role in 2025, Mesidor led Miami in sacks (12.5), including a dominant stretch in the CFP in which he had 5.5 in four games.
His impressive first-step quickness gave offensive tackles fits, but he also destroyed interior offensive linemen when he reduced down inside as a rusher. His pressure percentage when aligned as a defensive tackle was an astonishing 23.9%. He will turn 25 in early April, so the possibility of Mesidor being taken lower than this overall rating is definitely in play. But he's a relentless rusher who could fit in most every scheme.


21. Blake Miller, OT, Clemson
Height: 6-7 | Weight: 317 | Grade: Round 1/2
The case for Miller is pretty straightforward. If you're looking for an experienced, battle-tested, athletic offensive tackle who has steadily improved throughout his career, he fits the bill. A four-year starter at right tackle, Miller has logged nearly 3,700 career snaps and decreased the number of pressures he gave up in each season -- only nine pressures and two sacks in 2025. He also became a more disciplined player throughout his career after nine penalties as a true freshman.
Miller has great overall size and length (nearly at 84-inch wingspan), as well as light feet. I'd like to see him continue to add to his strength and be more aggressive with his punch in pass protection.


22. Caleb Lomu, OT, Utah
Height: 6-6 | Weight: 313 | Grade: Round 1/2
I like to describe Lomu as a "Steady Eddie," as he is consistently under control in pass protection, doing a great job of marrying his hands with the lower half of his body. He did not give up a sack in 2025, anchoring the left tackle spot for Utah over the past two seasons opposite of Spencer Fano.
Lomu showed steady growth from 2024 to 2025. His athletic testing at the combine mirrored his play on the field, including a 4.99-second 40-yard dash. He times his punch well in pass protection and shows some of the best recovery skills of any tackle in the class.


23. Omar Cooper Jr., WR, Indiana
Height: 6-0 | Weight: 199 | Grade: Round 1/2
Cooper was an extremely clutch player for Indiana this past season, a breakout year in which he led the team with 13 receiving touchdowns. He is one of the best run-after-catch players in the draft, showing great patience, instincts and contact balance to turn screens into solid gains. He averaged 7.28 yards after the catch in 2025. He is an impressive route runner, uses his body well to create leverage at the catch point and does all the dirty work you want to see out of your wide receivers.


24. R Mason Thomas, Edge, Oklahoma
Height: 6-2 | Weight: 241 | Grade: Round 1/2
Thomas is another fringe first-rounder who brings a distinctive build to the table. He has sub-32-inch arms, but he has extremely powerful hands and is one of the better prospects at using his lower center of gravity to get underneath offensive tackles. Thomas' pass-rush acumen is what will get him drafted this high, but his heavy mitts to set the edge and reduce running lanes also stands out. He had a combined 21 run stops over the past two seasons.
A quad injury limited Thomas to only 10 games this past season, but he still posted 6.5 sacks and 23 pressures on 173 pass-rushing snaps. He has burst off the edge that will appeal to any NFL defensive line coach.


25. Denzel Boston, WR, Washington
Height: 6-4 | Weight: 212 | Grade: Round 1/2
When studying Boston's tape, one of the first things that sticks out is just how buttery smooth he is as a mover and route runner. Unsurprisingly, he plays most of his snaps as a perimeter wideout given his excellent size, but he has the fluidity and route-running tact to be in a big slot role. He posted 20 receiving touchdowns over the past two seasons and dropped only four of his 209 career targets.
Boston's long speed and separation skills are two areas that will determine his ceiling in the NFL, as scouts do have questions.

26. Keldric Faulk, Edge, Auburn
Height: 6-6 | Weight: 276 | Grade: Round 1/2
Faulk's 2025 season was inferior to his 2024 season (2.0 sacks compared with 7.0, respectively). But he is a true junior who will not turn 21 until September, so his trajectory could still very much be on the upward slope.
Faulk has excellent overall size and length, including an 82-inch wingspan. He's not a rusher who wins with quickness off the snap, but rather someone who can get to the quarterback with size, length and smooth strides around the edge. Faulk must develop a better and more diverse rush plan against offensive tackles, but he also provides value as a sturdy run defender who can play from a variety of positions.


27. KC Concepcion, WR, Texas A&M
Height: 6-0 | Weight: 196 | Grade: Round 1/2
Concepcion is a big play waiting to happen. While modest in stature, he's not only one of the fastest players in the class, but also one of the easiest accelerators. Transferring to Texas A&M after two seasons at NC State opened up all sorts of explosive opportunities for him. He beefed up his yards per catch from 8.7 in 2024 to 15.1, while also taking a pair of punts to the house with the Aggies. Drops were an issue in 2025 (seven), but those were much more concentration-related than a strength or natural ability issue.


28. T.J. Parker, Edge, Clemson
Height: 6-4 | Weight: 263 | Grade: Round 1/2
Parker entered the 2025 season with eyes on being a top-10 pick in the class, but his season left a lot to be desired. In 2024, he set a Clemson record with six forced fumbles, a year after he set a Clemson freshman record with 12.5 tackles for loss.
Parker has a sturdy frame and plays with powerful, active and heavy hands. His splash-play production really fell off in 2025, but he showed good burst and hand usage during Senior Bowl week as a reminder of the best version of his skill set.


29. Ty Simpson, QB, Alabama
Height: 6-1 | Weight: 211 | Grade: Round 1/2
The 23-year-old Simpson became a first-year starter in 2025, leading Alabama to a CFP win in his 15 starts. His 2025 season was a tale of two halves, as he threw 21 touchdowns and only one interception in the first nine games before only seven touchdowns and four picks in the final six games. His accuracy shined early in the season, as did his ability to drive the football when he had the chance to set his feet.
Simpson has ordinary size for a quarterback, but he is an active and instinctive scrambler. He rushed for 296 yards (taking away sack yardage) in 2025. The evaluations of Simpson vary, but within the right system that highlights his processing and accuracy that we saw early in 2025, he could become a solid starter in the NFL.


30. Emmanuel McNeil-Warren, S, Toledo
Height: 6-4 | Weight: 201 | Grade: Round 1/2
With outstanding length for a safety, McNeil-Warren is the only non-Power 4 player in this ranking. The hallmark of his skill set is his ability to neutralize big plays. McNeil-Warren had 12 pass breakups and five interceptions over the past three seasons. He started off the 2025 season with a bang, posting 11 tackles, a forced fumble and a fumble recovery in against Kentucky.
McNeil-Warren's combine 40-yard dash didn't jump off the page at 4.52 seconds, and he isn't a thumper getting downhill in the running game, but he can be an impact center fielder with his range.


31. Chris Johnson, CB, San Diego State
Height: 6-0 | Weight: 193 | Grade: Round 1/2
Two words feel the most important on Johnson: natural playmaker. He had an exceptional 2025 season during which opposing quarterbacks targeting him as the closest coverage player posted a QBR of just 6.8 and completed 30.6% of their passes. Those numbers ranked 10th and seventh in the FBS, respectively.
His change-of-direction skills and ability to trigger back to the ball are apparent, and he can fly on vertical routes downfield. Johnson is not an overly physical corner, but his reactive athletic skills allow him to stay sticky in coverage.


32. Max Iheanachor, OT, Arizona State
Height: 6-6 | Weight: 321 | Grade: Round 1/2
One of the most intriguing players in the class, Iheanachor didn't even play high school football before taking to the sport in 2021 at East Los Angeles College. He played both tackle positions there for two seasons before three years at Arizona State.
Iheanachor has some outstanding traits, including an 83¼-inch wingspan. He ran a 4.91-second 40-yard dash at the combine, which tied for second fastest among O-linemen.
That athleticism transfers on tape, as he has fluid feet and can match-and-mirror rushers coming off the edge. He has to play with a more balanced base and still looks inexperienced at times, but that just means his upside is immense. Plus, he held his own in some spotlight games this past season.


33. Kayden McDonald, DT, Ohio State
Height: 6-2 | Weight: 326 | Grade: Round 1/2
The rugged McDonald blossomed in 2025, anchoring Ohio State's run defense in 14 games and 440 defensive snaps. He mostly lined up as a head-up nose tackle under defensive coordinator Matt Patricia, overwhelming centers in the running game and consistently resetting the line of scrimmage. He also made life easier on second-level defenders by creating space.
McDonald showed a little bit of pass-rush juice this past season, logging 3.0 sacks, but his more important contributions will be his ability to change the shape of the interior of the pocket. He is scheme versatile and will appeal to teams looking to crack down on chunk runs allowed.



34. Peter Woods, DT, Clemson
Height: 6-3 | Weight: 298 | Grade: Round 1/2
Woods was one of the top prospects entering 2025, but he had an OK season compared to the lofty expectations. He posted only five sacks in three seasons at Clemson, while seeing his pressures drop from 20 in 2024 to 11 in 2025.
Woods also measured with 31¼-inch arms at the combine, lacking the ideal dimensions to build a wall against the run or take on bulldozing bodies. And yet, he has exceptional quickness, powerful and active hands and an ability to diagnose plays that is keeping evaluators tantalized. The best version of Woods has not been realized yet, but disruptive interior defensive linemen -- even when they aren't generating sacks -- make life much easier for edge rushers. Maximizing Woods would result in a very tough defensive line to guard.


35. Colton Hood, CB, Tennessee
Height: 6-0 | Weight: 193 | Grade: Round 1/2
Hood played one season apiece at Auburn, Colorado and Tennessee. He is a high-energy competitor who is unafraid to help in the running game, but he's the most confident in man coverage on perimeter receivers.
Hood is a stellar athlete who posted a 40.5-inch vertical and 4.44 in the 40-yard dash. That explosiveness shows up at the catch point on tape, with 10 pass breakups in 2025. Hood needs to improve his discipline with his hands at the top of routes; he was flagged four times for pass interference or holding in 2025.


36. Avieon Terrell, CB, Clemson
Height: 5-11 | Weight: 186 | Grade: Round 1/2
The axiom of not judging a book by its cover applies to Terrell, as the three-year player is small but one of the fiercest cornerbacks in the class. Over the past two seasons, Terrell played 210 press coverage snaps -- he has a desire to get into the grill of opposing wide receivers. He forced an incredible eight fumbles over the past two seasons and shows exceptional timing on opportunities to dislodge the ball.
Terrell's lack of size will be tested by perimeter receivers at the NFL level, especially in the red zone. But his competitive instincts cannot be discounted. Terrell aggravated his hamstring on his first 40-yard dash run at Clemson's pro day, posting a 4.64.


37. Jadarian Price, RB, Notre Dame
Height: 5-11 | Weight: 203 | Grade: Round 2
Price's draft outlook could have been much different under other circumstances, but it just so happened that the clear-cut second-best running back in this class played behind the best one (Jeremiyah Love). But Price is a far different back, bringing a nasty package of power, contact balance and breakaway speed that allowed him to average 6.04 yards per carry in college.
Price was a limited participant in the passing game behind Love, totaling only six catches in 2025. But he showed sufficient ability as a screen receiver, turning those opportunities into a pair of touchdowns. He's an exceptional kickoff return man as well, taking 3 of 22 attempts for a touchdown.
The biggest downside on Price is his ball security; he fumbled three times on 113 rushes last season. He could start in an NFL backfield that complements him with a solid pass-catching back.


38. Malachi Lawrence, Edge, UCF
Height: 6-4 | Weight: 253 | Grade: Round 2
If the assignment is to find a pure rusher, Lawrence will be at the top of the list for some teams. He posted a jaw-dropping 4.52-yard dash in the 40 at the combine (second among defensive linemen) and had a 40-inch vertical jump. Plus. he measured in with 33⅝-inch arms.
Lawrence totaled 60 pressures over the past two seasons with a great first step and understanding of how to use his hands. He is one of the best closers among this class, as some of his best sacks from the 2025 season were hustle plays to stay with scrambling quarterbacks. Teams are going to test Lawrence against the run, where he must be stronger at the point of attack.



39. Zion Young, Edge, Missouri
Height: 6-6 | Weight: 262 | Grade: Round 2
After two years at Michigan State, Young concluded his college career with two seasons at Missouri. He was excellent for the Tigers in 2025, using heavy, active hands to pave his way through offensive tackles. Young is also a determined run stuffer, displaying the ability to lock out and set the edge. He has been tapped into often as an interior rusher in a reduced front, as his overall build and power allows him to handle the collisions that occur in tight quarters. His quickness also gives interior protectors fits.


40. Brandon Cisse, CB, South Carolina
Height: 6-0 | Weight: 189 | Grade: Round 2
Cisse finished his college career at South Carolina after two years at North Carolina State. He is at his best in press coverage, where he aligned on 81 snaps in 2025, since it allows him to flash his size and overall physicality.
Cisse posted a 41-inch vertical at the combine, and that trait shows up on tape. He's also an energetic run defender who had six run stuffs in 2025. Quicker receivers can give him trouble at the top of routes, but Cisse could thrive for an NFL team that lets him get physical at the line of scrimmage.


41. Jacob Rodriguez, LB, Texas Tech
Height: 6-1 | Weight: 231 | Grade: Round 2
It's hard to encapsulate just how outstanding Rodriguez's final college season was, as the Heisman Trophy finalist forced seven fumbles, intercepted four passes, scored on defense and offense. He was almost literally all over the field for Texas Tech.
That production is a testament to a player with rare instincts and processing skills. Rodriguez smoothly drops into coverage, is a precise "Peanut Puncher" and very good athlete. He might not have mass appeal because of his size, but he could be a home-run addition to the right scheme.


42. Cashius Howell, Edge, Texas A&M
Height: 6-3 | Weight: 253 | Grade: Round 2
Howell finished his five-year college career with two seasons at Texas A&M, earning SEC Defensive Player of the Year honors in 2025. He has a distinctive body type, as his 30¼-inch arm length is an extreme outlier for an edge who will be drafted as high as he likely will. But Howell's burst off the edge is among the best in class, as he pairs it with the ability to close the gap on pass protectors or turn the corner in a hurry.
His natural athletic movements showed up when he occasionally dropped into coverage, while his length showed up at the point of attack in the running game. Howell is at his best when he has the chance to focus on taking down the QB.


43. Chase Bisontis, G, Texas A&M
Height: 6-5 | Weight: 315 | Grade: Round 2
Bisontis is a versatile prospect who settled in at left guard for his final two seasons after playing predominantly right tackle as a true freshman. He's a nifty athlete with light feet, strong redirect skills and good size.
Bistontis' instincts and lateral agility empower him to survive amid interior traffic in pass protection, handling pass-rush games and cross-face rushers well. He still must develop further core strength, an area that showed up in a first-round CFP game when Miami's dominant defensive line overpowered him frequently. He'll have appeal to all teams, but especially those in a zone running scheme.


44. Caleb Banks, DT, Florida
Height: 6-6 | Weight: 327 | Grade: Round 2
If rankings were determined by the apex of a player's ability, Banks would be much higher on this list. He has built-in-a-lab measurables at his position, including just over 35-inch arms. Those tools showed up in a major way during a dominant week at the Senior Bowl. The evaluation on Banks is more complex because he was limited to three games in 2025 and recently underwent foot surgery. He's expected to be shelved from full football activity until June. On the field, Banks also needs to be more consistent.
Banks has massive power in his hands, plus quickness to shed blockers and influence plays behind the line of scrimmage. Sometimes, he can affect the shape of the pocket for quarterbacks as a rusher. Banks is one of those prospects that a team needs find out how to bring out his best on a consistent basis. If a team can do that, he has Pro Bowl upside. Every team's medical tolerance is a little bit different, so the range on grades could prove very wide.


45. CJ Allen, LB, Georgia
Height: 6-1 | Weight: 230 | Grade: Round 2
The quarterback of Georgia's defense in 2025, Allen is a slightly undersized inside linebacker. He is a cerebral, standout communicator who has good range and strong instincts that show up often in run defense. Allen has some tightness on tape, but he's comfortable spot-dropping in pass coverage. He set a career high in total tackles in 2025 with 88, and he contributed to Georgia's pass rush with 3.5 sacks. He's a solid, steady player with a high floor.

46. Anthony Hill Jr., LB, Texas
Height: 6-2 | Weight: 238 | Grade: Round 2
Amid a deep linebacker class, Hill has about as much production as any: 17.0 sacks, seven forced fumbles and three interceptions over the past three seasons. He's an opportunistic, extremely athletic stand-up linebacker who can also rush the passer as a blitzer or off the edge. Hill has a little bit of a Jekyll-and-Hyde nature to his game. He doesn't always read play development as quickly as other linebackers in this class, but he has the athletic ability to make up for any misreads.


47. Keylan Rutledge, G, Georgia Tech
Height: 6-4 | Weight: 316 | Grade: Round 2
I'll put Rutledge on the short list for nastiest players in the class, as the tone-setting guard wants to impose his will whenever possible. A two-year player at Georgia Tech, Rutledge logged over 1,700 snaps and surrendered only one sack. But the strength of his game is his play as a run blocker. He is a ferocious striker with hands like boulders that knock defenders on their back. That mentality is balanced by discipline, as Rutledge was flagged for a personal foul only once in his four college seasons.


48. Christen Miller, DT, Georgia
Height: 6-4 | Weight: 321 | Grade: Round 2
Miller appeared in 43 games and had 1,041 career defensive snaps for the Bulldogs. That modest number of snaps is important to note as it led to only 4.0 career sacks, but Georgia's scheme relies heavily on a defensive line rotation. And the scheme doesn't call for linemen to simply penetrate gaps or hunt splash plays behind the line of scrimmage.
Miller has excellent power to hold his ground, stay square and take on double-teams. He's a stout, selfless run defender who made life better for linebackers behind him. Miller's pass-rush impact is better than his sacks suggest, as his length and ability to drive offensive linemen back forced quarterbacks to reset their throwing platform or scramble from the pocket. Some players bring the sizzle; Miller brings the steak to make a defense better.


49. Jake Golday, LB, Cincinnati
Height: 6-5 | Weight: 239 | Grade: Round 2
A former Central Arkansas standout who spent two seasons at Cincinnati, Golday was an absolute force in 2025. He has impressive size to go along with significant range and versatility.
Golday can get downhill and affect the running game -- but sometimes he takes too aggressive of an angle on perimeter runs -- while also flashing rush ability from the edge (harkening back to his days as a defensive end at Central Arkansas). Though he doesn't have much on-ball production yet in pass coverage, his natural movement skills suggest it's an area in which he can become a real factor.


50. Gabe Jacas, Edge, Illinois
Height: 6-4 | Weight: 260 | Grade: Round 2
Jacas has been among the most productive pass rushers in the Big Ten over the past two seasons, racking up 19.0 sacks and 74 pressures. He's a rugged, determined run defender who uses powerful hands to set an edge. Jacas is not a premiere athlete, but he has the size teams covet to hold up against bigger offensive tackles in the NFL.


More Round 2 prospects
51. Josiah Trotter, LB, Missouri 52. Eli Stowers, TE, Vanderbilt 53. D'Angelo Ponds, CB, Indiana 54. Germie Bernard, WR, Alabama 55. Zachariah Branch, WR, Georgia 56. Emmanuel Pregnon, G, Oregon


Round 2-3 prospects
57. Keionte Scott, CB, Miami 58. Gennings Dunker, OT, Iowa 59. Kyle Louis, LB, Pitt 60. Treydan Stukes, CB, Arizona 61. Chris Bell, WR, Louisville 62. Lee Hunter, DT, Texas Tech 63. Caleb Tiernan, OT, Northwestern 64. Antonio Williams, WR, Clemson 65. Keyron Crawford, Edge, Auburn 66. Domonique Orange, DT, Iowa State 67. Zakee Wheatley, S, Penn State 68. Brenen Thompson, WR, Mississippi State 69. Jaishawn Barham, Edge, Michigan 70. Dani Dennis-Sutton, Edge, Penn State 71. Ted Hurst, WR, Georgia State 72. Oscar Delp, TE, Georgia

Round 3 prospects
73. Malachi Fields, WR, Notre Dame 74. Jalen Farmer, OG, Kentucky 75. Chris Brazzell II, WR, Tennessee 76. A.J. Haulcy, S, LSU 77. Carson Beck, QB, Miami 78. De'Zhaun Stribling, WR, Ole Miss 79. Keith Abney II, CB, Arizona State 80. Bud Clark, S, TCU 81. Jalon Kilgore, CB, South Carolina 82. Austin Barber, OT, Florida 83. Derrick Moore, Edge, Michigan 84. Max Klare, TE, Ohio State 85. Garrett Nussmeier, QB, LSU 86. Darrell Jackson Jr., DT, Florida State 87. Bryce Lance, WR, North Dakota State 88. Mike Washington Jr., RB, Arkansas 89. Elijah Sarratt, WR, Indiana



Round 3-4 prospects
90. Devin Moore, CB, Florida 91. Travis Burke, OT, Memphis 92. Tacario Davis, CB, Washington 93. Logan Jones, C, Iowa 94. Deion Burks, WR, Oklahoma 95. Chris McClellan, DT, Missouri 96. Gracen Halton, DT, Oklahoma 97. Jake Slaughter, C, Florida 98. Malik Muhammad, CB, Texas 99. Skyler Bell, WR, UConn 100. Tyler Onyedim, DT, Texas A&M 101. Chandler Rivers, CB, Duke 102. Sam Hecht, C, Kansas State 103. Sam Roush, TE, Stanford 104. Dametrious Crownover, OT, Texas A&M 105. Connor Lew, C, Auburn 106. Kage Casey, OT, Boise State 107. Kaleb Elarms-Orr, LB, TCU 108. Davison Igbinosun, CB, Ohio State 109. Joshua Josephs, Edge, Tennessee 110. Trey Zuhn III, C, Texas A&M 111. LT Overton, Edge, Alabama

Round 4 prospects
112. Cole Payton, QB, North Dakota State 113. Julian Neal, CB, Arkansas 114. Daylen Everette, CB, Georgia 115. Genesis Smith, S, Arizona 116. Febechi Nwaiwu, G, Oklahoma 117. Brian Parker II, C, Duke 118. Justin Joly, FB/H-Back, NC State 119. Keyshaun Elliott, LB, Arizona State 120. Will Kacmarek, TE, Ohio State 121. Will Lee III, CB, Texas A&M 122. Beau Stephens, G, Iowa 123. Jadon Canady, CB, Oregon 124. Billy Schrauth, G, Notre Dame 125. Drew Shelton, OT, Penn State 126. Nick Barrett, DT, South Carolina 127. Drew Allar, QB, Penn State 128. Zane Durant, DT, Penn State 129. Markel Bell, OT, Miami 130. Caden Curry, Edge, Ohio State


Round 4-5 prospects
131. Jonah Coleman, RB, Washington 132. Emmett Johnson, RB, Nebraska 133. Jeremiah Wright, G, Auburn 134. Jimmy Rolder, LB, Michigan 135. Taylen Green, QB, Arkansas 136. Jude Bowry, OT, Boston College 137. Marlin Klein, TE, Michigan 138. Colbie Young, WR, Georgia 139. Malik Benson, WR, Oregon 140. Nate Boerkircher, TE, Texas A&M 141. Diego Pounds, OT, Ole Miss 142. Joe Royer, TE, Cincinnati 143. Kamari Ramsey, S, USC 144. Jack Endries, TE, Texas 145. Eli Raridon, TE, Notre Dame 146. Jakobe Thomas, S, Miami 147. Keagen Trost, G, Missouri 148. Nicholas Singleton, RB, Penn State 149. Ja'Kobi Lane, WR, USC 150. TJ Hall, CB, Iowa


Position rankings
Quarterbacks
1. Fernando Mendoza, Indiana 2. Ty Simpson, Alabama 3. Carson Beck, Miami 4. Garrett Nussmeier, LSU 5. Cole Payton, North Dakota State 6. Drew Allar, Penn State 7. Taylen Green, Arkansas

Running backs
1. Jeremiyah Love, Notre Dame 2. Jadarian Price, Notre Dame 3. Mike Washington Jr., Arkansas 4. Jonah Coleman, Washington 5. Emmett Johnson, Nebraska 6. Nicholas Singleton, Penn State

Fullbacks/H-Backs
1. Justin Joly, NC State 2. Michael Trigg, Baylor 3. Oscar Delp, Georgia

Wide receivers
1. Carnell Tate, Ohio State 2. Jordyn Tyson, Arizona State 3. Makai Lemon, USC 4. Omar Cooper Jr., Indiana 5. Denzel Boston, Washington 6. KC Concepcion, Texas A&M 7. Germie Bernard, Alabama 8. Zachariah Branch, Georgia 9. Chris Bell, Louisville 10. Antonio Williams, Clemson 11. Brenen Thompson, Mississippi State 12. Ted Hurst, Georgia State 13. Malachi Fields, Notre Dame 14. Chris Brazzell II, Tennessee 15. De'Zhaun Stribling, Ole Miss 16. Bryce Lance, North Dakota State 17. Elijah Sarratt, Indiana 18. Deion Burks, Oklahoma 19. Skyler Bell, UConn 20. Colbie Young, Georgia 21. Malik Benson, Oregon 22. Ja'Kobi Lane, USC

Tight ends
1. Kenyon Sadiq, Oregon 2. Eli Stowers, Vanderbilt 3. Oscar Delp, Georgia 4. Max Klare, Ohio State 5. Sam Roush, Stanford 6. Will Kacmarek, Ohio State 7. Marlin Klein, Michigan 8. Nate Boerkircher, Texas A&M 9. Joe Royer, Cincinnati 10. Jack Endries, Texas 11. Eli Raridon, Notre Dame

Offensive tackles
1. Francis Mauigoa, Miami 2. Monroe Freeling, Georgia 3. Spencer Fano, Utah 4. Kadyn Proctor, Alabama 5. Blake Miller, Clemson 6. Caleb Lomu, Utah 7. Max Iheanachor, Arizona State 8. Gennings Dunker, Iowa 9. Caleb Tiernan, Northwestern 10. Austin Barber, Florida 11. Travis Burke, Memphis 12. Dametrious Crownover, Texas A&M 13. Kage Casey, Boise State 14. Drew Shelton, Penn State 15. Markel Bell, Miami 16. Jude Bowry, Boston College 17. Diego Pounds, Ole Miss

Guards
1. Olaivavega Ioane, Penn State 2. Chase Bisontis, Texas A&M 3. Keylan Rutledge, Georgia Tech 4. Emmanuel Pregnon, Oregon 5. Jalen Farmer, Kentucky 6. Febechi Nwaiwu, Oklahoma 7. Beau Stephens, Iowa 8. Billy Schrauth, Notre Dame 9. Jeremiah Wright, Auburn 10. Keagen Trost, Missouri

Centers
1. Logan Jones, Iowa 2. Jake Slaughter, Florida 3. Sam Hecht, Kansas State 4. Connor Lew, Auburn 5. Trey Zuhn III, Texas A&M 6. Brian Parker II, Duke



Edge rushers
1. David Bailey, Texas Tech 2. Arvell Reese, Ohio State 3. Rueben Bain Jr., Miami 4. Akheem Mesidor, Miami 5. R Mason Thomas, Oklahoma 6. Keldric Faulk, Auburn 7. T.J. Parker, Clemson 8. Cashius Howell, Texas A&M 9. Malachi Lawrence, UCF 10. Zion Young, Missouri 11. Gabe Jacas, Illinois 12. Keyron Crawford, Auburn 13. Jaishawn Barham, Michigan 14. Dani Dennis-Sutton, Penn State 15. Derrick Moore, Michigan 16. Joshua Josephs, Tennessee 17. LT Overton, Alabama 18. Caden Curry, Ohio State

Defensive tackles
1. Kayden McDonald, Ohio State 2. Peter Woods, Clemson 3. Caleb Banks, Florida 4. Christen Miller, Georgia 5. Lee Hunter, Texas Tech 6. Domonique Orange, Iowa State 7. Darrell Jackson Jr., Florida State 8. Chris McClellan, Missouri 9. Gracen Halton, Oklahoma 10. Tyler Onyedim, Texas A&M 11. Nick Barrett, South Carolina 12. Zane Durant, Penn State

Linebackers
1. Sonny Styles, Ohio State 2. Jacob Rodriguez, Texas Tech 3. CJ Allen, Georgia 4. Anthony Hill Jr., Texas 5. Jake Golday, Cincinnati 6. Josiah Trotter, Missouri 7. Kyle Louis, Pitt 8. Kaleb Elarms-Orr, TCU 9. Keyshaun Elliott, Arizona State 10. Jimmy Rolder, Michigan

Cornerbacks
1. Mansoor Delane, LSU 2. Jermod McCoy, Tennessee 3. Chris Johnson, San Diego State 4. Colton Hood, Tennessee 5. Avieon Terrell, Clemson 6. Brandon Cisse, South Carolina 7. D'Angelo Ponds, Indiana 8. Keionte Scott, Miami 9. Treydan Stukes, Arizona 10. Keith Abney II, Arizona State 11. Jalon Kilgore, South Carolina 12. Devin Moore, Florida 13. Tacario Davis, Washington 14. Malik Muhammad, Texas 15. Chandler Rivers, Duke 16. Davison Igbinosun, Ohio State 17. Julian Neal, Arkansas 18. Daylen Everette, Georgia 19. Will Lee III, Texas A&M 20. Jadon Canady, Oregon 21. TJ Hall, CB, Iowa

Safeties
1. Caleb Downs, Ohio State 2. Dillon Thieneman, Oregon 3. Emmanuel McNeil-Warren, Toledo 4. Zakee Wheatley, Penn State 5. A.J. Haulcy, LSU 6. Bud Clark, TCU 7. Genesis Smith, Arizona 8. Kamari Ramsey, USC 9. Jakobe Thomas, Miami

Kickers
1. Dominic Zvada, Michigan 2. Drew Stevens, Iowa 3. Trey Smack, Florida

Punters
1. Brett Thorson, Georgia 2. Ryan Eckley, Michigan State 3. Jack Stonehouse, Syracuse

Long snappers
1. Luke Basso, Oregon 2. Garrison Grimes, BYU 3. Tyler Duzansky, Penn State
'''    # 1. MODIFICA CRITICA: headless=False aprirà il browser così possiamo VEDERE cosa succede
    browser_cfg = BrowserConfig(headless=True)

    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, 
        exclude_external_links=True,
        magic=True,
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url="https://www.espn.com/nfl/draft2026/story/_/id/47590505/2026-nfl-draft-rankings-board-top-prospects-best-positional-field-yates#four", config=run_cfg)

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
            
            token_gs_list = pulisci_e_tokenizza(testo_gs)
            token_pars_list = pulisci_e_tokenizza(testo_pulito)
            
            
            
            print("\n--- TESTO ESTRATTO ---\n")
            #print(testo_pulito)
            token_level_eval(token_gs_list, token_pars_list)
        else:
            print("Errore: impossibile trovare il blocco principale.")

if __name__ == "__main__":
    asyncio.run(main())