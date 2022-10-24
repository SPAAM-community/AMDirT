from typing import Iterable
import pandas as pd
from rich.table import Table
from AMDirT import logger


def generate_table(columns: Iterable[str], rows, title: str, method: str) -> str:
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
            logger.info(*row)
            table.add_row(*row)
        return table
    else:
        df = pd.DataFrame(rows, columns=columns)
        return df.to_markdown(index=False, tablefmt="pretty")
