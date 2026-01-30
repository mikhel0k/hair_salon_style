import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.CategoryService import get_categories_paginated
from app.schemas.Category import CategoryCreate, CategoryResponse


@pytest.mark.asyncio
class TestGetCategoriesPaginatedService:

    async def test_get_categories_paginated_success(self):
        mock_session = AsyncMock()

        mock_category_1 = AsyncMock()
        mock_category_1.id = 1
        mock_category_1.name = "Haircut"

        mock_category_2 = AsyncMock()
        mock_category_2.id = 2
        mock_category_2.name = "Manicure"

        mock_category_3 = AsyncMock()
        mock_category_3.id = 3
        mock_category_3.name = "Pedicure"

        with patch("app.repositories.CategoryRepository.read_categories_paginate") as mock_repo:
            mock_repo.return_value = [mock_category_1, mock_category_2, mock_category_3]

            result = await get_categories_paginated(mock_session, 0, 99)
            mock_repo.assert_called_once_with(skip=0, limit=99, session=mock_session)

            assert isinstance(result, list)
            assert len(result) == 3
            assert result[0].name == "Haircut"
            assert result[0].id == 1
            assert result[1].name == "Manicure"
            assert result[1].id == 2
            assert result[2].name == "Pedicure"
            assert result[2].id == 3

    async def test_get_one_category_paginated_success(self):
        mock_session = AsyncMock()

        mock_category_1 = AsyncMock()
        mock_category_1.id = 1
        mock_category_1.name = "Haircut"

        with patch("app.repositories.CategoryRepository.read_categories_paginate") as mock_repo:
            mock_repo.return_value = [mock_category_1]

            result = await get_categories_paginated(mock_session, 0, 99)
            mock_repo.assert_called_once_with(skip=0, limit=99, session=mock_session)

            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0].name == "Haircut"
            assert result[0].id == 1

    async def test_get_no_one_category_paginated_success(self):
        mock_session = AsyncMock()

        with patch("app.repositories.CategoryRepository.read_categories_paginate") as mock_repo:
            mock_repo.return_value = []

            result = await get_categories_paginated(mock_session, 0, 99)
            mock_repo.assert_called_once_with(skip=0, limit=99, session=mock_session)

            assert isinstance(result, list)
            assert len(result) == 0
