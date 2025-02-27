from time import sleep
from enum import Enum, auto
from threading import Thread

class NeuroError(Exception):
    def __init__(self, message):
        self.message = f"NeuroError: {message}"

class Neurotransmitter(Enum):
    gaba = auto()
    glutamate = auto()
    acetylcholine = auto()

class Dendrite():
    def __init__(self, neuroreciever_type, size):
        self.neuroreciever_type = neuroreciever_type
        self.neuron_or_body_part = None
        self.size = size
        self.value = 0

    def recieve(self, neurotransmitter):
        if self.neuroreciever_type != neurotransmitter:
            return

        match neurotransmitter:
            case Neurotransmitter.gaba:
                self.value = -self.size

            case Neurotransmitter.glutamate:
                self.value = self.size
            
            case Neurotransmitter.acetylcholine:
                if isinstance(self.neuron_or_body_part, BodyPart):
                    self.value = self.size
    
    def reset(self):
        self.value = 0

class Neuron():
    def __init__(self, dendrites, axon, threshold, neurotransmitter):
        self.axon = axon
        self.dendrites = dendrites
        self.threshold = threshold

        for dendrite in dendrites:
            dendrite.neuron_or_body_part = self

        self.thread = Thread(target=self.sum_and_spike_if_nec, args=[neurotransmitter])

        self.thread.start()

    def send(self, neurotransmitter):
        self.axon.recieve(neurotransmitter)

    def sum_and_spike_if_nec(self, neurotransmitter):
        while True:
            sum_of_dendrites = sum([x.value for x in self.dendrites])
            if sum_of_dendrites >= self.threshold:
                self.send(neurotransmitter)

            for dendrite in self.dendrites:
                dendrite.reset()

            sleep(0.1)

    def __getitem__(self, i):
        return self.dendrites[i]
    
class BodyPart():
    def __init__(self, dendrites, threshold, function_to_exec):
        self.function_to_exec = function_to_exec
        self.dendrites = dendrites
        self.threshold = threshold

        for dendrite in dendrites:
            dendrite.neuron_or_body_part = self
            if dendrite.neuroreciever_type != Neurotransmitter.acetylcholine:
                raise NeuroError("All the Dendrites in a BodyPart must be acetylcholine.")

        self.thread = Thread(target=self.sum_and_exec_if_nec)

        self.thread.start()

    def sum_and_exec_if_nec(self):
        while True:
            sum_of_dendrites = sum([x.value for x in self.dendrites])
            if sum_of_dendrites >= self.threshold:
                self.function_to_exec()

            for dendrite in self.dendrites:
                dendrite.reset()

            sleep(0.1)
            

    def __getitem__(self, i):
        return self.dendrites[i]