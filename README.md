# Neural Simulation System

This project simulates how neurons communicate in the brain using Python. It helps understand how signals travel between neurons and trigger actions, similar to how our nervous system works.

## What This Project Does
This project includes several components that mimic the brain's functioning:

- **Neurons**: These act as messengers, receiving signals and deciding whether to send them forward.
- **Dendrites**: These are the input parts of neurons. They collect signals and pass them to the neuron.
- **Neurotransmitters**: These are the chemical signals used for communication between neurons.
- **Body Parts**: These represent the output. If they receive a strong enough signal, they perform an action.
- **Multithreading**: The program runs continuously to simulate real-time neural activity.

---

## Breaking Down Each Component

### **Neurotransmitters**
These are chemical messengers that neurons use to communicate. In this project, we define three types:
- `gaba` (inhibitory, reduces activity)
- `glutamate` (excitatory, increases activity)
- `acetylcholine` (triggers body part movement)

We define these using an `Enum`:
```python
from enum import Enum, auto

class Neurotransmitter(Enum):
    gaba = auto()
    glutamate = auto()
    acetylcholine = auto()
```

---

### **Dendrites (Signal Receivers)**
Dendrites receive signals in the form of neurotransmitters. Each dendrite has:
- A type (`neuroreciever_type`) that specifies which neurotransmitter it can accept.
- A `size` that determines the signal strength.
- A `value` that stores the received signal.
- A `recieve` method to process neurotransmitters.
- A `reset` method to clear the signal after processing.

Example:
```python
d = Dendrite(Neurotransmitter.glutamate, size=10)
```
This creates a dendrite that can receive glutamate signals with a size of 10.

---

### **Neurons (Signal Processors)**
Neurons receive signals from dendrites and decide whether to pass them forward. Each neuron:
- Has a list of `dendrites` connected to it.
- Has an `axon`, which is where the processed signal is sent.
- Has a `threshold`, which is the minimum total signal needed to activate.
- Runs a loop in a separate thread to continuously check the total signal.

Example:
```python
n = Neuron([d], axon=d, threshold=10, neurotransmitter=Neurotransmitter.glutamate)
```
This neuron:
- Receives input from the dendrite `d`
- Has an axon connected to another dendrite
- Activates if the total signal reaches 10

The `sum_and_spike_if_nec` method:
- Adds up signals from all dendrites.
- If the sum reaches the threshold, it sends the signal forward.
- Then resets all dendrites.

---

### **Body Parts (Output System)**
Body parts are the final step. If they receive enough signal, they perform an action. Each body part:
- Has dendrites that can only receive `acetylcholine`.
- Has a `threshold` that determines when it activates.
- Executes a function when activated.

Example:
```python
def move():
    print("Muscle contraction!")

b = BodyPart([d], threshold=10, function_to_exec=move)
```
This body part:
- Receives signals from `d`
- Activates when the signal reaches 10
- Executes `move()`, which prints "Muscle contraction!"

---

## **How It All Works Together**
1. A dendrite receives a neurotransmitter signal.
2. The neuron sums up the signals from its dendrites.
3. If the total signal reaches the threshold, the neuron sends it forward.
4. If the signal reaches a body part, it performs an action.
5. The process repeats in a loop to simulate real-time neural communication.

### **Example Simulation**
```python
d.recieve(Neurotransmitter.glutamate)
```
This sends a glutamate signal to the dendrite. If it reaches the neuron’s threshold, the neuron passes it forward, and if a body part is connected, it executes its action.

---

## **Error Handling**
- If a body part receives a non-acetylcholine neurotransmitter, an error (`NeuroError`) is raised to prevent incorrect activation.

```python
class NeuroError(Exception):
    def __init__(self, message):
        self.message = f"NeuroError: {message}"
```

---

## **Contributing**
This project is open for improvements! Feel free to add features, optimize code, or report issues.

## **License**
This project is open-source and free to use under the MIT License.