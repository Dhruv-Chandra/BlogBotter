import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


def get_tags_categories(title):
    lemmatizer = WordNetLemmatizer()
    title_for_tags = title.translate(str.maketrans("", "", string.punctuation))

    list_title_for_tags = title_for_tags.split()
    list_title_for_tags.extend([title_for_tags])

    tags = []
    stop_words = set(stopwords.words("english"))

    for word in list_title_for_tags:
        if word not in stop_words and len(word) > 1:
            tags.append(word)
            tags.append(lemmatizer.lemmatize(word))

    return tags, [title_for_tags]
