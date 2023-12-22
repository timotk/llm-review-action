from pathlib import Path

import pytest

from llm_action.__main__ import comment_as_github_annotation, get_file_list, query_llm
from llm_action.models import Comment


def test_get_file_list():
    files = get_file_list("**/*.py")
    assert len(files) > 0


@pytest.mark.skip
def test_query_llm():
    output = query_llm("Hi")
    assert isinstance(output, str)
    assert len(output) > 0


def test_comment_as_annotation_one_line():
    comment = Comment(line_start=1, content="Test")
    expected = "::notice file=test.py,line=1::Test"
    assert comment_as_github_annotation(comment, Path("test.py")) == expected


def test_comment_as_annotation_multi_line():
    comment = Comment(line_start=1, line_end=2, content="Test")
    expected = "::notice file=test.py,line=1,endLine=2::Test"
    assert comment_as_github_annotation(comment, Path("test.py")) == expected
