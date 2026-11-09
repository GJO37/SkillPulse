
import os, pandas as pd


def load_dataset(file_path: str):
    if not file_path:
        raise ValueError("File path is empty")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    try:
        data = pd.read_csv(file_path, encoding="utf-8-sig")
        required_columns = {"Job Title", "Skillset"}

        if not required_columns.issubset(data.columns):
            raise ValueError("Dataset contains invalid columns")

        if data.empty:
            raise ValueError("Dataset is empty")
        
        data = data[["Job Title", "Skillset"]].copy()
        data = data.dropna(subset=["Job Title", "Skillset"])

        data["job_title"] = (
            data["Job Title"]
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .str.lower()
        )

        data["skillset"] = data["Skillset"].str.split(",")
        data = data.explode("skillset")

        data["skillset"] = (
            data["skillset"]
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .str.lower()
        )

        dataset = data[(data["job_title"] != "") & (data["skillset"] != "")]

        if dataset.empty:
            raise ValueError("No valid dataset entries found")
        
        dataset = dataset.drop_duplicates(subset=["job_title", "skillset"])
        dataset = dataset.sort_values(["job_title", "skillset"])
        dataset = dataset.groupby("job_title", sort=True)["skillset"].agg(list)

        return dataset.to_dict()

    except (OSError, UnicodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
        raise RuntimeError(f"Failed to load dataset: {error}") from error