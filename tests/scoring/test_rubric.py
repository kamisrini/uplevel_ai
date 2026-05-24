"""Tests for the VP Engineering rubric definitions."""

from src.scoring.rubric import DIMENSION_NAMES, RUBRIC, RUBRIC_BY_NAME, rubric_as_text


def test_rubric_has_ten_dimensions():
    assert len(RUBRIC) == 10


def test_all_dimensions_have_five_score_levels():
    for dim in RUBRIC:
        assert set(dim.score_descriptors.keys()) == {1, 2, 3, 4, 5}, dim.name


def test_rubric_by_name_index_matches_list():
    assert set(RUBRIC_BY_NAME.keys()) == set(DIMENSION_NAMES)


def test_rubric_as_text_contains_all_dimension_names():
    text = rubric_as_text()
    for dim in RUBRIC:
        assert dim.name in text or dim.name.replace("_", " ").title() in text
