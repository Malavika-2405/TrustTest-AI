
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load a free, lightweight model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def calculate_semantic_similarity(expected_answer, actual_answer):
    """
    Calculates semantic similarity between expected and actual answers.
    Returns a score between 0 and 100.
    """

    if not expected_answer.strip() or not actual_answer.strip():
        return 0.0

    embeddings = model.encode(
        [expected_answer, actual_answer]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    score = max(0.0, min(100.0, float(similarity) * 100))

    return round(score, 2)
