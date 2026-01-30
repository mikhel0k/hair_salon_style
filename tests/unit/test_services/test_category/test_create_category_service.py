import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.CategoryService import create_category
from app.schemas.Category import CategoryCreate, CategoryResponse


@pytest.mark.asyncio
class TestCreateCategoryService:

    async def test_create_category_success(self):
        mock_session = AsyncMock()
        category_in = CategoryCreate(name="Haircut")

        mock_category_db = AsyncMock()
        mock_category_db.id = 1
        mock_category_db.name = "Haircut"

        with patch("app.repositories.CategoryRepository.create_category") as mock_repo:
            mock_repo.return_value = mock_category_db

            result = await create_category(category_in, mock_session)

            mock_repo.assert_called_once_with(category_data=category_in, session=mock_session)

            assert isinstance(result, CategoryResponse)
            assert result.name == "Haircut"
            mock_session.commit.assert_called_once()

    async def test_create_category_integrity_error(self):
        mock_session = AsyncMock()
        category_in = CategoryCreate(name="Haircut")

        with patch("app.repositories.CategoryRepository.create_category") as mock_repo:
            mock_repo.side_effect = IntegrityError(None, None, None)

            with pytest.raises(HTTPException) as exc:
                result = await create_category(category_in, mock_session)

            mock_repo.assert_called_once_with(category_data=category_in, session=mock_session)

            assert exc.value.status_code == 409
            assert exc.value.detail == "Category with this data already exists"
            mock_session.rollback.assert_called_once()
