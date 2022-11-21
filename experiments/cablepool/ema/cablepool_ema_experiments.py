from functools import partial

from cablepool_definitions import BATTERY_ENERGY_COST_RANGE, PV_COST_RANGE
from cablepool_leso_handshake import COLLECTION, METRICS, RESULTS_FOLDER, CablePooling
from ema_workbench import (
    CategoricalParameter,
    Model,
    MultiprocessingEvaluator,
    RealParameter,
    ScalarOutcome,
    SequentialEvaluator,
    ema_logging,
    save_results,
)
from ema_workbench.em_framework.evaluators import FullFactorialSampler

RATIO_SCENARIOS = ["high_ratio", "low_ratio", "both_ratios"]


if __name__ == "__main__":

    # initiate model
    ema_logging.log_to_stderr(ema_logging.INFO)

    run_ID = input("Please enter the run ID:")
    initialized_model = partial(CablePooling, run_ID=run_ID)
    model = Model(name=f"{COLLECTION.split('_')[0]}", function=initialized_model)

    # uncertainties / scenarios
    model.uncertainties = [
        RealParameter("pv_cost", *PV_COST_RANGE),
        RealParameter("battery_cost", *BATTERY_ENERGY_COST_RANGE),
    ]
    model.levers = [CategoricalParameter("dc_ratio", RATIO_SCENARIOS)]
    # specify outcomes
    model.outcomes = [ScalarOutcome(metric) for metric in METRICS]

    debug = False
    # run experiments
    if debug is False:
        with MultiprocessingEvaluator(model, n_processes=6) as evaluator:
            results = evaluator.perform_experiments(
                scenarios=32,
                policies=len(RATIO_SCENARIOS),
                uncertainty_sampling=FullFactorialSampler(),
            )
    else:
        with SequentialEvaluator(model) as evaluator:
            results = evaluator.perform_experiments(
                scenarios=2, policies=2, uncertainty_sampling=FullFactorialSampler()
            )

    # save results
    results_file_name = RESULTS_FOLDER / f"{COLLECTION}_ema_results_{run_ID}.tar.gz"
    save_results(results, file_name=results_file_name)
