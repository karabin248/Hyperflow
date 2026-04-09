from hyperflow.memory.session_memory import SESSION_MEMORY, SessionRecord


def test_session_memory_add_and_read():
    SESSION_MEMORY.clear()

    SESSION_MEMORY.add_record(
        SessionRecord(
            run_id="r1",
            raw_input="test input",
            intent="planning",
            mode="fusion",
            summary="test summary",
            observer_status="OK",
        )
    )

    recent = SESSION_MEMORY.get_recent()
    assert len(recent) == 1
    assert recent[0].intent == "planning"