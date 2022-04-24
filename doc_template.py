from elasticsearch_dsl import (  # type: ignore
    Document,
    Text,
    Keyword,
    DenseVector,
    token_filter,
    analyzer,
    Nested,
    Object,
)


class BaseDoc(Document):
    """
    wapo document mapping structure
    """

    id = (
        Keyword()
    )  # we want to treat the doc_id as a Keyword (its value won't be tokenized or normalized).
    title = (
        Text()
    )  # by default, Text field will be applied a standard analyzer at both index and search time
    instructions = Nested(
        analyzer="english"
    )
    fsa_lights_per100g = Object()  # we can also set the standard analyzer explicitly
    ingredients = Object()  # index the same content again with english analyzer
    nutr_values_per100g = Object()
    URL = Text()

    def save(self, *args, **kwargs):
        """
        save an instance of this document mapping in the index
        this function is not called because we are doing bulk insertion to the index in the index.py
        """
        return super(BaseDoc, self).save(*args, **kwargs)


if __name__ == "__main__":
    pass
