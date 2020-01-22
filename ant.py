from solution import Solution
import itertools
import bisect
import random


class Ant:

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.sales = None
        self.graph = None
        self.n = None

    def tour(self, graph, sales, start, opt2):
        self.graph = graph
        self.sales = sales
        self.n = len(graph.nodes)

        solutions = [Solution(graph, start, self) for _ in range(sales)]

        # できる限り均等にセールスマンが通る
        # as possible,  salesman travels vertexes as same
        saleses = [(self.n - 1) // sales for i in range(sales)]
        for i in range((self.n - 1) % sales):
            saleses[i] += 1

        unvisited = [i for i in range(1, self.n + 1) if i != start]
        for i in range(sales):
            for j in range(saleses[i]):
                next_node = self.choose_destination(solutions[i].current, unvisited)
                solutions[i].add_node(next_node)
                unvisited.remove(next_node)
            solutions[i].close()

        if opt2:
            self.opt2_update(graph, opt2, sales, saleses, solutions)

        return solutions

    def opt2_update(self, graph, opt2, sales, saleses, solutions):
        for i in range(sales):
            for j in range(opt2):
                k = saleses[i] + 1
                while True:
                    a = random.randint(0, k - 1)
                    b = random.randint(0, k - 1)
                    if a != b:
                        break
                if a > b:
                    a, b = b, a
                dist_a = graph.edges[solutions[i].nodes[a], solutions[i].nodes[a + 1]]['weight']
                dist_b = graph.edges[solutions[i].nodes[b], solutions[i].nodes[(b + 1) % k]]['weight']
                dist_c = graph.edges[solutions[i].nodes[a], solutions[i].nodes[b]]['weight']
                dist_d = graph.edges[solutions[i].nodes[a + 1], solutions[i].nodes[(b + 1) % k]]['weight']
                if dist_a + dist_b > dist_c + dist_d:
                    solutions[i].nodes[a + 1:b + 1] = reversed(solutions[i].nodes[a + 1: b + 1])
                    solutions[i].cost += (dist_c + dist_d - dist_a - dist_b)
                    solutions[i].path = []
                    for l in range(k):
                        solutions[i].path.append((solutions[i].nodes[l], solutions[i].nodes[(l + 1) % k]))

    def choose_destination(self, current, unvisited):
        if len(unvisited) == 1:
            return unvisited[0]
        scores = self.get_scores(current, unvisited)
        return self.choose_node(unvisited, scores)

    def choose_node(self, unvisited, scores):
        total = sum(scores)
        cumdist = list(itertools.accumulate(scores))
        index = bisect.bisect(cumdist, random.random() * total)
        return unvisited[min(index, len(unvisited) - 1)]

    def get_scores(self, current, unvisited):
        scores = []
        for node in unvisited:
            edge = self.graph.edges[current, node]
            score = self.score_edge(edge)
            scores.append(score)
        return scores

    def score_edge(self, edge):
        weight = edge.get('weight', 1)
        if weight == 0:
            return 1e200
        phe = edge['pheromone']
        return phe ** self.alpha * (1 / weight) ** self.beta
