import re

import fastfeedparser

TITLE = "L’Étreinte des Ombres"


def last_castopod():
    feed = fastfeedparser.parse("https://radio.oblivion.city/@FantasticRolls/feed.xml")
    episodes = [e for e in feed.entries if e.title.startswith(TITLE)]
    return episodes[-1].id if episodes else None


def last_youtube():
    feed = fastfeedparser.parse(
        "https://www.youtube.com/feeds/videos.xml?channel_id=UCzlNDwukhzL9Q6OTTiBl1_Q&key=PLxC6HqP9bTs0VlgWLUs1SSMBEbctB62yn"
    )
    episodes = [e for e in feed.entries if e.title.startswith(TITLE)]
    if not episodes:
        return None
    return episodes[0].id.split(":")[-1]


variables = {"CASTOPOD_URL": last_castopod, "YOUTUBE_URL": last_youtube}
regex = re.compile(r"{{(.*)}}")
with open("index.in.html", encoding="utf8") as input:
    with open("index.html", "w", encoding="utf8") as output:
        for line in input.readlines():
            match = regex.search(line)
            if match:
                variable = match.group(1)
                if variable in variables:
                    value = variables[variable]()
                    if value:
                        line = line.replace(match.group(0), value)
            output.write(line)
