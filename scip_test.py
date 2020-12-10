import logging
from pyscipopt import Model
import warnings

warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('in module %(name)s, in func %(funcName)s, '
                              '%(levelname)-8s: [%(filename)s:%(lineno)d] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
if not len(logger.handlers):
    logger.addHandler(stream_handler)
    logger.propagate = False


class MinIIS:
    def __init__(self, model: Model):
        self.model = model

    def iterate(self):
        constraint_infeasible = list()
        cons_rng = range(len(self.model.getConss()))
        for i in cons_rng:
            m = Model(sourceModel=self.model)
            constraints = m.getConss()
            cons = constraints[i]
            cons_name = cons.name
            logger.info(f'inter # {i} for name = {cons_name}')
            m.delCons(cons)
            m.hideOutput()
            m.presolve()
            if m.getStatus() == 'optimal':
                constraint_infeasible.append(cons_name)
        return constraint_infeasible


def opt():
    model = Model("Example")
    x = model.addVar("x")
    y = model.addVar("y", vtype="INTEGER")
    model.setObjective(x + y)
    model.addCons(x <= -5, 'c0_infeas')
    # model.addCons(y <= -5, 'c1_infeas')
    model.addCons(y <= 10, 'c2')
    model.addCons(x <= 10, 'c3')
    model.addCons(2 * x - y * y >= 0, 'c4')
    model.addCons(2 * x - y >= 0, 'c5')

    res = MinIIS(model=model).iterate()
    print(res)


if __name__ == '__main__':
    opt()
