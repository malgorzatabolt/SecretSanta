import random


class Mixer:
    def __init__(self, participants):
        self.participants = participants
        self.draw_id = []
        self.shuffled_participant = []

    def mix_and_pick(self):
        for i in range(len(self.participants)):
            while True:
                random_id = random.randint(1, len(self.participants))
                if random_id != i+1 and random_id not in self.draw_id:
                    self.draw_id.append(random_id)
                    break
            i += 1
        for picked_id in self.draw_id:
            self.shuffled_participant.append(self.participants[picked_id-1])
        return self.shuffled_participant

