from collections import defaultdict
from typing import Dict, Any
import pytest

class IdNotFoundError(Exception):
    """Exception for incorrect id."""

    def __init__(self, ID) -> None:
        """Init exception.

        Args:
            id: item id
        """
        self.message = f"Item with id = {ID} not found"
        super().__init__(self.message)


class TreeStore:
    """Class for storing input items."""

    def __init__(self, items: list[Dict[str, Any]]):
        self.items = items
        self.itemId, self.parentChild = self._createDictsForItems()
        self.idAllParents = self._calculateParents()

    def _createDictsForItems(self) -> list[Dict[str, Any]]:
        """Create two dictionaries with items info.

        Args:
            items (list[dict]): input list with data.

        Returns:
            Two dictionaries:
            itemId: key - id, value - dictionary with info for item
            parentChild: key - id, value - list of dicts of all children
        """
        items = self.items
        itemId = {}
        parentChild = defaultdict(list)
        for item in items:
            identification = item["id"]
            parent = item["parent"]
            itemId[identification] = item
            parentChild[parent].append(item)
        return [itemId, parentChild]

    def _calculateParents(self) -> Dict[str, Any]:
        """Find all ancestors.

        Args:
            items (list[dict]): input list with items info.
            itemId (dict): key - id, value - dictionary with info for item
            parentChild (dict): key - id, value - list of dicts of all children

        Returns:
            dict: key - id, value - list of ancestors.
        """
        itemId = self.itemId
        idAllParents = defaultdict(list)
        for key in itemId:
            ID = key
            parent = itemId[ID]["parent"]
            while parent != "root":
                idAllParents[key].append(itemId[parent])
                ID = parent
                parent = itemId[ID]["parent"]
        return idAllParents

    def getAll(self):
        """Get input list.
        Time complexity - O(1).
        """
        return self.items

    def getItem(self, ID: int) -> Dict[str, Any]:
        """Get item with provided it.
        Time complexity - O(1).
        Args:
            ID (int): item id

        Returns:
            Dictionary with information for item with id = ID.
        """
        if ID not in self.itemId:
            raise IdNotFoundError(ID)
        return self.itemId[ID]

    def getChildren(self, ID: int) -> list[Dict[str, Any]]:
        """Get all children of item with provided id.
        Time complexity - O(1).
        Args:
            ID (int): item id

        Returns:
            List[dict]: list of children (dictionaries) of provided item.
        """
        if ID not in self.itemId:
            raise IdNotFoundError(ID)
        return self.parentChild[ID]

    def getAllParents(self, ID: int) -> list[Dict[str, Any]]:
        """Return all ancestors of item with id = ID.
        Time complexity - O(1).

        Args:
            ID (int): item id.

        Returns:
            List[dict]: list of ancestors.
        """
        if ID not in self.itemId:
            raise IdNotFoundError(ID)
        return self.idAllParents[ID]


def testValidCommands():
    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None}
    ]
    ts = TreeStore(items)
    assert ts.getAll() == [{"id": 1, "parent": "root"}, {"id": 2, "parent": 1, "type": "test"}, {"id": 3, "parent": 1, "type": "test"}, {"id": 4, "parent": 2, "type": "test"}, {
        "id": 5, "parent": 2, "type": "test"}, {"id": 6, "parent": 2, "type": "test"}, {"id": 7, "parent": 4, "type": None}, {"id": 8, "parent": 4, "type": None}]
    assert ts.getItem(7) == {"id": 7, "parent": 4, "type": None}
    assert ts.getChildren(4) == [{"id": 7, "parent": 4, "type": None}, {
        "id": 8, "parent": 4, "type": None}]
    assert ts.getChildren(5) == []
    assert ts.getAllParents(7) == [{"id": 4, "parent": 2, "type": "test"}, {
        "id": 2, "parent": 1, "type": "test"}, {"id": 1, "parent": "root"}]


def testInvalidCommands():
    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None}
    ]
    ts = TreeStore(items)
    with pytest.raises(IdNotFoundError):
        ts.getItem(0)
    with pytest.raises(IdNotFoundError):
        ts.getChildren(0)
    with pytest.raises(IdNotFoundError):
        ts.getAllParents(0)
