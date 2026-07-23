"""
AfriAdapt Metrics
"""

from statistics import mean


def aggregate(results):

    metrics = {}

    keys = [
        "accuracy",
        "reasoning",
        "clarity",
        "safety",
        "local_relevance",
        "overall",
    ]

    for key in keys:

        metrics[key] = round(

            mean(result[key] for result in results),

            2,

        )

    return metrics