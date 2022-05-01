from elasticsearch_dsl import (  # type: ignore
    Document,
    Text,
    Integer,
    Float,
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

    id = Keyword() # we want to treat the id as a Keyword (its value won't be tokenized or normalized).
    title = Text() # by default, Text field will be applied a standard analyzer at both index and search time
    instructions = Object(dynamic="false")
    instructions_length = Integer()
    fsa_lights_per100g = Object(dynamic="false")  # we can also set the standard analyzer explicitly
    healthiness = Integer()
    ingredients = Object(dynamic="false")  # index the same content again with english analyzer
    ingredients_plain_text = Text(
        analyzer = "english"
    )
    # nutr_values_per100g = Object(dynamic="false")
    nutr_values_per100g_energy = Float()
    nutr_values_per100g_fat = Float()
    nutr_values_per100g_protein = Float()
    nutr_values_per100g_salt = Float()
    nutr_values_per100g_saturates = Float()
    nutr_values_per100g_sugars = Float()
    URL = Text()

    def save(self, *args, **kwargs):
        """
        save an instance of this document mapping in the index
        this function is not called because we are doing bulk insertion to the index in the index.py
        """
        return super(BaseDoc, self).save(*args, **kwargs)


if __name__ == "__main__":
    pass
