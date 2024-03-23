from dataclasses import dataclass, asdict

from flask import Flask, request
from natasha import Segmenter, Doc, MorphVocab, NewsEmbedding, NewsMorphTagger


_SEGMENTER = Segmenter()
_MORPH_VOCAB = MorphVocab()
_EMB = NewsEmbedding()
_MORPH_TAGGER = NewsMorphTagger(_EMB)

app = Flask(__name__)


@dataclass
class TokenSchema:
    num: int
    text: str
    lemma: str
    pos: str
    attrs: dict[str, str]


@dataclass
class SentenceSchema:
    num: int
    text: str
    tokens: list[TokenSchema]


@dataclass
class DocumentSchema:
    sentences: list[SentenceSchema]


@app.post("/analyse")
def analyse_document() -> dict:
    text = request.json.get("text")
    if not text:
        return {"error": "No text provided"}

    natasha_doc = Doc(text)
    natasha_doc.segment(_SEGMENTER)
    natasha_doc.tag_morph(_MORPH_TAGGER)
    for token in natasha_doc.tokens:
        token.lemmatize(_MORPH_VOCAB)

    doc = DocumentSchema(sentences=[])
    for sentence_num, sent in enumerate(natasha_doc.sents):
        sentence = SentenceSchema(num=sentence_num, text=sent.text, tokens=[])
        for token_num, token in enumerate(sent.tokens):
            token_schema = TokenSchema(
                num=token_num,
                text=token.text,
                lemma=token.lemma,
                pos=token.pos,
                attrs=token.feats,
            )
            sentence.tokens.append(token_schema)
        doc.sentences.append(sentence)

    return asdict(doc)


if __name__ == "__main__":
    app.run()
