import pygame, sys, random, math

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def Text(pos, text, color):
    font = pygame.font.Font('freesansbold.ttf', 12)
    text = font.render(text, True, color)
    rect = text.get_rect()
    rect.center = pos
    screen.blit(text, rect)

class Neuron:
    def __init__(self, inputs ,activationFunction):
        self.weights = [random.random() for i in range(inputs)]
        self.activationFunction = activationFunction
        self.bias = random.random()
        self.ouput = None
        self.gradient = None

    def feedForward(self, inputs):
        #print(zip(self.weights, inputs))
        #print(tuple(zip(self.weights, inputs)))
        #print(inputs)
        weightedSum = sum(w * i for w, i in tuple(zip(self.weights, inputs))) + self.bias
        self.output = self.activationFunction(weightedSum)
        return self.output
    
class Layer:
    def __init__(self, neurons, ipn, activationFunction=lambda x:x):
        self.neurons = [Neuron(ipn, activationFunction) for i in range(neurons)]

    def feedForward(self, inputs):
        for neuron in self.neurons:
            neuron.feedForward(inputs)
        a = lambda x:x.output
        return [a(neuron) for neuron in self.neurons]

class Network:
    def __init__(self, layerSizes, activationFunctions):
        self.layers = [Layer(layerSizes[i+1],layerSizes[i],activationFunctions[i]) for i in range(len(layerSizes)-1)]

    def feedForward(self, input):
        for layer in self.layers:
            input = layer.feedForward(input)

    def output(self):
        return [neuron.output for neuron in self.layers[len(self.layers)-1]]

    def cost(self, expectedOutput):
        cost = 0
        for neuron in self.layers[len(self.layers)-1]:
            cost += ((neuron.output)-(expectedOutput[self.layers[len(self.layers)].index(neuron)]))**2
        print("\n")
        return cost

    def Draw(self, input):
        numInputs = len(self.layers[0].neurons[0].weights)
        for i in range(numInputs):
            x = 20
            y = 20+((HEIGHT-40)*((i+.5)/(numInputs)))
            pygame.draw.circle(screen,(255,255,255),(x, y),15)
            Text((x,y),str(round(input[i],2)),(0,0,0))
        for layer in self.layers:
            for neuron in layer.neurons:
                x = 20+((self.layers.index(layer)+1)*(WIDTH-40)/len(self.layers))
                y = 20+((layer.neurons.index(neuron)+.5)*(HEIGHT-40)/len(layer.neurons))
                pygame.draw.circle(screen,(255,255,255),(x, y),15)
                Text((x,y),str(round(neuron.output,2)),(0,0,0))

class Dataset:
    def  __init__(self, path):
        with open(path, "r") as data:
            content = data.read()
        content = content.split("\n")
        newContent = []
        for line in content:
            newContent.append(line.split(","))
        newContent.remove(newContent[0])
        content = []
        for line in newContent:
            newLine = []
            for val in line:
                val = float(val)
                newLine.append(val)
            content.append(newLine)
        self.data = content
data = Dataset("diabetes.csv")

ReLU = lambda x:max(0,x)
sigmoid = lambda x:1/(1+math.exp(-x))
noFunc = lambda x:x
swish = lambda x:sigmoid(x)*x
numInputs = 8
network = Network((numInputs,5,4,1),(swish,swish,sigmoid))
input = random.choice(data.data)
print(input)
network.feedForward(input)
print(network.cost(input[numInputs-1]))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((8,8,25))
    network.Draw(input)

    pygame.display.update()
    clock.tick(60)