# 报错信息
/data/server/miniconda3/bin/conda run -n py32 --no-capture-output python /data/server/guozhicai/project/agent-lightning/myexample/basic/basic.py 
Traceback (most recent call last):
  File "/data/server/guozhicai/project/agent-lightning/myexample/basic/basic.py", line 38, in <module>
    asyncio.run(main())
  File "/data/server/miniconda3/envs/py32/lib/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/data/server/miniconda3/envs/py32/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/data/server/miniconda3/envs/py32/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/data/server/guozhicai/project/agent-lightning/myexample/basic/basic.py", line 33, in main
    agl.emit_message("answer", result)
  File "/data/server/guozhicai/project/agent-lightning/agentlightning/emitter/message.py", line 33, in emit_message
    span_attributes.update(attributes)
ValueError: dictionary update sequence element #0 has length 1; 2 is required
ERROR conda.cli.main_run:execute(127): `conda run python /data/server/guozhicai/project/agent-lightning/myexample/basic/basic.py` failed. (See above for error)

Process finished with exit code 1


# emit_message的第二个参数是dict
                result = {"answer": 4}  # 你的 agent 输出
                agl.emit_message("answer", result)