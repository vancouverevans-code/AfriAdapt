"""
Simple benchmark scorer.
"""


def score_prediction(
    prediction,
    reference,
):

    prediction = prediction.lower()

    reference = reference.lower()

    ref_words = set(reference.split())

    pred_words = set(prediction.split())

    overlap = ref_words.intersection(pred_words)

    if len(ref_words) == 0:
        return 0

    return round(
        len(overlap) / len(ref_words),
        2,
    )