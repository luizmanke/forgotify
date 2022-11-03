from pipelines import batch_database_update


def test_pipeline():

    result = batch_database_update.pipeline.execute_in_process()

    assert result.success
    assert result.output_for_node("get_number") == 200
