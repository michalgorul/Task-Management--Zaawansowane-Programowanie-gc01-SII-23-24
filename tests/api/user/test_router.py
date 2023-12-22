from uuid import UUID

import responses
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi_pagination import Page
from pytest_mock import MockFixture

from app.api.user.models import BaseUser, User, UserCreate
from app.api.user.service import USER_NOT_FOUND


class TestUserRoutes:
    class TestCreateUser:
        @responses.activate
        def test_create_user__ok(
            self,
            mocker: MockFixture,
            client: TestClient,
            user: User,
            user_create: UserCreate,
        ) -> None:
            mock_create_user_service = mocker.patch(
                "app.api.user.router.service.create_user", return_value=user
            )
            responses.add(
                responses.POST, "/users/", json=user.model_dump_json(), status=200
            )
            response = client.post(
                "/users/", json=user_create.model_dump() | {"password": "password1!"}
            )

            assert response.status_code == 200
            created_user = response.json()
            assert created_user["username"] == user_create.username
            assert created_user["email"] == user_create.email
            mock_create_user_service.assert_awaited_once()

        @responses.activate
        def test_create_user__unprocessable_entity(
            self,
            mocker: MockFixture,
            client: TestClient,
            user_create: UserCreate,
        ) -> None:
            mock_create_user_service = mocker.patch(
                "app.api.user.router.service.create_user"
            )
            response = client.post("/users/", json=user_create.model_dump_json())

            assert response.status_code == 422
            mock_create_user_service.assert_not_awaited()

    class TestGetUser:
        @responses.activate
        def test_get_user__ok(
            self, mocker: MockFixture, client: TestClient, user: User, user_id: UUID
        ) -> None:
            mock_get_user_service = mocker.patch(
                "app.api.user.router.service.get_user", return_value=user
            )
            responses.add(
                responses.GET,
                f"/users/{user_id}",
                json=user.model_dump_json(),
                status=200,
            )
            response = client.get(f"/users/{user_id}")

            assert response.status_code == 200
            retrieved_user = response.json()
            assert isinstance(UUID(retrieved_user["userId"]), UUID)
            assert retrieved_user["userId"] == str(user_id)
            mock_get_user_service.assert_awaited_once()

        @responses.activate
        def test_get_user__not_found(
            self, mocker: MockFixture, client: TestClient, user: User, user_id: UUID
        ) -> None:
            mock_get_user_service = mocker.patch(
                "app.api.user.router.service.get_user",
                side_effect=HTTPException(*USER_NOT_FOUND),
            )
            response = client.get(f"/users/{user_id}")

            assert response.status_code == 404
            mock_get_user_service.assert_awaited_once()

    class TestGetUsersUser:
        @responses.activate
        def test_get_users__ok(
            self,
            mocker: MockFixture,
            client: TestClient,
            user_page: Page[User],
            user_id: UUID,
            size: int,
        ) -> None:
            mock_get_users_service = mocker.patch(
                "app.api.user.router.service.get_users", return_value=user_page
            )
            responses.add(
                responses.GET, "/users/", json=user_page.model_dump_json(), status=200
            )
            response = client.get("/users/")

            assert response.status_code == 200
            assert response.json()["items"][0]["userId"] == str(user_id)
            assert response.json()["size"] == size
            mock_get_users_service.assert_awaited_once()

    class TestUpdateUser:
        @responses.activate
        def test_update_user__ok(
            self,
            mocker: MockFixture,
            client: TestClient,
            user_id: UUID,
            update_user: BaseUser,
            updated_user: User,
        ) -> None:
            mock_update_user_service = mocker.patch(
                "app.api.user.router.service.update_user", return_value=updated_user
            )
            responses.add(
                responses.PUT,
                f"/users/{user_id}",
                json=update_user.model_dump_json(),
                status=200,
            )
            response = client.put(
                f"/users/{user_id}", json=update_user.model_dump(by_alias=True)
            )

            assert response.status_code == 200
            updated_user_response = response.json()
            assert updated_user_response["username"] == update_user.username
            assert updated_user_response["email"] == update_user.email
            mock_update_user_service.assert_awaited_once()

        @responses.activate
        def test_update_user__unprocessable_entity(
            self,
            mocker: MockFixture,
            client: TestClient,
            user_id: UUID,
            user_create: UserCreate,
        ) -> None:
            mock_update_user_service = mocker.patch(
                "app.api.user.router.service.update_user"
            )
            response = client.put(
                f"/users/{user_id}", json=user_create.model_dump_json()
            )

            assert response.status_code == 422
            mock_update_user_service.assert_not_awaited()

        @responses.activate
        def test_update_user__not_found(
            self,
            mocker: MockFixture,
            client: TestClient,
            update_user: BaseUser,
            user_id: UUID,
        ) -> None:
            mock_update_user_service = mocker.patch(
                "app.api.user.router.service.update_user",
                side_effect=HTTPException(*USER_NOT_FOUND),
            )
            response = client.put(
                f"/users/{user_id}", json=update_user.model_dump(by_alias=True)
            )

            assert response.status_code == 404
            mock_update_user_service.assert_awaited_once()

    class TestDeleteUser:
        @responses.activate
        def test_delete_user__ok(
            self,
            mocker: MockFixture,
            client: TestClient,
            user_id: UUID,
        ) -> None:
            mock_delete_user_service = mocker.patch(
                "app.api.user.router.service.delete_user", return_value=user_id
            )
            responses.add(responses.DELETE, f"/users/{user_id}", status=200)
            response = client.delete(f"/users/{user_id}")

            assert response.status_code == 200
            deleted_user_id = response.json()
            assert isinstance(UUID(deleted_user_id), UUID)
            assert deleted_user_id == str(user_id)
            mock_delete_user_service.assert_awaited_once()

        @responses.activate
        def test_delete_user__not_found(
            self,
            mocker: MockFixture,
            client: TestClient,
            user_id: UUID,
        ) -> None:
            mock_update_user_service = mocker.patch(
                "app.api.user.router.service.delete_user",
                side_effect=HTTPException(*USER_NOT_FOUND),
            )
            response = client.delete(f"/users/{user_id}")

            assert response.status_code == 404
            mock_update_user_service.assert_awaited_once()
