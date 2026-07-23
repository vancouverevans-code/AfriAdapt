"""
Aggregate evaluation metrics.
"""


def summarize(scores):

    values = [s["score"] for s in scores]

    return {

        "average": round(
            sum(values) / len(values),
            2,
        ),

        "highest": max(values),

        "lowest": min(values),

        "examples": len(values),

    }