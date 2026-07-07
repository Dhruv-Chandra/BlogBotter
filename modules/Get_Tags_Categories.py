import string, nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Download NLTK data once at module load, not on every call
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)


def get_tags_categories(title):
    lemmatizer = WordNetLemmatizer()
    title_for_tags = title.translate(str.maketrans("", "", string.punctuation))

    list_title_for_tags = title_for_tags.split()
    list_title_for_tags.extend([title_for_tags])

    tags = set()
    stop_words = set(stopwords.words("english"))

    for word in list_title_for_tags:
        if word.lower() not in stop_words and len(word) > 1:
            tags.add(word)
            lemma = lemmatizer.lemmatize(word)
            if lemma != word:
                tags.add(lemma)

    return list(tags), [title_for_tags]
