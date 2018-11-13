class StepOrPhase:
    # again, awkward creation of object
    # XXX seems like we need to collect these into a "game" object or so
    # ^ XXX HOWEVER, don't assume game should inherit the other methods!!
    def __init__(self):
        # So far this is hard set, can it be better?
        self.index = 0

# DONT JUST SET. THINK ABOUT WHAT YOURE DOING! SAY SET SPECIFIC INDEX OR SO