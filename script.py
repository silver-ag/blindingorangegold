import math
import random

def scriptdata():
    data = {}
    yield C("here is wisdom: people suffer because they did something to deserve it.")
    yield C("here is foolishness:")
    yield C(" ")
    settings = {"clearer font": False, "low intensity effects": False, "effects off": False, "volume": 0.05, "outside": False}
    while True:
        x = yield C(["start game", "accessibility settings", "quit"], bg="titlescreen", pxgetter=pixel_getter_passthrough)
        if x == 0:
            break
        elif x == 1:
            x = yield C([f"clearer font: {settings['clearer font']}", f"low intensity effects: {settings['low intensity effects']}", f"effects off: {settings['effects off']}", "volume up", "volume down", "back"])
            while True:
                if x == 0:
                    settings["clearer font"] = not settings["clearer font"]
                elif x == 1:
                    settings["low intensity effects"] = not settings["low intensity effects"]
                elif x == 2:
                    settings["effects off"] = not settings["effects off"]
                elif x == 3:
                    settings["volume"] += 0.025
                elif x == 4:
                    settings["volume"] -= 0.025
                else:
                    break
                x = yield C([f"clearer font: {settings['clearer font']}", f"low intensity effects: {settings['low intensity effects']}", f"effects off: {settings['effects off']}", "volume up", "volume down", "back"], settings=settings)
        elif x == 2:
            exit()
    answered = 0
    yield C("what's your name?", pig_a, "interviewroom", "pigA_default", pixel_getter_warpone)
    x = yield C(["theophila.", "..."])
    if x == 0:
        answered += 1
        yield C("good to meet you, theophila. i'm david")
    else:
        yield C("look, i don't want you to think of me as The Police. just think of me as david.")
    yield C("now, would you like to tell me what you were doing?")
    x = yield C(["art.", "..."])
    if x == 0:
        answered += 1
        yield C("that's fine, but we've got to respect people's property when we're trying to, express ourselves.")
        yield C("\"here is wisdom: each person ought to be free to the extent that doesn't touch another.\"")
        yield C("i mean, i understand that you're trying to say something, but how would you feel if i came and wrote on your house?", fg="pigA_nice")
        x = yield C(["fine, really.", "..."])
        if x == 0:
            answered += 1
            yield C("maybe you would, but a lot of people wouldn't, and we have to respect that.")
            yield C("i mean, it's pretty disturbing stuff. \"hate hate hate...\"", fg="pigA_default")
            yield C("you must understand that would upset most people?")
            x = yield C(["sure, that's the point. art should hurt the people you do it to.", "..."])
            if x == 0:
                answered += 1
        else:
            yield C("well?", fg="pigA_default")
            yield C("look, i'd love to sit here all day, but i've got a responsibility to go out and keep people safe.")
            yield C("do you understand that you've committed a crime?")
            x = yield C(["yes.", "no.", "..."])
            if x == 0:
                answered += 2
            elif x == 1:
                answered += 1
    else:
        yield C("well?")
        yield C("look, i'd love to sit here all day, but i've got a responsibility to go out and keep people safe.")
        yield C("do you understand that you've committed a crime?")
        x = yield C(["yes.", "no.", "..."])
        if x == 0:
            answered += 3
        elif x == 1:
            answered += 1
    yield C("alright, what i'm going to do is this.")
    yield C("you can go back to the cells now, and have a think about what's happened here.")
    yield C("we'll finish up the paperwork, and we'll decide whether we're going to charge you.")
    data["will be charged"] = (answered >= 3)

    yield C(" ", blank, bg="cell", fg="transparent")
    yield C()
    yield C("idolators! you wear the symbol and forgot what it pointed towards!", voice)
    yield C("get in there!", pig_b)
    yield C("(bang, the door - the cell next door)", blank)
    yield C("do you think you're serving god? sin punished is doubled! god doesn't punish, sin is that which seperates the sinner from the star of infinity!", voice)
    yield C(" ", blank)
    yield C("fuck.", voice)
    yield C("(knock knock on the wall)", blank)
    yield C("how about you, you holding up okay?", voice)
    x = yield C(["yeah, okay.", "not really.", "..."])
    if x == 0:
        yield C("good, don't let the cunts get to you.")
        yield C("move as the spirit moves you, like they say.")
        x = yield C(["yeah, definitely", "what do you mean?"])
        if x == 1:
            yield C("the quakers - \"as the spirit moves you\".")
            yield C("when you look towards infinity and open your heart, the spirit of guidance that enters you.")
        yield C("i'm a grandfather, you know.")
        yield C("that's why i'm here.")
    elif x == 1:
        yield C("right answer. never forget that.")
        yield C("do you pray?")
        x = yield C(["yes.", "no, i prefer to act."])
        if x == 0:
            yield C("good. love is the only really effective motivator, it's good that you have access to it for the things you'll need to do.")
        else:
            yield C("that's a good sentiment in the sense that i think you're understanding it, but the prayer i'm talking about isn't asking god to solve your problems.")
            yield C("it's not in words.")
            yield C("it's about burning yourself up with the fire of absolute perception.")
            yield C("that's what i do when i'm afraid.")
    elif x == 2:
        yield C("hello? there is someone in there right?")
        yield C(" ")
    yield C(" ")
    yield C(speaker=blank, fg="pigB")
    yield C("Come with me.", pig_b)
    if data["will be charged"]:
        yield C("We're going to be charging you with criminal damage.")
        yield C("We'll let you go for now, but you'll receive a court summons by post.")
        yield C("Do you understand what the consequences will be if you don't attend the court date we give you?")
        x = yield C(["yes.", "no.", "..."])
        if x == 0:
            yield C("good.")
        else:
            yield C("you could be imprisoned for up to a year.")
            yield C("so make sure you attend, we wouldn't want that.")
            yield C("you may not understand it now, but we care about your safety. we want you to live in a safe and lawful society.")
    else:
        yield C("We're going to give you the benefit of the doubt this time.")
        yield C("We'll let you go, but if we see you again it'll be a lot more serious.")
    yield C(" ", blank, bg="outside_copshop", pxgetter = pixel_getter_warptwo)
    settings["outside"] = True
    yield C(" ", fg="transparent", settings=settings)
    x = yield C(["(into the police station)", "(home)"])
    if x == 0:
        settings["outside"] = False
        yield C(" ", bg="copshop_frontdesk", settings=settings, pxgetter = pixel_getter_warpone)
        yield C("my friend's being held here. when will he be released?", blank)
        yield C("i'm afraid i can't give out that information.", pig_c)
        settings["outside"] = True
        yield C(" ", blank, bg="outside_copshop", pxgetter=pixel_getter_warptwo, settings=settings)
        yield C(["(home)"])
    yield C(" ", blank, bg="town")
    yield C(fg="protest")
    yield C("here is wisdom: there is a higher moral law which the law should reflect.", protesters)
    yield C("but the reflection is cracked and must be repaired!")
    x = yield C(["(take a leaflet)", "(home)"], blank)
    if x == 0:
        data["took leaflet"] = True
        yield C("\"brighter sign collective\nopen meeting tuesday the 11th\"")
    else:
        data["took leaflet"] = False
    settings["outside"] = False
    yield C(" ", bg="home", fg="transparent", pxgetter=pixel_getter_warpone, settings=settings)
    yield C(["(collapse)"])
    yield C("...", bg="black")
    yield C()
    yield C(" ", bg="home")
    x = yield C(["(town)", "(church)"] + (["(brighter sign meeting)"] if data["took leaflet"] else []))
    if x == 0:
        settings["outside"] = True
        yield C(" ", bg="town", pxgetter=pixel_getter_warptwo, settings=settings)
        yield C()
        yield C(bg="wall_clean")
        yield C(["(pain must be heard, the bright piercing whisper)"])
        yield C(" ", bg="wall_graffiti")
        yield C("cool.", ultraviolate)
        yield C(["thanks."])
        yield C("i think i know what you mean. the transcendent absolute can't be named or described, only seen.", fg="ultraviolate")
        x = yield C(["yeah!", "something like that. it's right there, and there's a moral obligation, because like - things have to die to be reborn?"])
        if x == 0:
            yield C("i'm glad someone understands.")
        else:
            yield C("mmm, that makes sense.")
        ultraviolate[0] = "ULTRA-VIOLATE"
        yield C("i'm called ULTRA-VIOLATE.")
        yield C(["theophila."])
        yield C("good to meet you! hopefully i'll see you around.")
        data["person met"] = "ultraviolate"
    elif x == 1:
        settings["outside"] = True
        yield C(" ", bg="church_outside", pxgetter=pixel_getter_warptwo, settings = settings)
        yield C()
        settings["outside"] = False
        yield C(" ", bg="church_inside", fg="congregation", pxgetter=pixel_getter_warpone, settings = settings)
        yield C("here is wisdom: god is the king of kings.", preacher)
        yield C("we follow the law of the land, how much more so should we follow the law of heaven?")
        yield C("please, pray these words with me:")
        yield C("@@@@@@@  @@@@@@@@@  @  @@@@@@@@@  @@@  @@@@@  @@@  @@@@@@@@@@@@@  @@  @@@@@@@@@  @@  @@@@@  @@@@  @@@@  @@@@@@@@@@  @@@@  @@@  @@@  @@  @@@@@@@@@@")
        yield C("hi, are you new here?", aster, fg="aster")
        yield C(["yes."])
        yield C("i thought so. don't worry, not all the preachers are as boring as michael.")
        yield C("you should come down on thursday when julia is in.")
        yield C("still, sometimes listening to him i think that church is just where people who've never heard the voice of god in their heart go to commiserate.")
        x = yield C(["i'm theophila", "..."])
        if x == 0:
            aster[0] = "Aster"
            yield C("aster. i hope i'll see you around!")
        else:
            yield C("well, i hope you'll be back again.")
        data["person met"] = "aster"
    else:
        yield C(" ", bg="meeting_hall", fg="meeting_people")
        tom[0] = "Tom"
        yield C("alright everyone, it's good to see you.", tom)
        yield C("well done on the protest yesterday, it was very powerful to see so many people standing up to the failures of the system.")
        yield C("and that's something that we really need. more and more, the processes of our government are excluding empathy.")
        yield C("it's crucial that our social systems should be build on the empathic connection natural to every one of us. it's only by understanding how someone feels that we can treat them with respect.")
        yield C("respect which is sorely lacking in the way our government treats people today. so thank you all for coming.")
        yield C("for newcomers, newspapers are available for a two pound donation on the corner table.")
        yield C("heya, i don't think i've seen you before?", mary, fg="mary")
        yield C(["no, i don't think so."])
        mary[0] = "Mary"
        yield C("i'm mary.")
        yield C(["theophila."])
        yield C("what did you think about what tom was saying?")
        x = yield C(["pretty cool.", "i didn't find it very convincing to be honest."])
        if x == 0:
            yield C("nice, i hope i'll see you at the next one then.")
        else:
            yield C("yeah, i can't stand when people talk about how \"powerful\" a protest was when it was just standing around with snarky placards.")
        data["person met"] = "mary"
    settings["outside"] = False
    yield C(" ", blank, bg="home", fg="transparent", pxgetter=pixel_getter_warpone, settings=settings)
    yield C(["(collapse)"])
    yield C("...", bg="black")
    yield C("(\"i'm falling through the cold cloudless sky of desperation, no ground to stand on. i'm worthless, i need you, i'll say anything, i'll do anything, i'm so scared...\")")
    yield C("(you're empty and scared? you think i'm not? you think i'm not scared all the time of not being good enough, of not being real?)")
    yield C("(i just don't make it other people's problem! i can't collapse like you and force someone else to take care of me!)")
    yield C("(i'm sorry, it's not your fault. it's going to be okay.)")
    yield C("(i envy you, dying like lot's wife. crying salt tears until nothing else is left.)")
    yield C(" ", bg="home")
    if data["will be charged"]:
        yield C("(you've got mail)")
        yield C("\"COURT SUMMONS\nyou are hereby ordered to present yourself to the magistrates court on goldsmith's road on friday the fourth of october at 9:40 AM.\"")
    yield C(" ")
    settings["outside"] = True
    yield C(bg="town", settings=settings)
    yield C("...")
    yield C("(what's that noise?)")
    yield C(" ", bg="outside_copshop", fg="protest")
    yield C("police must take better care of people in their custody!", protesters)
    yield C(["what happened?"])
    yield C("some old guy died in custody yesterday. they're saying he climbed up on the desk in reception and fell.", tom)
    yield C("((()))", blank, pxgetter = pixel_getter_warpthree)
    yield C("-()-")
    yield C(["stagnant self-annihilating ghouls! they were looking right along the road to the edge of heaven and spat blood on it! infinitely distant material emanation really means something, huh..."])
    yield C(random.choice(challenging_prayers))
    yield C(["(screaming, shouting, bleeding, dissolving)"])
    yield C("i know it's upsetting, but we need to be orderly about this.", tom)
    yield C("\"here is wisdom: justice comes slowly.\"")
    yield C("alright, stay calm. there's no need for any of that.", pig_b, fg="pigB")
    yield C(["you manichaen precipitate! why, this is hell, nor am i out of it!"])
    yield C(["(spit)"])
    yield C("right, you're under arrest.", pig_b)
    yield C("don't resist, violence will only make it worse.", tom)
    if data["person met"] == "aster" or (data["person met"] == "ultraviolate" and random.choice([True,False])):
        yield C(f"({aster[0].lower()} shoves between you and the cop.)", blank, fg="aster")
        yield C("come on, into the crowd.", aster)
        yield C("fuck! i just can't understand people like that.", tom)
    else:
        yield C(f"({mary[0].lower()} punches the cop in the head.)", blank, fg="mary")
        yield C("come on, into the crowd.", mary)
        yield C("fuck! i just can't understand people like that.", tom)
    settings["outside"] = False
    yield C("...", blank, bg="group_house", fg=data["person met"], settings=settings)
    yield C("how are you doing?", {"ultraviolate":ultraviolate, "mary":mary, "aster":aster}[data["person met"]])
    names = {'ultraviolate':'aster and mary', 'aster':'ULTRA-VIOLATE and mary', 'mary':'ULTRA-VIOLATE and aster'}[data['person met']]
    yield C(f"these are my friends {names}.")
    ultraviolate[0] = "ULTRA-VIOLATE"
    aster[0] = "Aster"
    mary[0] = "Mary"
    if data["person met"] != "ultraviolate":
        yield C("hello.", ultraviolate, fg="ultraviolate")
    if data["person met"] != "aster":
        yield C("hey.", aster, fg="aster")
    if data["person met"] != "mary":
        yield C("hi.", mary, fg="mary")
    yield C("let's get something to eat.", ultraviolate, fg="ultraviolate")
    x = yield C(["how could they not understand?", "why is motion so difficult?", "who sits on the throne of the world?"])
    if x == 0:
        yield C("i think it's fear. it's understandable, some of it.")
        yield C("and it means taking responsibility. \"blessed are the terrible, for they are capable of good on a scale inaccessible to those convinced of their own virtue\".", mary, fg="mary")
        yield C("but there's always those who had no choice in knowing. you can come to the people who were taught by force.")
        yield C(["but i'm not one of them."])
        yield C(" ", blank)
    elif x == 1:
        yield C("i don't know. i'm sorry.")
        yield C("i think maybe it couldn't be easy. you can't be in the habit of breaking habits.", mary, fg="mary")
        yield C("but it seems to come naturally to some people.")
        yield C("at least death and rebirth is possible.")
    else:
        yield C("the throne is empty, god wouldn't stoop to it, and who else could reach up to it?")
        yield C("anyway, even if it was occupied, the king could be thrown down. that's what you do, with kings. it's part of what they mean.", aster, fg="aster")
        yield C("there is no rule that (provably) has no exception. when the monster's wings block out the sky, the star of infinity must always shine through somewhere.")
        yield C("that's why the world is cursed. certainty is impossible. the axiom has feet of clay. freedom, ironically, is not optional.")
    yield C("shall we pray together?", ultraviolate, fg="ultraviolate")
    prayers = sorted(random.sample(challenging_prayers, 5), key=lambda a: random.randint(0,5))
    yield C(prayers[0], blank)
    yield C(prayers[1], fg="aster")
    yield C(prayers[2], fg="mary")
    settings["outside"] = True
    yield C(prayers[3], bg="outside_copshop", settings=settings)
    yield C(prayers[4], fg="transparent")
    prayers = sorted(random.sample(consolation_prayers, 4), key=lambda a: random.randint(0,5))
    yield C(prayers[0], bg="burning_copshop")
    yield C(prayers[1])
    yield C(prayers[2])
    yield C(prayers[3])
    yield C(" ")

    yield C("here is wisdom: people suffer because they did something to deserve it.", blank)
    yield C(speaker=("A%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", (210,60,50)))
    yield C(speaker=("Dazai's Curse", (210,60,50)))
    yield C(speaker=("Evil Inclination", (210,60,50)))
    yield C(speaker=("King Soulless", (210,60,50)))

    yield False

challenging_prayers = ["(the scream of infinity)",
                       ["(fall to your knees)"],
                       ["(awkward movement of a forever-dying dove)"],
                       "(a sunlight nail through your head)",
                       "(world pillar falling on you)",
                       ["(dry retching muscle twist and rip open)"],
                       "(the rain-that-falls demands action)",
                       "(alice is in your skin, sick with reality)",
                       "(there's a bundle of razorblades in your throat that you're trying to speak)",
                      ]

consolation_prayers = ["(light, light, light, light, light, light, light, light, light, light, light)",
                       "(held in the centre of a crystal sphere; the sky)",
                       ["(kiss the ground)"],
                       "(blinding light at the heart of creation, and seas of crashing bronze)",
                       "(the teleological extension of glory; the schematic abstraction of love)",
                       "(the sap is rising. it is a season of fire)",
                       ["(stare at the sun)"],
                       ["(drink the water that pours from heaven)"],
                       "(harmonic echo of the moment of creation - this moment)",
                      ]

def prayscriptdata():
    yield C()
    yield C(" ", blank, pxgetter=pixel_getter_prayer)
    for line in sorted(random.sample(challenging_prayers, 3), key=lambda a: random.randint(0,5)):
        yield C(line)
    for line in sorted(random.sample(consolation_prayers, 2), key=lambda a: random.randint(0,5)):
        yield C(line)
    yield False

def C(dialogue = False, speaker = False, bg = False, fg = False, pxgetter = False, settings = False):
    # C for Changes
    return (dialogue, speaker, ("assets/" + bg + ".png") if bg else False, ("assets/" + fg + ".png") if fg else False, pxgetter, settings)

blank = ("", (255,255,255))
pig_a = ("Pig A", (200,200,150))
pig_b = ("Pig B", (200,200,150))
pig_c = ("Pig C", (200,200,150))
voice = ("Voice", (200,100,200))
protesters = ("Protesters", (100,200,255))
preacher = ("Preacher", (100,200,130))
tom = ["Protester In High-Vis", (255,100,150)]
aster = ["Stranger", (120, 140, 160)]
mary = ["Stranger", (160, 120, 140)]
ultraviolate = ["Stranger", (140, 160, 120)]

def pixel_getter_passthrough(x, y, background, foreground, params):
    bg_px = background.get_at((int((x/640) * background.get_rect()[2]), int((y/640) * background.get_rect()[3])))
    fg_px = foreground.get_at((int((x/640) * foreground.get_rect()[2]), int((y/640) * foreground.get_rect()[3])))
    fg_a = fg_px[3]
    bg_r = bg_px[0]/256
    bg_g = bg_px[1]/256
    bg_b = bg_px[2]/256
    fg_r = fg_px[0]/256
    fg_g = fg_px[1]/256
    fg_b = fg_px[2]/256
    return (int((bg_r * (255-fg_a)) + (fg_r * fg_a)), int((bg_g * (255-fg_a)) + (fg_g * fg_a)), int((bg_b * (255-fg_a)) + (fg_b * fg_a)), 255)

def pixel_getter_warpone(x, y, background, foreground, params):
    bg_px = background.get_at((int((((x+(params[0]*10))%640)/640) * background.get_rect()[2]), int((y/640) * background.get_rect()[3])))
    fg_px = foreground.get_at((int((((x+(params[1]*10))%640)/640) * foreground.get_rect()[2]), int((y/640) * foreground.get_rect()[3])))
    fg_a = fg_px[3]
    bg_r = bg_px[0]/256
    bg_g = bg_px[1]/256
    bg_b = (bg_px[2] + (params[2]*30))/256
    fg_r = (fg_px[0] + (params[2]*30))/256
    fg_g = fg_px[1]/256
    fg_b = fg_px[2]/256
    return (int((bg_r * (255-fg_a)) + (fg_r * fg_a)) % 256, int((bg_g * (255-fg_a)) + (fg_g * fg_a)) % 256, int((bg_b * (255-fg_a)) + (fg_b * fg_a)) % 256, 255)    

def pixel_getter_warptwo(x, y, background, foreground, params):
    bg_px = background.get_at((int((x/640) * background.get_rect()[2]), int((y/640) * background.get_rect()[3])))
    fg_px = foreground.get_at((int((((x+(math.asin((params[1]*5.34)%1)*5))%640)/640) * foreground.get_rect()[2]), int((y/640) * foreground.get_rect()[3])))
    fg_a = fg_px[3]
    bg_r = bg_px[0]/256
    bg_g = ((bg_px[1]/(params[2] if abs(params[2]) != 0 and abs(params[2]) > 0.235 else 1)))/256
    bg_b = bg_px[2]/256
    fg_r = fg_px[0]/256
    fg_g = (fg_px[1]+math.sin(params[0]*10))/256
    fg_b = fg_px[2]/256
    return (int((bg_r * (255-fg_a)) + (fg_r * fg_a)) % 256, int((bg_g * (255-fg_a)) + (fg_g * fg_a)) % 256, int((bg_b * (255-fg_a)) + (fg_b * fg_a)) % 256, 255)

def pixel_getter_warpthree(x, y, bg, fg, params):
    dist = x/(20*params[1] if params[1]!=0 else 2)
    p = (int((x/640)*bg.get_rect()[2]), int((((y+(params[0]*dist))%639)/640)*bg.get_rect()[3]))
    bg_px = bg.get_at((int((x/640)*bg.get_rect()[2]), int((((y+(params[0]*dist))%639)/640)*bg.get_rect()[3])))
    fg_px = fg.get_at((int((x/640)*fg.get_rect()[2]), int((((y+(params[0]*dist*1.1))%639)/640)*fg.get_rect()[3])))
    fg_a = fg_px[3]
    degree = ((math.sin(params[2]*13.11)+1)/2)
    bg_r = min(((bg_px[0]*degree) + (bg_px[1]*(1-degree))) + 30, 255) / 256
    bg_g = ((bg_px[1]*degree) + (bg_px[2]*(1-degree))) / 256
    bg_b = ((bg_px[2]*degree) + (bg_px[0]*(1-degree))) / 256
    fg_r = ((fg_px[0]*degree) + (fg_px[2]*(1-degree))) / 256
    fg_g = ((fg_px[1]*degree) + (fg_px[0]*(1-degree))) / 256
    fg_b = ((fg_px[2]*degree) + (fg_px[1]*(1-degree))) / 256
    return (int((bg_r * (255-fg_a)) + (fg_r * fg_a)) % 256, int((bg_g * (255-fg_a)) + (fg_g * fg_a)) % 256, int((bg_b * (255-fg_a)) + (fg_b * fg_a)) % 256, 255)

def pixel_getter_prayer(x, y, bg, fg, params):
    v = ((y/40)*math.sin((params[0]*y)+math.cos(params[1]*x)), (y/80)*math.cos((params[0]*y)+math.cos(params[1]*x)))
    bg_px = bg.get_at(((int((min(max(x+v[0],0),639)/640) * bg.get_rect()[2])), (int((min(max(y+v[1],0),639)/640) * bg.get_rect()[3]))))
    fg_px = fg.get_at(((int((min(max(x-v[1],0),639)/640) * fg.get_rect()[2])), (int((min(max(y-v[0],0),639)/640) * fg.get_rect()[3]))))
    fg_a = fg_px[3]
    bg_r = (bg_px[0]+(10*v[0]) if bg_px[0]+(10*v[0]) <= 256 else bg_px[0]-(10*v[0]))/256
    bg_g = (bg_px[1]+(10*v[1]) if bg_px[1]+(10*v[1]) <= 256 else bg_px[1]-(10*v[1]))/256
    bg_b = bg_px[2]/256
    fg_r = fg_px[0]/256
    fg_g = (fg_px[1]+(10*v[0]) if fg_px[1]+(10*v[0]) <= 256 else fg_px[1]-(10*v[0]))/256
    fg_b = (fg_px[2]+(10*v[1]) if fg_px[2]+(10*v[1]) <= 256 else fg_px[2]-(10*v[1]))/256
    return (int((bg_r * (255-fg_a)) + (fg_r * fg_a)) % 256, int((bg_g * (255-fg_a)) + (fg_g * fg_a)) % 256, int((bg_b * (255-fg_a)) + (fg_b * fg_a)) % 256, 255)
