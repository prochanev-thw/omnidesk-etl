def parse_nested_elements(data: dict, element_name: str) -> list:
    return [
        item[element_name] for
        key, item in
        data.items() if
        key != 'total_count'
    ]
