import pandas as pd
from rich.table import Table


def generate_table(columns, rows, title, method):
    """Generate output table

    Args:
        columns (list): name of columns
        rows (list of list): rows of the table
        title (str): title of the table
        method (string): table generation method (rich or markdown)
    """

    if method == "rich":
        table = Table(title=title)
        for column in columns:
            table.add_column(column, style="red", overflow="fold")
        for row in rows:
            print(*row)
            table.add_row(*row)
        return table
    else:
        df = pd.DataFrame(rows, columns=columns)
        return df.to_markdown(index=False, tablefmt="pretty")
