import random

def random_range(start, stop, step):
    steps = int((stop - start) / step)
    return start + step * random.randint(0, steps)

class RandomSearch:
    def __init__(self, search_space, n_iterations, target_metric, screener_class, **screener_args):
        self.search_space = search_space
        self.n_iterations = n_iterations
        self.target_metric = target_metric
        self.screener_class = screener_class
        self.screener_args = screener_args

    def _generate_random_hyperparameters(self):
        return {
            key: random_range(start, stop + step, step)
            for key, (start, stop, step) in self.search_space.items()
        }

    def run(self):
        best_result = None
        best_hyperparameters = None

        for i in range(self.n_iterations):
            hyperparameters = self._generate_random_hyperparameters()

            screener = self.screener_class(**self.screener_args, hyperparameters=hyperparameters)
            
            result = screener.run()

            if best_result is None or result[self.target_metric].sum() > best_result[self.target_metric].sum():
                best_result = result
                best_hyperparameters = hyperparameters

            print(f"Iteration {i+1}/{self.n_iterations}: Best result - {best_result.head(1)['id'].iloc[0]}")
    
        return best_result, best_hyperparameters