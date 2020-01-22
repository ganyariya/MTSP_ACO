from collections import defaultdict


class Solver:

    def __init__(self, rho=0.03, q=1, top=None):
        self.rho = rho
        self.q = q
        self.top = top

    def solve(self, *args, **kwargs):
        best = None
        for solution in self.optimize(*args, **kwargs):
            if best is None:
                best = solution
            elif sum([s.cost for s in best]) > sum([s.cost for s in solution]):
                best = solution
        return best

    def optimize(self, graph, colony, sales, start=1, gen_size=None, limit=50, opt2=None):
        gen_size = gen_size or len(graph.nodes)
        ants = colony.get_ants(gen_size)

        for u, v in graph.edges:
            weight = graph.edges[u, v]['weight']
            if weight == 0:
                weight = 1e100
            graph.edges[u, v].setdefault('pheromone', 1 / weight)

        for _ in range(limit):
            sales_solutions = self.find_solutions(graph, ants, sales, start, opt2)
            for solutions in sales_solutions:
                solutions.sort()
            sales_solutions.sort(key=lambda x: sum([y.cost for y in x]))
            self.global_update(sales_solutions, graph)

            yield sales_solutions[0]

    def find_solutions(self, graph, ants, sales, start, opt2):
        return [ant.tour(graph, sales, start, opt2) for ant in ants]

    def global_update(self, sales_solutions, graph):
        next_pheromones = defaultdict(float)
        for solutions in sales_solutions:
            cost = sum([solution.cost for solution in solutions])
            for solution in solutions:
                for path in solution:
                    next_pheromones[path] += 1 / cost

        for edge in graph.edges:
            p = graph.edges[edge]['pheromone']
            graph.edges[edge]['pheromone'] = p * (1 - self.rho) + next_pheromones[edge]
