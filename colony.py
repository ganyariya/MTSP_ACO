from ant import Ant


class Colony:
    def __init__(self, alpha=1, beta=3):
        self.alpha = alpha
        self.beta = beta

    def get_ants(self, size):
        return [Ant(self.alpha, self.beta) for i in range(size)]
