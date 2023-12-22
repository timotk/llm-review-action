from llm_review.models import Comment, Comments


def test_comment():
    Comment(line_start=1, content="Test")
    Comment(line_start=1, line_end=2, content="Test")


def test_comments_from_dict():
    Comments.model_validate(
        [
            {"line_start": 1, "content": "Test"},
            {"line_start": 1, "line_end": 2, "content": "Test"},
        ]
    )
