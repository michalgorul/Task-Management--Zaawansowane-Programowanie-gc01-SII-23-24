from uuid import UUID

import responses
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi_pagination import Page
from pytest_mock import MockFixture

from app.api.task.models import BaseTask, Task, TaskCreate
from app.api.task.service import TASK_NOT_FOUND


class TestTaskRoutes:
    class TestCreateTask:
        @responses.activate
        def test_create_task__ok(
            self,
            mocker: MockFixture,
            client: TestClient,
            task: Task,
            task_create: TaskCreate,
        ) -> None:
            mock_create_task_service = mocker.patch(
                "app.api.task.router.service.create_task", return_value=task
            )
            responses.add(
                responses.POST, "/tasks/", json=task.model_dump_json(), status=200
            )
            response = client.post(
                "/tasks/",
                json=task_create.model_dump(mode="json") | {"password": "password1!"},
            )

            assert response.status_code == 200
            created_task = response.json()
            assert created_task["name"] == task_create.name
            assert created_task["description"] == task_create.description
            mock_create_task_service.assert_awaited_once()

        @responses.activate
        def test_create_task__unprocessable_entity(
            self,
            mocker: MockFixture,
            client: TestClient,
            task_create: TaskCreate,
        ) -> None:
            mock_create_task_service = mocker.patch(
                "app.api.task.router.service.create_task"
            )
            response = client.post("/tasks/", json=task_create.model_dump_json())

            assert response.status_code == 422
            mock_create_task_service.assert_not_awaited()

    class TestGetTask:
        @responses.activate
        def test_get_task__ok(
            self, mocker: MockFixture, client: TestClient, task: Task, task_id: UUID
        ) -> None:
            mock_get_task_service = mocker.patch(
                "app.api.task.router.service.get_task", return_value=task
            )
            responses.add(
                responses.GET,
                f"/tasks/{task_id}",
                json=task.model_dump_json(),
                status=200,
            )
            response = client.get(f"/tasks/{task_id}")

            assert response.status_code == 200
            retrieved_task = response.json()
            assert isinstance(UUID(retrieved_task["taskId"]), UUID)
            assert retrieved_task["taskId"] == str(task_id)
            mock_get_task_service.assert_awaited_once()

        @responses.activate
        def test_get_task__not_found(
            self, mocker: MockFixture, client: TestClient, task: Task, task_id: UUID
        ) -> None:
            mock_get_task_service = mocker.patch(
                "app.api.task.router.service.get_task",
                side_effect=HTTPException(*TASK_NOT_FOUND),
            )
            response = client.get(f"/tasks/{task_id}")

            assert response.status_code == 404
            mock_get_task_service.assert_awaited_once()

    class TestGetTasksTask:
        @responses.activate
        def test_get_tasks__ok(
            self,
            mocker: MockFixture,
            client: TestClient,
            task_page: Page[Task],
            task_id: UUID,
            size: int,
        ) -> None:
            mock_get_tasks_service = mocker.patch(
                "app.api.task.router.service.get_tasks", return_value=task_page
            )
            responses.add(
                responses.GET, "/tasks/", json=task_page.model_dump_json(), status=200
            )
            response = client.get("/tasks/")

            assert response.status_code == 200
            assert response.json()["items"][0]["taskId"] == str(task_id)
            assert response.json()["size"] == size
            mock_get_tasks_service.assert_awaited_once()

    class TestUpdateTask:
        @responses.activate
        def test_update_task__ok(
            self,
            mocker: MockFixture,
            client: TestClient,
            task_id: UUID,
            update_task: BaseTask,
            updated_task: Task,
        ) -> None:
            mock_update_task_service = mocker.patch(
                "app.api.task.router.service.update_task", return_value=updated_task
            )
            responses.add(
                responses.PUT,
                f"/tasks/{task_id}",
                json=update_task.model_dump_json(),
                status=200,
            )
            response = client.put(
                f"/tasks/{task_id}", json=update_task.model_dump(by_alias=True)
            )

            assert response.status_code == 200
            updated_task_response = response.json()
            assert updated_task_response["name"] == update_task.name
            assert updated_task_response["description"] == update_task.description
            mock_update_task_service.assert_awaited_once()

        @responses.activate
        def test_update_task__unprocessable_entity(
            self,
            mocker: MockFixture,
            client: TestClient,
            task_id: UUID,
            task_create: TaskCreate,
        ) -> None:
            mock_update_task_service = mocker.patch(
                "app.api.task.router.service.update_task"
            )
            response = client.put(
                f"/tasks/{task_id}", json=task_create.model_dump_json()
            )

            assert response.status_code == 422
            mock_update_task_service.assert_not_awaited()

        @responses.activate
        def test_update_task__not_found(
            self,
            mocker: MockFixture,
            client: TestClient,
            update_task: BaseTask,
            task_id: UUID,
        ) -> None:
            mock_update_task_service = mocker.patch(
                "app.api.task.router.service.update_task",
                side_effect=HTTPException(*TASK_NOT_FOUND),
            )
            response = client.put(
                f"/tasks/{task_id}", json=update_task.model_dump(by_alias=True)
            )

            assert response.status_code == 404
            mock_update_task_service.assert_awaited_once()

    class TestDeleteTask:
        @responses.activate
        def test_delete_task__ok(
            self,
            mocker: MockFixture,
            client: TestClient,
            task_id: UUID,
        ) -> None:
            mock_delete_task_service = mocker.patch(
                "app.api.task.router.service.delete_task", return_value=task_id
            )
            responses.add(responses.DELETE, f"/tasks/{task_id}", status=200)
            response = client.delete(f"/tasks/{task_id}")

            assert response.status_code == 200
            deleted_task_id = response.json()
            assert isinstance(UUID(deleted_task_id), UUID)
            assert deleted_task_id == str(task_id)
            mock_delete_task_service.assert_awaited_once()

        @responses.activate
        def test_delete_task__not_found(
            self,
            mocker: MockFixture,
            client: TestClient,
            task_id: UUID,
        ) -> None:
            mock_update_task_service = mocker.patch(
                "app.api.task.router.service.delete_task",
                side_effect=HTTPException(*TASK_NOT_FOUND),
            )
            response = client.delete(f"/tasks/{task_id}")

            assert response.status_code == 404
            mock_update_task_service.assert_awaited_once()
