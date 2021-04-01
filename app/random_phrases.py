from random import choice


class Random_Phrases:
    """Collections of random phrases deployed at various times in the application."""

    def __init__(self, phrases):
        """Creates instance using list of phrases as an input."""

        self.phrases = phrases

    def get_phrase(self, name=None):
        if name == None:
            return choice(self.phrases)
        else:
            return choice(self.phrases).replace("[NAME]", name)


login_greetings = Random_Phrases([
    "Woohoo, you're back!",
    "You're so close!",
    "... log in ... sign on ... log on ... sign in ... ¯\_(ツ)_/¯",
    "Sign in already :-)",
    "Whatchya waitin' for???",
    "Lookin' good, boo",
    "Gotta sign in to make the thing work bro..."])

new_user_greetings = Random_Phrases([
    "Howdy, new friend!",
    "We're so glad you're here!",
    "You're going to love it here!",
    "Fresh meattttt... (some of us are zombies)",
    "OMG fancy meeting you here!",
    "No day like today, baby.",
    "What a day to be alive... amiright?"
])

welcome_first_login = Random_Phrases([
    "Welcome to the platform, [NAME].",
    "Beep beep new user coming through...",
    "[NAME], we're glad you're here."
])

welcome_at_login = Random_Phrases([
    "Welcome back, [NAME].",
    "Woohoo!  You're back :-)",
    "[NAME], so glad you could make it.",
    "Well hello again, [NAME]!",
    "It's good to see you again."
])

logged_in_home = Random_Phrases([
    "You're a star, [NAME].",
    "Good day to you, [NAME].",
    "Welcome home, [NAME]!"
])

new_group_greeting = Random_Phrases([
    "We've got a new group on our hands people!",
    "A gaggle? A pod? A murder?  What type of group are we dealing with here?",
    "group: like one person, but more."
])

