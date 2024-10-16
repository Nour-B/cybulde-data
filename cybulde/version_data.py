from cybulde.config_schemas.data_processing_config_schema import DataProcessingConfig
from cybulde.utils.config_utils import get_config
from cybulde.utils.data_utils import initialize_dvc, initialize_dvc_storage, make_new_data_version


@get_config(config_path="../configs", config_name="data_processing_config")
def version_data(config: DataProcessingConfig) -> None:
    print(config)
    initialize_dvc()

    initialize_dvc_storage(config.dvc_remote_name, config.dvc_remote_url)

    make_new_data_version(config.dvc_raw_data_folder, config.dvc_remote_name)


if __name__ == "__main__":
    version_data()
