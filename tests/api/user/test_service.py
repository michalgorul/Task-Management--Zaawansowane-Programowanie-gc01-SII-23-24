from uuid import UUID

import pytest
from fastapi import HTTPException
from fastapi_pagination import Page, Params
from pytest_mock import MockFixture
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.user import service
from app.api.user.models import BaseUser, User, UserCreate, UserTasks, UserUpdate
from app.api.user.service import (
    create_user,
    delete_user,
    get_user,
    get_user_tasks,
    get_users,
)
from app.database.user.models import UserTable


class TestUserServices:
    class TestCreateUser:
        @pytest.mark.asyncio
        async def test_create_user__ok(
            self,
            mocker: MockFixture,
            db: Session,
            user_create: UserCreate,
            user_table: UserTable,
            user_response: User,
        ) -> None:
            mock_create_user_crud = mocker.patch(
                "app.api.user.service.crud.create_user", return_value=user_table
            )
            created_user = await create_user(user_create, db)

            assert created_user == user_response
            mock_create_user_crud.assert_called_once_with(user_create, db)

    @pytest.mark.asyncio
    async def test_create_user__integrity_error(
        self,
        mocker: MockFixture,
        db: Session,
        user_create: UserCreate,
        user_table: UserTable,
        user_response: User,
    ) -> None:
        mock_create_user_crud = mocker.patch(
            "app.api.user.service.crud.create_user",
            side_effect=IntegrityError(statement="", params={}, orig=Exception()),
        )
        with pytest.raises(Exception) as e:
            await create_user(user_create, db)

        assert e.value.status_code == 409
        mock_create_user_crud.assert_called_once_with(user_create, db)

        @pytest.mark.asyncio
        async def test_create_user__common_exception(
            self,
            mocker: MockFixture,
            db: Session,
            user_create: UserCreate,
            user_table: UserTable,
            user_response: User,
        ) -> None:
            mock_create_user_crud = mocker.patch(
                "app.api.user.service.crud.create_user", side_effect=Exception()
            )
            with pytest.raises(Exception) as e:
                await create_user(user_create, db)

            assert e.value.status_code == 500
            mock_create_user_crud.assert_called_once_with(user_create, db)

    class TestGetUser:
        @pytest.mark.asyncio
        async def test_get_user__ok(
            self,
            mocker: MockFixture,
            db: Session,
            user_response: User,
            user_id: UUID,
            user_table: UserTable,
        ) -> None:
            mock_get_user_crud = mocker.patch(
                "app.api.user.service.crud.get_user", return_value=[user_table]
            )
            retrieved_user = await get_user(user_id, db)

            assert retrieved_user.user_id == user_id
            assert retrieved_user == user_response
            mock_get_user_crud.assert_called_once_with(user_id, db)

        @pytest.mark.asyncio
        async def test_get_user__not_found(
            self,
            mocker: MockFixture,
            db: Session,
            user_response: User,
            user_id: UUID,
            user_table: UserTable,
        ) -> None:
            mock_get_user_crud = mocker.patch(
                "app.api.user.service.crud.get_user", return_value=[]
            )
            with pytest.raises(HTTPException) as e:
                await get_user(user_id, db)

            assert e.value.status_code == 404
            mock_get_user_crud.assert_called_once_with(user_id, db)

    class TestGetUserTasks:
        @pytest.mark.asyncio
        async def test_get_user_tasks__ok(
            self,
            mocker: MockFixture,
            db: Session,
            user_id: UUID,
            user_table_with_tasks: UserTable,
            users_tasks: UserTasks,
        ) -> None:
            mock_get_user_crud = mocker.patch(
                "app.api.user.service.crud.get_user",
                return_value=[user_table_with_tasks],
            )
            retrieved_user = await get_user_tasks(user_id, db)

            assert retrieved_user.user_id == user_id
            assert retrieved_user == users_tasks
            mock_get_user_crud.assert_called_once_with(user_id, db)

        @pytest.mark.asyncio
        async def test_get_user_tasks__not_found(
            self,
            mocker: MockFixture,
            db: Session,
            user_response: User,
            user_id: UUID,
            user_table: UserTable,
        ) -> None:
            mock_get_user_crud = mocker.patch(
                "app.api.user.service.crud.get_user", return_value=[]
            )
            with pytest.raises(HTTPException) as e:
                await get_user_tasks(user_id, db)

            assert e.value.status_code == 404
            mock_get_user_crud.assert_called_once_with(user_id, db)

    class TestGetUsersUser:
        @pytest.mark.asyncio
        async def test_get_users__ok(
            self,
            mocker: MockFixture,
            db: Session,
            user_page: Page[User],
            user_id: UUID,
            size: int,
        ) -> None:
            mock_get_users_crud = mocker.patch(
                "app.api.user.service.crud.get_users", return_value=user_page
            )
            pagination = Params()
            retrieved_users = await get_users(pagination, db)

            assert retrieved_users.items[0].user_id == user_id
            assert retrieved_users.size == size
            mock_get_users_crud.assert_called_once_with(pagination, db)

    class TestUpdateUser:
        @pytest.mark.asyncio
        async def test_update_user__ok(
            self,
            mocker: MockFixture,
            db: Session,
            user_id: UUID,
            update_user: UserUpdate,
            updated_user: User,
        ) -> None:
            mock_update_user_crud = mocker.patch(
                "app.api.user.service.crud.update_user", return_value=1
            )
            mock_get_user = mocker.patch(
                "app.api.user.service.crud.get_user",
                return_value=[UserTable(**updated_user.model_dump())],
            )
            updated_user_service = await service.update_user(user_id, update_user, db)

            assert updated_user_service.model_dump() == updated_user.model_dump(
                exclude={"tasks"}
            )
            mock_update_user_crud.assert_called_once_with(
                user_id=user_id, new_user=update_user, db=db
            )
            mock_get_user.assert_called_once_with(user_id, db)

        @pytest.mark.asyncio
        async def test_update_user__common_exception(
            self,
            mocker: MockFixture,
            db: Session,
            user_id: UUID,
            update_user: UserUpdate,
        ) -> None:
            mock_update_user_crud = mocker.patch(
                "app.api.user.service.crud.update_user", side_effect=Exception()
            )
            with pytest.raises(HTTPException) as e:
                await service.update_user(user_id, update_user, db)

            assert e.value.status_code == 500
            mock_update_user_crud.assert_called_once_with(
                user_id=user_id, new_user=update_user, db=db
            )

        @pytest.mark.asyncio
        async def test_update_user__not_found(
            self,
            mocker: MockFixture,
            db: Session,
            update_user: UserUpdate,
            user_id: UUID,
        ) -> None:
            mock_update_user_crud = mocker.patch(
                "app.api.user.service.crud.update_user",
                return_value=0,
            )
            with pytest.raises(HTTPException) as e:
                await service.update_user(user_id, update_user, db)

            assert e.value.status_code == 404
            mock_update_user_crud.assert_called_once_with(
                user_id=user_id, new_user=update_user, db=db
            )

    class TestDeleteUser:
        @pytest.mark.asyncio
        async def test_delete_user__ok(
            self,
            mocker: MockFixture,
            db: Session,
            user_id: UUID,
            user_table: UserTable,
        ) -> None:
            mock_get_user_crud = mocker.patch(
                "app.api.user.service.crud.get_user", return_value=[user_table]
            )
            mock_delete_user_crud = mocker.patch(
                "app.api.user.service.crud.delete_user", return_value=user_id
            )
            deleted_user_id = await delete_user(user_id, db)

            assert deleted_user_id == user_id
            mock_get_user_crud.assert_called_once_with(user_id, db)
            mock_delete_user_crud.assert_called_once_with(user_id, db)

        @pytest.mark.asyncio
        async def test_delete_user__common_exception(
            self,
            mocker: MockFixture,
            db: Session,
            user_id: UUID,
            user_table: UserTable,
        ) -> None:
            mock_get_user_crud = mocker.patch(
                "app.api.user.service.crud.get_user", return_value=[user_table]
            )
            mock_delete_user_crud = mocker.patch(
                "app.api.user.service.crud.delete_user", side_effect=Exception
            )
            with pytest.raises(HTTPException) as e:
                await delete_user(user_id, db)

            assert e.value.status_code == 500
            mock_get_user_crud.assert_called_once_with(user_id, db)
            mock_delete_user_crud.assert_called_once_with(user_id, db)

        @pytest.mark.asyncio
        async def test_delete_user__not_found(
            self,
            mocker: MockFixture,
            db: Session,
            user_id: UUID,
            user_table: UserTable,
        ) -> None:
            mock_get_user_crud = mocker.patch(
                "app.api.user.service.crud.get_user", return_value=[]
            )
            mock_delete_user_crud = mocker.patch(
                "app.api.user.service.crud.delete_user"
            )
            with pytest.raises(HTTPException) as e:
                await delete_user(user_id, db)

            assert e.value.status_code == 404
            mock_get_user_crud.assert_called_once_with(user_id, db)
            mock_delete_user_crud.assert_not_called()
