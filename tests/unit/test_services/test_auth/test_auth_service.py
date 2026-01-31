import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.services.AuthService import registration, login
from app.schemas.Worker import WorkerCreate, Login


@pytest.mark.asyncio
class TestRegistrationAuthService:

    async def test_registration_success(self):
        mock_session = AsyncMock()
        worker_data = WorkerCreate(
            username="worker1",
            password="secret123",
            master_id=None,
            is_master=False,
            is_admin=False,
            is_active=True,
        )
        mock_worker_in_db = MagicMock()
        mock_worker_in_db.id = 1
        mock_worker_in_db.master_id = None
        mock_worker_in_db.is_master = False
        mock_worker_in_db.is_admin = False
        mock_worker_in_db.is_active = True

        with patch("app.services.AuthService.get_password_hash", return_value="hashed"), \
                patch("app.services.AuthService.create_token", return_value="jwt_token"), \
                patch("app.repositories.WorkerRepository.create_worker", new_callable=AsyncMock, return_value=mock_worker_in_db) as mock_create:
            result = await registration(worker_data, mock_session)

            mock_create.assert_called_once()
            mock_session.commit.assert_called_once()
            assert result == "jwt_token"

    async def test_registration_integrity_error_409(self):
        mock_session = AsyncMock()
        worker_data = WorkerCreate(
            username="worker1",
            password="secret123",
            master_id=None,
            is_master=False,
            is_admin=False,
            is_active=True,
        )

        with patch("app.services.AuthService.get_password_hash", return_value="hashed"), \
                patch("app.repositories.WorkerRepository.create_worker", new_callable=AsyncMock, side_effect=IntegrityError(None, None, None)):
            with pytest.raises(HTTPException) as exc:
                await registration(worker_data, mock_session)

            mock_session.rollback.assert_called_once()
            assert exc.value.status_code == 409
            assert "already exists" in exc.value.detail


@pytest.mark.asyncio
class TestLoginAuthService:

    async def test_login_success(self):
        mock_session = AsyncMock()
        login_data = Login(username="admin", password="qwerty123")
        mock_worker = MagicMock()
        mock_worker.id = 1
        mock_worker.master_id = None
        mock_worker.is_master = False
        mock_worker.is_admin = True
        mock_worker.is_active = True
        mock_worker.password = "hashed"

        with patch("app.repositories.WorkerRepository.get_worker_by_username", new_callable=AsyncMock, return_value=mock_worker), \
                patch("app.services.AuthService.verify_password", return_value=True), \
                patch("app.services.AuthService.create_token", return_value="jwt_token"):
            result = await login(login_data, mock_session)

            assert result == "jwt_token"

    async def test_login_user_not_found_401(self):
        mock_session = AsyncMock()
        login_data = Login(username="unknown", password="qwerty123")

        with patch("app.repositories.WorkerRepository.get_worker_by_username", new_callable=AsyncMock, return_value=None):
            with pytest.raises(HTTPException) as exc:
                await login(login_data, mock_session)

            assert exc.value.status_code == 401
            assert "incorrect" in exc.value.detail.lower()

    async def test_login_wrong_password_401(self):
        mock_session = AsyncMock()
        login_data = Login(username="admin", password="wrongpass")
        mock_worker = MagicMock()
        mock_worker.id = 1
        mock_worker.master_id = None
        mock_worker.is_master = False
        mock_worker.is_admin = True
        mock_worker.is_active = True
        mock_worker.password = "hashed"

        with patch("app.repositories.WorkerRepository.get_worker_by_username", new_callable=AsyncMock, return_value=mock_worker), \
                patch("app.services.AuthService.verify_password", return_value=False):
            with pytest.raises(HTTPException) as exc:
                await login(login_data, mock_session)

            assert exc.value.status_code == 401
            assert "incorrect" in exc.value.detail.lower()
