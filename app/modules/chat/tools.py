from langchain_core.tools import tool


@tool(parse_docstring=True)
def deep_think(content: str) -> str:
    """
    深度思考函数，接收思考内容并直接返回思考内容，用于在上下文中协助推理。

    Args:
        content (str): 思考的内容。

    Returns:
        str: 思考的内容，用于追加在上下文中协助推理。
    """
    print(f"深度思考:\n {content}")
    return content


if __name__ == "__main__":
    print(deep_think("1+1=2"))
