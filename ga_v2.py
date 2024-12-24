import random
import numpy as np

class GA:
    def __init__(self, P, n):
        self.P = P
        self.n = n
        self.D_range = np.linspace(0.01,1,1000)
        self.lyambda_range = np.linspace(0.3,1.5,1000)
        self.A_range = np.linspace(10**3,10*5,1000)

    # Функция приспособленности (fitness): насколько близко решение к P = 50000
    def fitness(self, individual):
        D, lyambda, A = individual
        return abs(self.P - D ** 3 * self.n * lyambda * A)

    # Генерация начальной популяции
    def generate_population(self, size):
        pop_ar = []

        for _ in range(size):
            l = []
            l.append(random.choice(self.D_range))  # D
            l.append(random.choice(self.lyambda_range)) # lyambda
            l.append(random.choice(self.A_range))  # A

            pop_ar.append(l)

        return pop_ar


    # Селекция (выбор лучших индивидов)
    def select_population(self, population, fitness_values, num_to_select):
        selected = sorted(zip(population, fitness_values), key=lambda x: x[1])
        return [individual for individual, _ in selected[:num_to_select]]


    # Скрещивание (crossover)
    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]


    # Мутация
    def mutate(self, individual, mutation_rate=0.1):
        mut_ar = []

        # D
        if random.random() > mutation_rate:
            mut_ar.append(individual[0])
        else:
            mut_ar.append(random.choice(self.D_range))

        # lyambda
        if random.random() > mutation_rate:
            mut_ar.append(individual[1])
        else:
            mut_ar.append(random.choice(self.lyambda_range))

        # A
        if random.random() > mutation_rate:
            mut_ar.append(individual[2])
        else:
            mut_ar.append(random.choice(self.A_range))

        return mut_ar


# Основной цикл генетического алгоритма
def genetic_algorithm(ga, pop_size, generations, mutation_rate):
    population = ga.generate_population(pop_size)

    for generation in range(generations):
        fitness_values = [ga.fitness(ind) for ind in population]

        if np.min([fitness_values]) == 0:
            break

        selected = ga.select_population(population, fitness_values, pop_size // 2)

        next_generation = []
        while len(next_generation) < pop_size:
            parent1, parent2 = random.sample(selected, 2)
            offspring1, offspring2 = ga.crossover(parent1, parent2)

            next_generation.append(ga.mutate(offspring1, mutation_rate))

            if len(next_generation) < pop_size:
                next_generation.append(ga.mutate(offspring2, mutation_rate))

        population = next_generation

    # Лучшее решение
    best_individual = min(population, key=ga.fitness)
    return best_individual

P = 50000
n = 1500

ga = GA(P, n)

# Параметры алгоритма
pop_size = 100
mutation_rate = 0.1
generations = 100

solution = genetic_algorithm(ga, pop_size, generations, mutation_rate)

print("Найденное решение (D, lyambda, A):", solution)
print("Результат:", solution[0]**3*n*solution[1]*solution[2])

