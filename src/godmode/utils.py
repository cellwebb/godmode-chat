async def preprocess_stream(stream, replace_double_newline=False, verbose=False):
    """Preprocess stream for display in Streamlit"""
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            if verbose:
                text_to_print = chunk.choices[0].delta.content.replace("\n", "\\n")
                print(f'"{text_to_print}"')

            text_to_write = chunk.choices[0].delta.content

            if replace_double_newline:
                text_to_write = chunk.choices[0].delta.content.replace("\n\n", "\n")

            for char in text_to_write:
                yield char
