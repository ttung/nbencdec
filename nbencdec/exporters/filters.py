import functools


def comment_lines_with_escaping(
        text,
        prefix="#",
        escape_prefix="# EPY",
        escape_format_string="# EPY: ESCAPE {}"):
    """
    Build a Python comment line from input text.

    Parameters
    ----------
    text : str
        Text to comment out.
    prefix : str
        Character to append to the start of each line.
    """
    def escape_if_necessary(line):
        if line.startswith(escape_prefix):
            return escape_format_string.format(line)
        else:
            return "{}{}".format(prefix, line)

    splitlines = [
        escape_if_necessary(line)
        for line in text.splitlines()]
    return "\n".join(splitlines)


def ipython2encodedpython(code):
    def tweak_transform(orig_transform):
        """
        Takes the transform and modifies it such that we compare each line to its transformation.  If they are
        different, that means the line is a special ipython command.  We strip that from the output, but record the
        special command in a comment so we can restore it.
        """
        def new_push_builder(push_func):
            def new_push(line):
                result = push_func(line)

                if line != result:
                    return "# EPY: ESCAPE {}".format(line)

                return result
            return new_push

        orig_transform.push = functools.update_wrapper(new_push_builder(orig_transform.push), orig_transform.push)

        return orig_transform

    from IPython.core.inputtransformer import StatelessInputTransformer
    @StatelessInputTransformer.wrap
    def escaped_epy_lines(line):
        """Transform lines that happen to look like EPY comments."""
        if line.startswith("# EPY"):
            return "# EPY: ESCAPE {}".format(line)
        return line

    """Transform IPython syntax to an encoded Python syntax

    Parameters
    ----------

    code : str
        IPython code, to be transformed to Python encoded in a way to facilitate transformation back into IPython.
    """
    from IPython.core.inputsplitter import IPythonInputSplitter

    # get a list of default line transforms.  then capture
    fake_isp = IPythonInputSplitter(line_input_checker=False)
    logical_line_transforms = [escaped_epy_lines()]
    logical_line_transforms.extend([tweak_transform(transform) for transform in fake_isp.logical_line_transforms])

    isp = IPythonInputSplitter(line_input_checker=False, logical_line_transforms=logical_line_transforms)
    result = isp.transform_cell(code)
    if result.endswith("\n") and not code.endswith("\n"):
        # transform_cell always slaps a trailing NL.  If the input did _not_
        # have a trailing NL, then we remove it.
        result = result[:-1]
    return result
