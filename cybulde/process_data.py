from cybulde.config_schemas.data_processing.dataset_cleaners_schema import DatasetCleanerManagerConfig
from cybulde.utils.utils import get_logger
from hydra.utils import instantiate
from omegaconf import OmegaConf
from pathlib import Path
import dask.dataframe as dd

from pathlib import Path
import os

from dask.distributed import Client

from cybulde.config_schemas.data_processing_config_schema import DataProcessingConfig
from cybulde.utils.config_utils import get_config
from cybulde.utils.data_utils import get_raw_data_with_version
from cybulde.utils.gcp_utils import access_secret_version

def process_raw_data(
    df_partition: dd.core.DataFrame, dataset_cleaner_manager: DatasetCleanerManagerConfig
) -> dd.core.Series:
    processed_partition: dd.core.Series = df_partition["text"].apply(dataset_cleaner_manager)
    return processed_partition


@get_config(config_path="../configs", config_name="data_processing_config")
def process_data(config: DataProcessingConfig) -> None:
    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")

    #print(config)
    #print(OmegaConf.to_yaml(config))
    #return

    processed_data_save_dir = config.processed_data_save_dir

    cluster = instantiate(config.dask_cluster)
    client = Client(cluster)
    try:
        dataset_reader_manager = instantiate(config.dataset_reader_manager)
        dataset_cleaner_manager = instantiate(config.dataset_cleaner_manager)

        df = dataset_reader_manager.read_data(config.dask_cluster.n_workers)

        #print(60*"#")
        #print(f"{df.npartitions=}")
        #print(60*"#")

        logger.info("Cleaning data...")
        df = df.assign(
            cleaned_text=df.map_partitions(
                process_raw_data, dataset_cleaner_manager=dataset_cleaner_manager, meta=("text", "object")
            )
        )
        df = df.compute()

        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
        test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")

        train_df = df[df["split"] == "train"]
        dev_df = df[df["split"] == "dev"]
        test_df = df[df["split"] == "test"]

        train_df.to_parquet(train_parquet_path)
        dev_df.to_parquet(dev_parquet_path)
        test_df.to_parquet(test_parquet_path)
        
    finally:
        logger.info("Closing dask client and cluster...")
        client.close()
        cluster.close()


if __name__ == "__main__":
    process_data()
