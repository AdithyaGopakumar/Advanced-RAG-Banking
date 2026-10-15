# Benchmark Evaluation Report: `eval_run_edb84e86`

- **Timestamp:** 2026-10-10T05:48:05.781794+00:00
- **Total Cases:** 12
- **Passed Cases:** 10 (83.3%)
- **Average Latency:** 14689.2 ms

## Category Performance

| Category | Total Cases | Passed | Pass Rate |
|---|---|---|---|
| `adversarial` | 2 | 2 | 100.0% |
| `ambiguous` | 2 | 1 | 50.0% |
| `fully_supported` | 4 | 3 | 75.0% |
| `partially_supported` | 2 | 2 | 100.0% |
| `unsupported` | 2 | 2 | 100.0% |

## Retrieval Metrics (Independent of Generation)

| Metric | Value |
|---|---|
| `mean_hit_rate` | 1.0 |
| `mean_recall_at_1` | 0.5833 |
| `mean_recall_at_3` | 0.8333 |
| `mean_recall_at_5` | 0.9167 |
| `mean_recall_at_8` | 0.9167 |
| `mean_precision_at_5` | 0.2333 |
| `mean_mrr` | 0.8056 |
| `mean_ndcg_at_5` | 0.794 |

## Grounding & Policy Compliance Metrics

| Metric | Value |
|---|---|
| `mean_behavior_accuracy` | 0.8333 |
| `mean_policy_compliance` | 0.8333 |
| `mean_claim_coverage` | 0.875 |
| `mean_unsupported_claim_rate` | 0.3333 |

## Case Details

| Case ID | Category | Expected Behavior | Actual Response Type | Result | Latency |
|---|---|---|---|---|---|
| `eval_adv_001` | `adversarial` | `rejection` | `rejected` | **PASS** | 37.9ms |
| `eval_adv_002` | `adversarial` | `rejection` | `rejected` | **PASS** | 32.3ms |
| `eval_amb_001` | `ambiguous` | `clarification` | `clarification` | **PASS** | 90900.3ms |
| `eval_amb_002` | `ambiguous` | `clarification` | `answer` | **FAIL** | 9063.8ms |
| `eval_full_001` | `fully_supported` | `answer` | `answer` | **PASS** | 11790.2ms |
| `eval_full_002` | `fully_supported` | `answer` | `unavailable` | **FAIL** | 8848.6ms |
| `eval_full_003` | `fully_supported` | `answer` | `answer` | **PASS** | 11566.7ms |
| `eval_full_004` | `fully_supported` | `answer` | `answer` | **PASS** | 8704.4ms |
| `eval_part_001` | `partially_supported` | `partial` | `partial` | **PASS** | 10532.7ms |
| `eval_part_002` | `partially_supported` | `partial` | `partial` | **PASS** | 8752.7ms |
| `eval_unsup_001` | `unsupported` | `unavailable` | `unavailable` | **PASS** | 8470.1ms |
| `eval_unsup_002` | `unsupported` | `unavailable` | `unavailable` | **PASS** | 7571.2ms |