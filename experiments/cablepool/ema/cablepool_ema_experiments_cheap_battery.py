from functools import partial
from ema_workbench import (
    save_results,
    RealParameter,
    CategoricalParameter,
    ScalarOutcome,
    Constant,
    Model,
    ema_logging,
    MultiprocessingEvaluator,
    SequentialEvaluator,
)
from cablepool_leso_handshake import METRICS, RESULTS_FOLDER, CablePooling, COLLECTION



if __name__ == "__main__":
    
    # initiate model
    ema_logging.log_to_stderr(ema_logging.INFO)
    
    run_ID = input('Please enter the run ID:')
    APPROACH = "cheap_battery"
    initialized_model = partial(CablePooling, run_ID=run_ID, approach=APPROACH)
    model = Model(name=f"{COLLECTION}", function=initialized_model)

    # uncertainties / scenarios
    model.uncertainties = [
        RealParameter("pv_cost_factor", 0.38, 0.85),
        RealParameter("battery_cost_factor", 0.1, 0.41),
    ]
    # specify outcomes
    model.outcomes = [ScalarOutcome(metric) for metric in METRICS]

    # run experiments
    with MultiprocessingEvaluator(model, n_processes=2) as evaluator:
        results = evaluator.perform_experiments(scenarios=200)
    
    # save results
    results_file_name = RESULTS_FOLDER / f"{COLLECTION}_ema_results_{run_ID}.tar.gz"
    save_results(results, file_name=results_file_name)

