from lightflow.tasks.base import BaseTask


class TestDepBaseTask:
    def test_rshift_operators_simple_task(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task1 >> task2 >> task3
        assert task1.downstream_tasks == {"task2": task2}
        assert task2.upstream_tasks == {"task1": task1}
        assert task2.downstream_tasks == {"task3": task3}
        assert task3.upstream_tasks == {"task2": task2}

    def test_rshift_operators_list_of_tasks(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task4 = BaseTask(task_id="task4")
        task1 >> [task2, task3] >> task4
        assert task1.downstream_tasks == {"task2": task2, "task3": task3}
        assert task2.upstream_tasks == {"task1": task1}
        assert task2.downstream_tasks == {"task4": task4}
        assert task3.upstream_tasks == {"task1": task1}
        assert task3.downstream_tasks == {"task4": task4}
        assert task4.upstream_tasks == {"task2": task2, "task3": task3}

    def test_lshift_operators_simple_task(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task1 << task2 << task3
        assert task1.upstream_tasks == {"task2": task2}
        assert task2.downstream_tasks == {"task1": task1}
        assert task2.upstream_tasks == {"task3": task3}
        assert task3.downstream_tasks == {"task2": task2}

    def test_lshift_operators_list_of_tasks(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task4 = BaseTask(task_id="task4")
        task1 << [task2, task3] << task4
        assert task1.upstream_tasks == {"task2": task2, "task3": task3}
        assert task2.downstream_tasks == {"task1": task1}
        assert task2.upstream_tasks == {"task4": task4}
        assert task3.downstream_tasks == {"task1": task1}
        assert task3.upstream_tasks == {"task4": task4}
        assert task4.downstream_tasks == {"task2": task2, "task3": task3}

    def test_mix_rshift_lshift_operators_simple_task(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task1 >> task2 << task3
        assert task1.downstream_tasks == {"task2": task2}
        assert task2.upstream_tasks == {"task1": task1, "task3": task3}
        assert task3.downstream_tasks == {"task2": task2}

    def test_mix_rshift_lshift_operators_list_of_tasks(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task4 = BaseTask(task_id="task4")
        task1 >> [task2, task3] << task4
        assert task1.downstream_tasks == {"task2": task2, "task3": task3}
        assert task2.upstream_tasks == {"task1": task1, "task4": task4}
        assert task2.downstream_tasks == {}
        assert task3.upstream_tasks == {"task1": task1, "task4": task4}
        assert task3.downstream_tasks == {}
        assert task4.downstream_tasks == {"task2": task2, "task3": task3}

    def test_mix_rshift_lshift_operators_list_multiple_line(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task4 = BaseTask(task_id="task4")
        task5 = BaseTask(task_id="task5")
        task6 = BaseTask(task_id="task6")
        task1 >> [task2, task3] << task4
        task4 >> [task5, task6]
        assert task1.downstream_tasks == {"task2": task2, "task3": task3}
        assert task2.upstream_tasks == {"task1": task1, "task4": task4}
        assert task2.downstream_tasks == {}
        assert task3.upstream_tasks == {"task1": task1, "task4": task4}
        assert task3.downstream_tasks == {}
        assert task4.downstream_tasks == {"task2": task2, "task3": task3, "task5": task5, "task6": task6}
        assert task4.upstream_tasks == {}
        assert task5.downstream_tasks == {}
        assert task5.upstream_tasks == {"task4": task4}
        assert task6.downstream_tasks == {}
        assert task6.upstream_tasks == {"task4": task4}

    def test_set_downstream_task(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task1.set_downstream(task2)
        task1.set_downstream(task3)
        assert task1.downstream_tasks == {"task2": task2, "task3": task3}
        assert task2.upstream_tasks == {"task1": task1}
        assert task3.upstream_tasks == {"task1": task1}

    def test_set_downstream_list(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task4 = BaseTask(task_id="task4")
        task1.set_downstream([task2, task3])
        task1.set_downstream(task4)
        assert task1.downstream_tasks == {"task2": task2, "task3": task3, "task4": task4}
        assert task2.upstream_tasks == {"task1": task1}
        assert task3.upstream_tasks == {"task1": task1}
        assert task4.upstream_tasks == {"task1": task1}

    def test_set_upstream_task(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task1.set_upstream(task2)
        task1.set_upstream(task3)
        assert task1.upstream_tasks == {"task2": task2, "task3": task3}
        assert task2.downstream_tasks == {"task1": task1}
        assert task3.downstream_tasks == {"task1": task1}

    def test_set_upstream_list(self):
        task1 = BaseTask(task_id="task1")
        task2 = BaseTask(task_id="task2")
        task3 = BaseTask(task_id="task3")
        task4 = BaseTask(task_id="task4")
        task1.set_upstream([task2, task3])
        task1.set_upstream(task4)
        assert task1.upstream_tasks == {"task2": task2, "task3": task3, "task4": task4}
        assert task2.downstream_tasks == {"task1": task1}
        assert task3.downstream_tasks == {"task1": task1}
        assert task4.downstream_tasks == {"task1": task1}
