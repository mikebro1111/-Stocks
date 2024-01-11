from abc import ABC, abstractmethod
from typing import List, Dict, Any, Type


class BaseStorage(ABC):
    """
    Abstract base class defining the interface for storage operations.

    This class provides abstract methods for basic CRUD operations. Implementations
    should define these methods according to their specific storage backend.
    """
    @abstractmethod
    def save_one(self, data: Dict[str, Any]):
        """
        Save a single record to the storage.

        Args:
            data (Dict[str, Any]): The data record to save.

        Returns:
            The result of the insert operation.
        """
        return self.collection.insert_one(data.dict)

    @abstractmethod
    def save_many(self, data: List[Dict[str, Any]]):
        """
        Save multiple records to the storage.

        Args:
            data (List[Dict[str, Any]]): The list of data records to save.

        Returns:
            The result of the bulk insert operation.
        """
        return self.collection.insert_many([price.dict for price in data])

    @abstractmethod
    def find(self, query: Dict[str, Any]) -> List[Type[Dict[str, Any]]]:
        """
        Find records matching a query.

        Args:
            query (Dict[str, Any]): The search query.

        Returns:
            List[Type[Dict[str, Any]]]: A list of records matching the query.
        """
        return [Dict[str, Any] for data in self.collection.find(query)]

    @abstractmethod
    def update_one(self, filter: Dict[str, Any], update: Dict[str, Any]):
        """
        Update a single record based on a filter.

        Args:
            filter (Dict[str, Any]): The filter to identify the record.
            update (Dict[str, Any]): The update to apply.

        Returns:
            The result of the update operation, or None if no record was found.
        """
        result = self.collection.update_one(filter, {'$set': update})
        if result.matched_count:
            return self.find(filter)[0]
        return None

    @abstractmethod
    def update_many(self, filter: Dict[str, Any], update: Dict[str, Any]):
        """
        Update multiple records based on a filter.

        Args:
            filter (Dict[str, Any]): The filter to identify records.
            update (Dict[str, Any]): The updates to apply.

        Returns:
            The result of the bulk update operation.
        """
        return self.collection.update_many(filter, {'$set': update})

    @abstractmethod
    def delete_one(self, filter: Dict[str, Any]):
        """
        Delete a single record based on a filter.

        Args:
            filter (Dict[str, Any]): The filter to identify the record.

        Returns:
            The result of the delete operation.
        """
        return self.collection.delete_one(filter)

    @abstractmethod
    def delete_many(self, filter: Dict[str, Any]):
        """
        Delete multiple records based on a filter.

        Args:
            filter (Dict[str, Any]): The filter to identify the records.

        Returns:
            The result of the bulk delete operation.
        """
        return self.collection.delete_many(filter)
