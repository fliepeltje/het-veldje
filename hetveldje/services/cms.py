import os
from dataclasses import dataclass

import frontmatter
import markdown2


@dataclass
class FaqItem:
    question: str
    html_content: str

    @classmethod
    def from_file(cls, file_path: str) -> "FaqItem":
        with open(file_path, "r") as f:
            item = frontmatter.load(f)
        return cls(
            question=item.metadata["title"],
            html_content=markdown2.markdown(item.content),
        )

    @classmethod
    def get_all(cls) -> list["FaqItem"]:
        paths = [f"content/faq/{n}" for n in os.listdir("content/faq")]
        return [cls.from_file(p) for p in paths]
