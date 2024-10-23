
from pathlib import Path
import pandas as pd

from cybulde.config_schemas.tokenizer_training_config_schema import TokenizerTrainingConfig
from cybulde.utils.config_utils import get_pickle_config
from cybulde.utils.utils import get_logger



@get_pickle_config(config_path="cybulde/configs/automatically_generated", config_name="tokenizer_training_config")
def train_tokenizer(config: TokenizerTrainingConfig) -> None:
    logger = get_logger(Path(__file__).name)


    data_parquet_path = config.data_parquet_path
    text_column_name = config.text_column_name

    df = pd.read_parquet(data_parquet_path)
    print(df[text_column_name].head())



    print(config)
    exit(0)

    

    

if __name__ == "__main__":
    train_tokenizer()