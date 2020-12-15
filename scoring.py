import sklearn.metrics as metrics
from sklearn.metrics.scorer import get_scorer
from itertools import product

def pr_auc_score(y_true, y_score):
    precision, recall, thresholds = \
        metrics.precision_recall_curve(y_true, y_score[:, 1])
    return metrics.auc(recall, precision, reorder=True)


def tn(y_true, y_pred):
    return metrics.confusion_matrix(y_true, y_pred)[0, 0]


def fp(y_true, y_pred):
    return metrics.confusion_matrix(y_true, y_pred)[0, 1]


def fn(y_true, y_pred):
    return metrics.confusion_matrix(y_true, y_pred)[1, 0]


def tp(y_true, y_pred):
    return metrics.confusion_matrix(y_true, y_pred)[1, 1]


def cost(y_true, y_pred, fp_cost=1, fn_cost=1):
    return fp(y_true, y_pred) * fp_cost + fn(y_true, y_pred) * fn_cost


def mean_squared_error_cost(true_value, pred_value, fp_cost=1, fn_cost=1):
    # fp is true_value=true and pred_value>0.5
    # fn is true_value=false and pred_value<0.5
    from numpy import mean
    squares = []
    for t, p in zip(true_value, pred_value):
        diff = (t - p) ** 2
        if t:
            diff *= fp_cost
        else:
            diff *= fn_cost
        squares.append(diff)
    return mean(squares)


def mse(y_true, y_pred):
    return min(metrics.mean_squared_error([1 if x else 0 for x in y_true],
                                          map(lambda x: x[0][1 if x[1] else 0], zip(y_pred, y_true))),
               metrics.mean_squared_error([1 if x else 0 for x in y_true],
                                          map(lambda x: x[0][0 if x[1] else 1], zip(y_pred, y_true))))


def mse_cost(y_true, y_pred, fp_cost=1, fn_cost=1):
    return min(mean_squared_error_cost([1 if x else 0 for x in y_true],
                                       map(lambda x: x[0][1 if x[1] else 0], zip(y_pred, y_true)),
                                       fp_cost=fp_cost, fn_cost=fn_cost),
               mean_squared_error_cost([1 if x else 0 for x in y_true],
                                       map(lambda x: x[0][0 if x[1] else 1], zip(y_pred, y_true)),
                                       fp_cost=fp_cost, fn_cost=fn_cost))


def mse1(y_true, y_pred):
    return max(metrics.mean_squared_error([1 if x else 0 for x in y_true],
                                          map(lambda x: x[0][1 if x[1] else 0], zip(y_pred, y_true))),
               metrics.mean_squared_error([1 if x else 0 for x in y_true],
                                          map(lambda x: x[0][0 if x[1] else 1], zip(y_pred, y_true))))


def mse_cost1(y_true, y_pred, fp_cost=1, fn_cost=1):
    return max(mean_squared_error_cost([1 if x else 0 for x in y_true],
                                       map(lambda x: x[0][1 if x[1] else 0], zip(y_pred, y_true)),
                                       fp_cost=fp_cost, fn_cost=fn_cost),
               mean_squared_error_cost([1 if x else 0 for x in y_true],
                                       map(lambda x: x[0][0 if x[1] else 1], zip(y_pred, y_true)),
                                       fp_cost=fp_cost, fn_cost=fn_cost))


def get_scoring():
    scoring = {}
    scoring_proba = {}
    scores_names = ['accuracy', 'adjusted_mutual_info_score', 'adjusted_rand_score', 'average_precision',
                    'completeness_score',
                    'f1', 'f1_macro', 'f1_micro', 'f1_weighted', 'fowlkes_mallows_score',
                    'homogeneity_score', 'mutual_info_score', 'neg_log_loss', 'normalized_mutual_info_score',
                    'precision',
                    'precision_macro', 'precision_micro', 'precision_weighted', 'recall',
                    'recall_macro', 'recall_micro', 'recall_weighted', 'roc_auc', 'v_measure_score']
    metrics_functions = [metrics.cohen_kappa_score, metrics.hinge_loss,
                         metrics.matthews_corrcoef, metrics.accuracy_score,
                         metrics.f1_score, metrics.hamming_loss,
                         metrics.log_loss, metrics.precision_score, metrics.recall_score,
                         metrics.zero_one_loss, metrics.average_precision_score, metrics.roc_auc_score]

    pr_auc_scorer = metrics.make_scorer(pr_auc_score, greater_is_better=True,
                                        needs_proba=True)
    scoring = {x: get_scorer(x) for x in scores_names}
    scoring.update({x.__name__: metrics.make_scorer(x) for x in metrics_functions})

    scoring["pr_auc"] = pr_auc_scorer

    scoring.update({'tp': metrics.make_scorer(tp), 'tn': metrics.make_scorer(tn),
                    'fp': metrics.make_scorer(fp), 'fn': metrics.make_scorer(fn)})

    scoring.update({"cost_{0}_{1}".format(*x): metrics.make_scorer(cost, fp_cost=x[0], fn_cost=x[1]) for x in
                    product(range(1, 4), range(1, 4))})
    scoring.update(
        {"mse_cost_{0}_{1}".format(*x): metrics.make_scorer(mse_cost, fp_cost=x[0], fn_cost=x[1], needs_proba=True) for
         x in
         product(range(1, 4), range(1, 4))})

    scoring.update(
        {"mse1_cost_{0}_{1}".format(*x): metrics.make_scorer(mse_cost1, fp_cost=x[0], fn_cost=x[1], needs_proba=True)
         for x in
         product(range(1, 4), range(1, 4))})

    scoring["mse"] = metrics.make_scorer(mse, needs_proba=True)
    scoring["mse1"] = metrics.make_scorer(mse1, needs_proba=True)

    return scoring, scoring_proba
