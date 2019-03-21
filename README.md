# kellerkompanie-crawler
A simple crawler for the Kellerkompanie webpages.

## Dependencies
* Python 3.7
* dateparser package (https://dateparser.readthedocs.io/en/latest/installation.html): 
```pip install dateparser```

## Examples
### Generate news.json
Generates the news.json file based on announcements from the forum (news section) and announced missions from 
the missions subforum

```
python forum_crawler.py news.json
``` 

It will generate news entries with following properties:
* uuid: string
* newsType: enum of value "NEWS", "DONATION", "MISSION"
* title: string
* content: string
* weblink: string
* timestamp: long

Example:
```
{
    "uuid": "de262609-3b28-495f-a4f8-b8c60db16210",
    "newsType": "NEWS",
    "title": "[Info] Transparenzbericht Serverkosten",
    "content": "Um die Transparenz der Serverkosten (in Bezug auf die Spenden) zu erh\u00f6hen hier nun einige Infos \u00fcber die Kiste. Dies betrifft den Gameserver und den Wiki Webserver, nicht das TS und die Webseite/Forum, diese werden weiterhin von Ravin gestellt. Als Gameserver besitzen wir einen Hetzner der Reihe EX61-NVMe im Rechenzentrum Frankfurt mit einem Intel\u00ae Core\u2122 i7-8700 (Hexa Core), 64GB DDR4 RAM und 512GB NVMe SSD. Die Auswahl dieses Modells lag an der vergleichsweise hohen Single Thread Performance, von der ArmA profitiert. Die 64GB sind Overkill, konnten aber nicht angepasst werden in dem Modell. Auf dem Gameserver laufen 4 ArmA Instanzen parallel: der eigentliche Server und 3 headless clients. Au\u00dferdem wird dar\u00fcber auch das Repo und das Webinterface f\u00fcr den Server gehostet. Der Gameserver kostet im Monat 70,21 \u20ac. Das Wiki l\u00e4uft auf einem virtuellen Server, der ebenfalls bei Hetzner gehostet ist, allerdings in N\u00fcrnberg. Es handelt sich um das Modell CX21, welches inkl. Backup im Monat ziemlich genau 7,00 \u20ac kostet.",
    "weblink": "http://kellerkompanie.com/forum/viewtopic.php?f=3&t=914&sid=1e34811f0b36934eaec50cc4dd0f6865",
    "timestamp": 1552738200000.0
}
```