from cybulde.config_schemas.dask_cluster import dask_cluster_schema
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass
from utils.gcp_utils import access_secret_version

from cybulde.config_schemas.data_processing import dataset_cleaners_schema, dataset_readers_schema
from cybulde.config_schemas.infrastructure import gcp_schema


@dataclass
class DataProcessingConfig:
    dvc_remote_name: str = "gcs-storage"
    dvc_remote_url: str = "gs://cybulde-n/data/raw"
    dvc_raw_data_folder: str = "data/raw"

    version: str = MISSING
    data_local_save_dir: str = "./dataset/raw"
    dvc_remote_repo: str = "https://github.com/Nour-B/cybulde-data.git"
    dvc_data_folder: str = "data/raw"
    github_user_name: str = "Nour-B"
    github_access_token_secret_id: str = "cybulde-data-github-access-token"

    infrastructure: gcp_schema.GCPConfig = gcp_schema.GCPConfig()

    dataset_reader_manager: dataset_readers_schema.DatasetReaderManagerConfig = MISSING
    dataset_cleaner_manager: dataset_cleaners_schema.DatasetCleanerManagerConfig = MISSING

    dask_cluster: dask_cluster_schema.DaskClusterConfig = MISSING 
    processed_data_save_dir: str = MISSING


def setup_config() -> None:
    gcp_schema.setup_config()
    dataset_readers_schema.setup_config()
    dataset_cleaners_schema.setup_config()
    dask_cluster_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(name="data_processing_config_schema", node=DataProcessingConfig)
