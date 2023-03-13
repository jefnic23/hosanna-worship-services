import os


class Liturgy():
    '''Loads and stores the liturgy.'''

    def __init__(self):
        if os.path.exists('liturgy/confession.txt'):
            self.confession = open('liturgy/confession.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/greeting.txt'):
            self.greeting = open('liturgy/greeting.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/kyrie.txt'):
            self.kyrie = open('liturgy/kyrie.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/creed.txt'):
            self.creed = open('liturgy/creed.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/dialogue.txt'):
            self.dialogue = open('liturgy/dialogue.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/holy-holy-holy.txt'):
            self.hosanna = open('liturgy/holy-holy-holy.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/communion-dialogue.txt'):
            self.communion_dialogue = open('liturgy/communion-dialogue.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/lords-prayer.txt'):
            self.lords_prayer = open('liturgy/lords-prayer.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/communion-hymn.txt'):
            self.communion_hymn = open('liturgy/communion-hymn.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/gospel-acclamation.txt'):
            self.gospel_acclamation = open('liturgy/gospel-acclamation.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/prayer-after-communion.txt'):
            self.prayer_after_communion = open('liturgy/prayer-after-communion.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/benediction.txt'):
            self.benediction = open('liturgy/benediction.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/dismissal.txt'):
            self.dismissal = open('liturgy/dismissal.txt', 'r', encoding='utf-8').read()
