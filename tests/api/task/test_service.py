from uuid import UUID

import pytest
from fastapi import HTTPException
from fastapi_pagination import Page, Params
from pytest_mock import MockFixture
from sqlalchemy.orm import Session

from app.api.task import service
from app.api.task.models import BaseTask, Task, TaskCreate, TaskUpdate
from app.api.task.service import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
)
from app.database.task.models import TaskTable


class TestTaskServices:
    class TestCreateTask:
        @pytest.mark.asyncio
        async def test_create_task__ok(
            self,
            mocker: MockFixture,
            db: Session,
            task_create: TaskCreate,
            task_table: TaskTable,
            task: Task,
        ) -> None:
            mock_create_task_crud = mocker.patch(
                "app.api.task.service.crud.create_task", return_value=task_table
            )
            created_task = await create_task(task_create, db)

            assert created_task == task
            mock_create_task_crud.assert_called_once_with(task_create, db)

        @pytest.mark.asyncio
        async def test_create_task__common_exception(
            self,
            mocker: MockFixture,
            db: Session,
            task_create: TaskCreate,
            task_table: TaskTable,
            task: Task,
        ) -> None:
            mock_create_task_crud = mocker.patch(
                "app.api.task.service.crud.create_task", side_effect=Exception()
            )
            with pytest.raises(Exception) as e:
                await create_task(task_create, db)

            assert e.value.status_code == 500
            mock_create_task_crud.assert_called_once_with(task_create, db)

    class TestGetTask:
        @pytest.mark.asyncio
        async def test_get_task__ok(
            self,
            mocker: MockFixture,
            db: Session,
            task: Task,
            task_id: UUID,
            task_table: TaskTable,
        ) -> None:
            mock_get_task_crud = mocker.patch(
                "app.api.task.service.crud.get_task", return_value=[task_table]
            )
            retrieved_task = await get_task(task_id, db)

            assert retrieved_task.task_id == task_id
            assert retrieved_task == task
            mock_get_task_crud.assert_called_once_with(task_id, db)

        @pytest.mark.asyncio
        async def test_get_task__not_found(
            self,
            mocker: MockFixture,
            db: Session,
            task: Task,
            task_id: UUID,
            task_table: TaskTable,
        ) -> None:
            mock_get_task_crud = mocker.patch(
                "app.api.task.service.crud.get_task", return_value=[]
            )
            with pytest.raises(HTTPException) as e:
                await get_task(task_id, db)

            assert e.value.status_code == 404
            mock_get_task_crud.assert_called_once_with(task_id, db)

    class TestGetTasksTask:
        @pytest.mark.asyncio
        async def test_get_tasks__ok(
            self,
            mocker: MockFixture,
            db: Session,
            task_page: Page[Task],
            task_id: UUID,
            size: int,
        ) -> None:
            mock_get_tasks_crud = mocker.patch(
                "app.api.task.service.crud.get_tasks", return_value=task_page
            )
            pagination = Params()
            retrieved_tasks = await get_tasks(pagination, db)

            assert retrieved_tasks.items[0].task_id == task_id
            assert retrieved_tasks.size == size
            mock_get_tasks_crud.assert_called_once_with(pagination, db)

    class TestUpdateTask:
        @pytest.mark.asyncio
        async def test_update_task__ok(
            self,
            mocker: MockFixture,
            db: Session,
            task_id: UUID,
            update_task: TaskUpdate,
            updated_task: Task,
        ) -> None:
            mock_update_task_crud = mocker.patch(
                "app.api.task.service.crud.update_task", return_value=1
            )
            mock_get_task = mocker.patch(
                "app.api.task.service.crud.get_task",
                return_value=[TaskTable(**updated_task.model_dump())],
            )
            updated_task_service = await service.update_task(task_id, update_task, db)

            assert updated_task_service == updated_task
            mock_update_task_crud.assert_called_once_with(
                task_id=task_id, new_task=update_task, db=db
            )
            mock_get_task.assert_called_once_with(task_id, db)

        @pytest.mark.asyncio
        async def test_update_task__common_exception(
            self,
            mocker: MockFixture,
            db: Session,
            task_id: UUID,
            update_task: TaskUpdate,
        ) -> None:
            mock_update_task_crud = mocker.patch(
                "app.api.task.service.crud.update_task", side_effect=Exception()
            )
            with pytest.raises(HTTPException) as e:
                await service.update_task(task_id, update_task, db)

            assert e.value.status_code == 500
            mock_update_task_crud.assert_called_once_with(
                task_id=task_id, new_task=update_task, db=db
            )

        @pytest.mark.asyncio
        async def test_update_task__not_found(
            self,
            mocker: MockFixture,
            db: Session,
            update_task: BaseTask,
            task_id: UUID,
        ) -> None:
            mock_update_task_crud = mocker.patch(
                "app.api.task.service.crud.update_task",
                return_value=0,
            )
            with pytest.raises(HTTPException) as e:
                await service.update_task(task_id, update_task, db)

            assert e.value.status_code == 404
            mock_update_task_crud.assert_called_once_with(
                task_id=task_id, new_task=update_task, db=db
            )

    class TestDeleteTask:
        @pytest.mark.asyncio
        async def test_delete_task__ok(
            self,
            mocker: MockFixture,
            db: Session,
            task_id: UUID,
            task_table: TaskTable,
        ) -> None:
            mock_get_task_crud = mocker.patch(
                "app.api.task.service.crud.get_task", return_value=[task_table]
            )
            mock_delete_task_crud = mocker.patch(
                "app.api.task.service.crud.delete_task", return_value=task_id
            )
            deleted_task_id = await delete_task(task_id, db)

            assert deleted_task_id == task_id
            mock_get_task_crud.assert_called_once_with(task_id, db)
            mock_delete_task_crud.assert_called_once_with(task_id, db)

        @pytest.mark.asyncio
        async def test_delete_task__common_exception(
            self,
            mocker: MockFixture,
            db: Session,
            task_id: UUID,
            task_table: TaskTable,
        ) -> None:
            mock_get_task_crud = mocker.patch(
                "app.api.task.service.crud.get_task", return_value=[task_table]
            )
            mock_delete_task_crud = mocker.patch(
                "app.api.task.service.crud.delete_task", side_effect=Exception
            )
            with pytest.raises(HTTPException) as e:
                await delete_task(task_id, db)

            assert e.value.status_code == 500
            mock_get_task_crud.assert_called_once_with(task_id, db)
            mock_delete_task_crud.assert_called_once_with(task_id, db)

        @pytest.mark.asyncio
        async def test_delete_task__not_found(
            self,
            mocker: MockFixture,
            db: Session,
            task_id: UUID,
            task_table: TaskTable,
        ) -> None:
            mock_get_task_crud = mocker.patch(
                "app.api.task.service.crud.get_task", return_value=[]
            )
            mock_delete_task_crud = mocker.patch(
                "app.api.task.service.crud.delete_task"
            )
            with pytest.raises(HTTPException) as e:
                await delete_task(task_id, db)

            assert e.value.status_code == 404
            mock_get_task_crud.assert_called_once_with(task_id, db)
            mock_delete_task_crud.assert_not_called()
