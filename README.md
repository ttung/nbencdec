# NoteBook ENCode DECode

## Rationale
Storing `.ipynb` files in code repositories has two significant drawbacks:
1. Most, if not all existing IDEs will not index `.ipynb` files.  Therefore, if one wishes to refactor code that impacts `.ipynb`, it often has to be done manually.
2. It is challenging to code review `.ipynb` files well.

At the same time, ipython notebooks have significant usability advantages over plain python source files.  `nbencdec` allows users to convert .ipynb into a .py file with enough hints embedded in comments such that it is possible to reconstruct the original structure of the `.ipynb` file.

## Usage
* Install the nbencdec package.
  * Option 1: Clone the repo, and run `pip install -e .`
  * Option 2: run `pip install nbencdec`.
* Run `nbencdec encode <ipynb file> <output .py file>` to encode an `.ipynb` file as a `.py` file.
* Run `nbencdec decode <py file> <output .ipypy file>` to decode a properly encoded `.py` file.

## Hints
There are four types of hints embedded in the comments:
1. `# EPY: stripped_notebook: <json>`: This represents the json structure of the original `.ipynb` file, except for the `cells` field.  See the [ipython file format specification](https://nbformat.readthedocs.io/en/latest/) for more details.
2. `# EPY: START code` and `# EPY: END code`.  Lines in between these two markers should be incorporated into a single [code cell](https://nbformat.readthedocs.io/en/latest/format_description.html#code-cells) in the `.ipynb` file.
3. `# EPY: START markdown` and `# EPY: END markdown`.  Lines in between these two markers should be incorporated into a single [code cell](https://nbformat.readthedocs.io/en/latest/format_description.html#markdown-cells) in the `.ipynb` file.
4. `# EPY: ESCAPE`.  The remaining text on that line should be written verbatim to the `.ipynb` file.  This is used for [ipython magic commands](http://ipython.readthedocs.io/en/stable/interactive/magics.html), which would not be valid python.
