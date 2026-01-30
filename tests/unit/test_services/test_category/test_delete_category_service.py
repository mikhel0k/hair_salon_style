import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.CategoryService import delete_category


@pytest.mark.asyncio
class TestDeleteCategoryService:

    async def test_delete_category_success(self):
        mock_session = AsyncMock()
        category_id = 1

        mock_category_db = AsyncMock()
        mock_category_db.id = category_id

        with patch("app.repositories.CategoryRepository.read_category", return_value=mock_category_db) as mock_read, \
                patch("app.repositories.CategoryRepository.delete_category", return_value=None) as mock_delete:
            await delete_category(category_id, mock_session)

            mock_read.assert_called_once_with(category_id=category_id, session=mock_session)
            mock_delete.assert_called_once_with(category=mock_category_db, session=mock_session)
            mock_session.commit.assert_called_once()

    async def test_delete_category_not_found(self):
        mock_session = AsyncMock()
        category_id = 999

        with patch("app.repositories.CategoryRepository.read_category", return_value=None) as mock_read:
            with pytest.raises(HTTPException) as exc:
                await delete_category(category_id, mock_session)

            assert exc.value.status_code == 404
            assert exc.value.detail == "Category not found"
            mock_session.commit.assert_not_called()

    async def test_delete_category_integrity_error(self):
        mock_session = AsyncMock()
        category_id = 1
        mock_category_db = AsyncMock()

        with patch("app.repositories.CategoryRepository.read_category", return_value=mock_category_db), \
                patch("app.repositories.CategoryRepository.delete_category",
                      side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await delete_category(category_id, mock_session)

            assert exc.value.status_code == 409
            assert exc.value.detail == "Something went wrong"
            mock_session.rollback.assert_called_once()
