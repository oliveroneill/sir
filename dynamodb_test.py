import dynamodb


def test_convert_null_to_empty_string():
    data = {
        "test": 1,
        "none_value": None,
        "good_string": "string_val",
        "word_none": "None",
        "empty_string": ""
    }
    expected = {
        "test": 1,
        "none_value": None,
        "good_string": "string_val",
        "word_none": "None",
        "empty_string": None
    }
    output = {k: dynamodb.convert_empty_string_to_none(v) for k, v in data.items()}
    assert output == expected


def test_convert_empty_string_to_none():
    data = {
        "test": 1,
        "none_value": None,
        "good_string": "string_val",
        "word_none": "None",
        "empty_string": ""
    }
    expected = {
        "test": 1,
        "none_value": "",
        "good_string": "string_val",
        "word_none": "None",
        "empty_string": ""
    }
    output = {k: dynamodb.convert_null_to_empty_string(v) for k, v in data.items()}
    assert output == expected
