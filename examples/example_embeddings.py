from embedding_service.client import EmbeddingClient

# run:
# python -m embedding_service.server --embedding sbert  --model msmarco-distilbert-base-v3
if __name__ == "__main__":
    sbert_encoder = EmbeddingClient(
        host="localhost", embedding_type="sbert"
    )  # connect to the sbert embedding server
    # fasttext_encoder = EmbeddingClient(
    #     host="localhost", embedding_type="fasttext"
    # )  # connect to the fasttext embedding server
    texts = [
        "romaine lettuce",
        "black olives",
        "grape tomatoes",
        "garlic",
        "pepper",
        "purple onion",
        "seasoning",
        "garbanzo beans",
        "feta cheese crumbles"
    ]  # encode two sentences/documents at the same time
    embedding = sbert_encoder.encode(texts)
    print(embedding.shape)  # shape is (2, 768)
    print(embedding)
    print("="*20)

    texts2 = [
      "plain flour, ground pepper, salt, tomatoes",
    ]

    embedding = sbert_encoder.encode(texts2)
    print(embedding.shape)  # shape is (2, 768)
    print(embedding)
    print("=" * 20)
    # embedding = fasttext_encoder.encode(texts)
    # print(embedding.shape)  # shape is (2, 300)
