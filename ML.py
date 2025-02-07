import pygame, sys, random, math

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def Text(pos, text, color):
    font = pygame.font.Font('freesansbold.ttf', 12)
    text = font.render(str(text), True, color)
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
        self.output = self.activationFunction.function(weightedSum)
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
        #self.learningRate = learningRate

    def feedForward(self, input):
        for layer in self.layers:
            input = layer.feedForward(input)

    def output(self):
        return [neuron.output for neuron in self.layers[len(self.layers)-1]]

    def cost(self, expectedOutput):
        cost = 0
        #print(type(expectedOutput))
        if isinstance(expectedOutput, float):
            return (self.layers[len(self.layers)-1].neurons[0].output - expectedOutput) ** 2
        elif isinstance(expectedOutput, list):
            for neuron in self.layers[len(self.layers)-1].neurons:
                cost += ((neuron.output)-(expectedOutput[self.layers[len(self.layers)-1].neurons.index(neuron)]))**2
        #print("\n")
            return cost

    def backpropagate(self):
        for layer in self.layers:
            for neuron in layer.neurons:
                for weight in neuron.weights:
                    pass
                    #weight -= self.learningRate*(derivative of cost with respect to the weight)

    def Draw(self, input, cost):
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
        Text((WIDTH/2,20),f"Cost: {cost}",(255,255,255))

def Dataset(path):
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
    return content
data = Dataset("diabetes.csv")

class ActivationFunction:
    def __init__(self, function, derivative):
        self.function = function
        self.derivative = derivative

ReLU = ActivationFunction(lambda x:max(0,x), lambda x:0 if(x<=0) else 1)
sigmoid = ActivationFunction(lambda x:1/(1+math.exp(-x)), lambda x:-(((1+math.exp(-x))**-2)*(-math.exp(-x))))
noFunc = ActivationFunction(lambda x:x, lambda x:1)
#swish = lambda x:sigmoid(x)*x
numInputs = 8
network = Network((numInputs,3,1),(ReLU,sigmoid))
input = random.choice(data)
#print(input)
network.feedForward(input)
#print(network.cost(input[numInputs-1]))
cost = network.cost(input[numInputs-1])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            input = random.choice(data)
            network.feedForward(input)
            cost = network.cost(input[numInputs])

    screen.fill((8,8,25))
    #screen.fill((100,100,100))
    network.Draw(input, cost)

    pygame.display.update()
    clock.tick(60)