import logging
from typing import Any, Dict, List, Optional

import reflex as rx

from ryoma.datasource.factory import DataSourceProvider
from ryoma_lab.models.datasource import DataSourceModel
from ryoma_lab.services.catalog import CatalogService
from ryoma_lab.services.datasource import DataSourceService


class DataSourceState(rx.State):
    id: int
    name: str
    datasource: Optional[str] = ""
    connection_url: str
    attributes: dict[str, str] = {}
    catalog_id: int
    sort_value: str
    is_open: bool = False
    allow_crawl_catalog: bool = True
    config_type: str = "connection_url"
    datasources: List[DataSourceModel] = []

    update_datasource_dialog_open: bool = False

    def toggle_update_datasource_dialog(self, datasource_id: int):
        self.update_datasource_dialog_open = not self.update_datasource_dialog_open
        self.id = datasource_id

    def _sort_datasources(self, key: str):
        self.datasources.sort(key=lambda ds: getattr(ds, key, "").lower())

    def sort_values(self, value: str):
        self.sort_value = value
        self._sort_datasources(self.sort_value)

    def load_datasources(self):
        with DataSourceService() as datasource_service:
            self.datasources = datasource_service.load_datasources()
        if self.sort_value:
            self._sort_datasources(self.sort_value)

    def change_crawl_catalog(self, value: bool):
        self.allow_crawl_catalog = value

    @rx.var
    def datasource_names(self) -> List[str]:
        return [datasource.name for datasource in self.datasources]

    @rx.var
    def num_datasources(self) -> int:
        return len(self.datasources)

    def _datasource_fields(self, datasource: str) -> dict[str, Any]:
        fields = DataSourceProvider[datasource].value.__fields__.copy()
        for additional_field in ["type", "name", "connection_url"]:
            if additional_field in fields:
                del fields[additional_field]
        return fields

    @rx.var
    def datasource_attribute_names(self) -> List[str]:
        if self.datasource:
            fields = self._datasource_fields(self.datasource)
            return list(fields.keys())
        else:
            return []

    @rx.var
    def missing_configs(self) -> bool:
        if not self.datasource or not self.name:
            return True

        # Use connection_url
        if self.config_type == "connection_url":
            return not self.connection_url
        else:
            # Required by the data source
            model_fields = self._datasource_fields(self.datasource)
            return any(
                model_fields[key].required and not self.attributes.get(key)
                for key in model_fields
            )

    def set_datasource_attributes(self, attribute: str, value: str):
        self.attributes[attribute] = value

    def get_datasource_attributes(self) -> dict[str, str]:
        model_fields = self._datasource_fields(self.datasource)
        return {key: self.attributes.get(key, "") for key in model_fields}

    def get_datasource_configs(self) -> dict:
        return (
            {"connection_url": self.connection_url}
            if self.config_type == "connection_url"
            else self.attributes
        )

    def connect_and_add_datasource(self):
        if self.missing_configs:
            return
        configs = self.get_datasource_configs()
        try:
            with DataSourceService() as datasource_service:
                ds = datasource_service.connect_datasource(self.datasource, configs)
                datasource_model = self.build_datasource_model()
                datasource_service.create_datasource(datasource_model.dict())

            with CatalogService() as catalog_service:
                catalog_service.upsert(self.name, ds.database, ds.db_schema)

            rx.toast.success(f"Connected to {self.datasource}")
        except Exception as e:
            logging.error(f"Failed to connect to {self.datasource}: {e}")
            rx.toast.error(f"Failed to connect to {self.datasource}: {e}")

        self.load_datasources()

    def build_datasource_model(
        self, datasource: Optional[DataSourceModel] = None
    ) -> DataSourceModel:
        datasource_attrs = self.get_datasource_attributes()
        datasource_params = {
            "name": self.name,
            "type": self.datasource,
            "connection_url": self.connection_url,
            "attributes": str(datasource_attrs),
        }
        if datasource:
            for key, value in datasource_params.items():
                setattr(datasource, key, value)
            return datasource
        return DataSourceModel(**datasource_params)

    def update_datasource(self, ds_id: int):
        datasource = self.build_datasource_model()
        with DataSourceService() as datasource_service:
            datasource_service.update_datasource(ds_id, datasource.dict())
        self.load_datasources()

    def delete_datasource(self, datasource_id: int):
        with DataSourceService() as datasource_service:
            datasource_service.delete_datasource(datasource_id)
        self.load_datasources()

    @staticmethod
    def connect(datasource_name: str) -> Any:
        with DataSourceService() as datasource_service:
            return datasource_service.connect_datasource_by_name(datasource_name)

    def on_load(self):
        self.load_datasources()
