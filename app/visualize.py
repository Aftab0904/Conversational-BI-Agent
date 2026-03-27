import matplotlib.pyplot as plt

def auto_plot(df):

    if df is None or len(df) == 0:
        return None

    # Limit rows for clean chart
    df = df.head(10)

    try:
        # Case 1: 2 columns → bar chart
        if df.shape[1] == 2:
            x = df.iloc[:, 0]
            y = df.iloc[:, 1]

            fig, ax = plt.subplots()
            ax.bar(x.astype(str), y)
            ax.set_title("Top Results")
            plt.xticks(rotation=45)
            return fig

        # Case 2: numeric trend
        elif any("order" in col.lower() for col in df.columns):
            fig, ax = plt.subplots()
            df.plot(ax=ax)
            ax.set_title("Trend Analysis")
            return fig

        # Case 3: fallback
        else:
            fig, ax = plt.subplots()
            df.head(10).plot(kind="bar", ax=ax)
            ax.set_title("Data Overview")
            return fig

    except Exception:
        return None