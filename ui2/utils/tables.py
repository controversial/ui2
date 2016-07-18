"""Internal utilities used in ui2."""

def make_table(rows, columns=None):
    """Create an ASCII table and return it as a string.
    
    Pass a list of dicts to represent rows in the table and a list of strings
    to represent columns. The strings in 'columns' will be used as the keys to
    the dicts in 'rows.'

    Not all column values have to be present in each row dict.

    >>> print(make_table([{"a": 1, "b": "test"}, {"yay": 16}]))
    +----------------+
    | a | b    | yay |
    |================|
    | 1 | test |     |
    |   |      | 16  |
    +----------------+
    """
    # If columns aren't specified, use all keys in the rows, alphabetized
    if columns is None:
        columns = set()
        for r in rows:
            columns.update(r.keys())
        columns = sorted(list(columns))

    # If there are no rows, add a blank one to make it prettier
    if not rows:
        rows = [{}]

    # Calculate how wide each cell needs to be
    cell_widths = {}
    for c in columns:
        values = [str(r.get(c, "")) for r in rows]
        cell_widths[c] = len(max(values + [c], key=len))

    # Used for formatting rows
    row_template = "|" + " {} |" * len(columns)
    
    # CONSTRUCT THE TABLE

    # The top row with the column titles
    justified_column_heads = [c.ljust(cell_widths[c]) for c in columns]
    header = row_template.format(*justified_column_heads)
    # The second row contains separators
    sep = "|" + "=" * (len(header) - 2) + "|"
    # Rows of data
    lines = []
    for r in rows:
        fields = [str(r.get(c, "")).ljust(cell_widths[c]) for c in columns]
        line = row_template.format(*fields)
        lines.append(line)

    # Borders go on the top and the bottom
    border = "+" + "-" * (len(header) - 2) + "+"
    return "\n".join([border, header, sep] + lines + [border])
