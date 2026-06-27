# Run list

Generated: 2026-06-23 17:57 UTC

W&B project: `marl-traffic-gat`

Requested tags: `baseline`, `fgsv2`, `fgs_ablation`, `fgsv3`

Total matching runs: **70**

Metric columns prefer `best_validation/*`, then fall back to `validation/*`, `best_train/*`, and `train/*` when needed.

## Summary

| Tag | Runs |
|---|---:|
| `baseline` | 42 |
| `fgsv2` | 4 |
| `fgs_ablation` | 15 |
| `fgsv3` | 9 |

| Scenario | Runs |
|---|---:|
| `cologne1` | 12 |
| `cologne3` | 8 |
| `cologne8` | 16 |
| `ingolstadt1` | 10 |
| `ingolstadt7` | 9 |
| `ingolstadt21` | 15 |

## cologne1

| Family | Algorithm | Variant | Run | Tags | State | Created | Episode | Wait | Delay | Queue | Trip | Source |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Baseline | `colight` | `colight__045507` | [0nw8244o](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/0nw8244o) | `baseline` | finished | 2026-06-04 | 200 | 15.921 | 36.962 | 8.172 | 53.544 | `validation` |
| Baseline | `dqn` | `dqn__013136` | [ophtbgjo](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/ophtbgjo) | `baseline` | finished | 2026-06-04 | 200 | 8.367 | 28.146 | 4.56 | 45.821 | `validation` |
| Baseline | `fixed_time` | `fixed_time` | [tze5f2wx](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/tze5f2wx) | `baseline` | finished | 2026-06-04 | 5 | 28.693 | 54.613 | 15.53 | 65.608 | `validation` |
| Baseline | `frap` | `frap__045507` | [40q4hqct](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/40q4hqct) | `baseline` | finished | 2026-06-04 | 200 | 10.56 | 31.723 | 4.857 | 49.307 | `validation` |
| Baseline | `ppo` | `ppo__013258` | [9dgtkbpe](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/9dgtkbpe) | `baseline` | finished | 2026-06-04 | 200 | 5.137 | 22.769 | 2.717 | 40.501 | `validation` |
| Baseline | `sac_builtin` | `sac_builtin__011224` | [55onx74j](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/55onx74j) | `baseline` | finished | 2026-06-09 | 175 | 5.057 | 22.989 | 2.742 | 40.714 | `best_validation` |
| Baseline | `static_max_pressure` | `static_max_pressure` | [frxn9jus](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/frxn9jus) | `baseline` | finished | 2026-06-04 | 5 | 5.854 | 24.201 | 2.91 | 41.779 | `validation` |
| FGS ablation | `fgs` | `fgs_mlp_gat_sac` | [qrr5n53z](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/qrr5n53z) | `fgs_ablation` | finished | 2026-06-04 | 200 | 5.321 | 22.703 | 2.601 | 40.365 | `validation` |
| FGS ablation | `fgs` | `fgs_mlp_gatv2_sac` | [wssbl2w1](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/wssbl2w1) | `fgs_ablation` | finished | 2026-06-05 | 200 | 5.385 | 23.047 | 2.627 | 40.647 | `validation` |
| FGS ablation | `fgs_ppo` | `fgs_mlp_gatv2_ppo` | [dand0e2u](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/dand0e2u) | `fgs_ablation` | finished | 2026-06-20 | 35 | 1.06 | 12.494 | 120.703 | 26.442 | `best_validation` |
| FGSv2 | `fgsv2` | `fgsv2_sac` | [69gslqo1](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/69gslqo1) | `fgsv2` | finished | 2026-06-20 | 5 | 0.381 | 11.957 | 43.716 | 33.648 | `best_validation` |
| FGSv3 | `fgsv3` | `fgsv3_frap_gatv2_sac` | [coq3f9ve](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/coq3f9ve) | `fgsv3` | finished | 2026-06-20 | 5 | 0.381 | 11.957 | 43.716 | 33.648 | `best_validation` |

## cologne3

| Family | Algorithm | Variant | Run | Tags | State | Created | Episode | Wait | Delay | Queue | Trip | Source |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Baseline | `colight` | `colight__170149` | [xvq79dqi](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/xvq79dqi) | `baseline` | finished | 2026-06-07 | 200 | 7.897 | 21.938 | 0.998 | 57.736 | `validation` |
| Baseline | `dqn` | `dqn__130122` | [z0kuqwt0](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/z0kuqwt0) | `baseline` | finished | 2026-06-07 | 200 | 93.547 | 127.174 | 7.645 | 139.989 | `validation` |
| Baseline | `fixed_time` | `fixed_time` | [pmc74urj](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/pmc74urj) | `baseline` | finished | 2026-06-04 | 5 | 43.592 | 63.645 | 5.679 | 93.845 | `validation` |
| Baseline | `frap` | `frap__170149` | [r7og9ssz](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/r7og9ssz) | `baseline` | finished | 2026-06-07 | 200 | 18.556 | 39.837 | 2.783 | 71.132 | `validation` |
| Baseline | `ppo` | `ppo__130122` | [2olasa0c](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/2olasa0c) | `baseline` | finished | 2026-06-07 | 200 | 6.454 | 20.288 | 0.826 | 56.543 | `validation` |
| Baseline | `sac_builtin` | `sac_builtin__234452` | [10782649](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/10782649) | `baseline` | finished | 2026-06-10 | 165 | 5.543 | 18.899 | 0.767 | 55.11 | `best_validation` |
| Baseline | `static_max_pressure` | `static_max_pressure` | [8ok6nhdb](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/8ok6nhdb) | `baseline` | finished | 2026-06-04 | 5 | 31.786 | 56.371 | 3.367 | 81.588 | `validation` |
| FGS ablation | `fgs_ppo` | `fgs_mlp_gatv2_ppo` | [e268c0c4](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/e268c0c4) | `fgs_ablation` | finished | 2026-06-20 | 5 | 0.081 | 6.943 | 46.087 | 37.747 | `best_validation` |

## cologne8

| Family | Algorithm | Variant | Run | Tags | State | Created | Episode | Wait | Delay | Queue | Trip | Source |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Baseline | `colight` | `colight__191734` | [uvf3nu0e](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/uvf3nu0e) | `baseline` | finished | 2026-06-07 | 200 | 23.786 | 51.836 | 1.632 | 105.681 | `validation` |
| Baseline | `dqn` | `dqn__225548` | [q1fs0t7e](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/q1fs0t7e) | `baseline` | finished | 2026-06-10 | 140 | 6.711 | 25.55 | 0.464 | 89.792 | `best_validation` |
| Baseline | `fixed_time` | `fixed_time` | [mgol3a84](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/mgol3a84) | `baseline` | finished | 2026-06-04 | 5 | 30.266 | 51.519 | 2.176 | 115.66 | `validation` |
| Baseline | `frap` | `frap__183855` | [rh0cys0s](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/rh0cys0s) | `baseline` | finished | 2026-06-07 | 200 | 17.105 | 44.854 | 1.204 | 108.555 | `validation` |
| Baseline | `ppo` | `ppo__175652` | [ai3kzhl8](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/ai3kzhl8) | `baseline` | finished | 2026-06-07 | 200 | 4.856 | 21.862 | 0.325 | 86.112 | `validation` |
| Baseline | `sac_builtin` | `sac_builtin__010956` | [fs9843sk](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/fs9843sk) | `baseline` | finished | 2026-06-10 | 149 | 4.728 | 21.77 | 0.329 | 86.037 | `best_validation` |
| Baseline | `static_max_pressure` | `static_max_pressure` | [1c8l6ojg](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/1c8l6ojg) | `baseline` | finished | 2026-06-04 | 5 | 159.541 | 257.903 | 10.584 | 231.399 | `validation` |
| FGS ablation | `fgs` | `fgs_mlp_gatv2_sac` | [m0pvd51d](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/m0pvd51d) | `fgs_ablation` | finished | 2026-06-13 | 35 | 4.927 | 22.202 | 0.343 | 86.416 | `best_validation` |
| FGS ablation | `fgs_ppo` | `fgs_frap_gatv2_ppo` | [2t9zorx4](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/2t9zorx4) | `fgs_ablation` | finished | 2026-06-13 | 190 | 6.687 | 24.619 | 0.467 | 88.882 | `best_validation` |
| FGS ablation | `fgs_ppo` | `fgs_mlp_gat_ppo` | [cs3hekkt](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/cs3hekkt) | `fgs_ablation` | finished | 2026-06-13 | 200 | 6.724 | 24.892 | 0.466 | 89.105 | `best_validation` |
| FGS ablation | `fgs_ppo` | `fgs_mlp_gatv2_ppo` | [5qnfc0c0](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/5qnfc0c0) | `fgs_ablation` | finished | 2026-06-13 | 130 | 6.25 | 24.025 | 0.437 | 88.308 | `best_validation` |
| FGSv2 | `fgsv2` | `fgsv2_sac` | [j6utvuvh](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/j6utvuvh) | `fgsv2` | finished | 2026-06-17 | 5 | 0.359 | 10.081 | 26.138 | 59.667 | `best_validation` |
| FGSv3 | `fgsv3` | `fgsv3_frap_gatv2_sac` | [3efrqs9n](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/3efrqs9n) | `fgsv3` | finished | 2026-06-17 | 194 | 6.178 | 26.529 | 0.428 | 90.718 | `best_validation` |
| FGSv3 | `fgsv3` | `fgsv3_frap_gatv2_sac_presslight_rescofix` | [ax41fc7a](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/ax41fc7a) | `fgsv3` | finished | 2026-06-22 | 194 | 82.546 | 112.747 | 2.923 | 168.212 | `best_validation` |
| FGSv3 | `fgsv3` | `fgsv3_frap_gatv2_sac_ti4_big` | [spr06wpk](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/spr06wpk) | `fgsv3` | finished | 2026-06-22 | 20 | 0.185 | 10.06 | 36.374 | 55.221 | `best_validation` |
| FGSv3 | `fgsv3_ppo` | `fgsv3_frap_gatv2_ppo` | [73f4ilpr](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/73f4ilpr) | `fgsv3` | finished | 2026-06-17 | 195 | 4.79 | 21.561 | 0.335 | 86.033 | `best_validation` |

## ingolstadt1

| Family | Algorithm | Variant | Run | Tags | State | Created | Episode | Wait | Delay | Queue | Trip | Source |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Baseline | `colight` | `colight__225554` | [uy44xufm](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/uy44xufm) | `baseline` | finished | 2026-06-10 | 145 | 5.322 | 22.433 | 1.52 | 36.484 | `best_validation` |
| Baseline | `dqn` | `dqn__150121` | [eft1am1g](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/eft1am1g) | `baseline` | finished | 2026-06-11 | 100 | 4.681 | 21.754 | 1.096 | 35.667 | `best_validation` |
| Baseline | `fixed_time` | `fixed_time` | [2no5xp6c](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/2no5xp6c) | `baseline` | finished | 2026-06-04 | 5 | 20.284 | 40.784 | 7.363 | 54.42 | `validation` |
| Baseline | `frap` | `frap__200110` | [yigu017p](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/yigu017p) | `baseline` | finished | 2026-06-09 | 200 | 7.338 | 26.633 | 1.67 | 40.097 | `validation` |
| Baseline | `ppo` | `ppo__192243` | [m6mpgfye](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/m6mpgfye) | `baseline` | finished | 2026-06-09 | 200 | 5.22 | 22.448 | 0.926 | 36.023 | `validation` |
| Baseline | `sac_builtin` | `sac_builtin__234428` | [d2umfmr3](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/d2umfmr3) | `baseline` | finished | 2026-06-10 | 192 | 4.915 | 22.328 | 1.079 | 35.955 | `best_validation` |
| Baseline | `static_max_pressure` | `static_max_pressure` | [spirh5gs](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/spirh5gs) | `baseline` | finished | 2026-06-04 | 5 | 6.659 | 25.252 | 1.296 | 38.532 | `validation` |
| FGS ablation | `fgs_ppo` | `fgs_mlp_gatv2_ppo` | [ydbyxzgn](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/ydbyxzgn) | `fgs_ablation` | finished | 2026-06-20 | 10 | 2.683 | 17.95 | 2.54 | 27.928 | `best_validation` |
| FGSv2 | `fgsv2` | `fgsv2_sac` | [imt49gsi](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/imt49gsi) | `fgsv2` | finished | 2026-06-20 | 5 | 2.14 | 17.441 | 2.546 | 27.352 | `best_validation` |
| FGSv3 | `fgsv3` | `fgsv3_frap_gatv2_sac` | [0fe4qytm](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/0fe4qytm) | `fgsv3` | finished | 2026-06-20 | 5 | 2.14 | 17.441 | 2.546 | 27.352 | `best_validation` |

## ingolstadt7

| Family | Algorithm | Variant | Run | Tags | State | Created | Episode | Wait | Delay | Queue | Trip | Source |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Baseline | `colight` | `colight__225557` | [sxwqxqk2](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/sxwqxqk2) | `baseline` | finished | 2026-06-10 | 70 | 17.478 | 47.044 | 1.217 | 78.642 | `best_validation` |
| Baseline | `dqn` | `dqn__225538` | [gjt94c26](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/gjt94c26) | `baseline` | finished | 2026-06-10 | 165 | 9.429 | 34.354 | 0.813 | 71.723 | `best_validation` |
| Baseline | `fixed_time` | `fixed_time` | [zaizq4iq](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/zaizq4iq) | `baseline` | finished | 2026-06-04 | 5 | 66.089 | 122.883 | 5.162 | 135.526 | `validation` |
| Baseline | `frap` | `frap` | [63n81pxb](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/63n81pxb) | `baseline` | finished | 2026-06-17 | 45 | 9.339 | 29.8 | 17.989 | 65.23 | `best_validation` |
| Baseline | `ppo` | `ppo__002947` | [6omllzzz](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/6omllzzz) | `baseline` | finished | 2026-06-21 | 160 | 5.387 | 24.125 | 0.381 | 64.611 | `best_validation` |
| Baseline | `sac_builtin` | `sac_builtin__031010` | [qupw42rl](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/qupw42rl) | `baseline` | finished | 2026-06-16 | 74 | 5.519 | 24.006 | 0.522 | 64.372 | `best_validation` |
| Baseline | `static_max_pressure` | `static_max_pressure` | [cndug0p6](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/cndug0p6) | `baseline` | finished | 2026-06-04 | 5 | 12.534 | 212.698 | 0.492 | 66.888 | `validation` |
| FGS ablation | `fgs` | `fgs_mlp_gatv2_sac` | [a3a0xacw](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/a3a0xacw) | `fgs_ablation` | finished | 2026-06-21 | 42 | 4.765 | 17.111 | 11.787 | 52.662 | `best_validation` |
| FGS ablation | `fgs_ppo` | `fgs_mlp_gatv2_ppo` | [9z2qj178](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/9z2qj178) | `fgs_ablation` | finished | 2026-06-20 | 105 | 6.756 | 26.108 | 0.495 | 66.522 | `best_validation` |

## ingolstadt21

| Family | Algorithm | Variant | Run | Tags | State | Created | Episode | Wait | Delay | Queue | Trip | Source |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Baseline | `colight` | `colight__225601` | [nxssu8q6](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/nxssu8q6) | `baseline` | finished | 2026-06-10 | 150 | 120.784 | 216.79 | 2.547 | 302.088 | `best_validation` |
| Baseline | `dqn` | `dqn__030625` | [ib1b0jol](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/ib1b0jol) | `baseline` | finished | 2026-06-16 | 10 | 33.784 | 78.664 | 2.178 | 220.409 | `best_validation` |
| Baseline | `fixed_time` | `fixed_time` | [k9p5r2sh](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/k9p5r2sh) | `baseline` | finished | 2026-06-04 | 5 | 96.38 | 145.716 | 3.166 | 281.831 | `validation` |
| Baseline | `frap` | `frap` | [jb9fjrha](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/jb9fjrha) | `baseline` | finished | 2026-06-17 | 125 | 50.982 | 101.451 | 7.242 | 232.451 | `best_validation` |
| Baseline | `ppo` | `ppo__014830` | [1twrrwys](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/1twrrwys) | `baseline` | finished | 2026-06-16 | 200 | 25.745 | 67.156 | 4.766 | 206.999 | `best_validation` |
| Baseline | `sac_builtin` | `sac_builtin__030643` | [lwtr8dq7](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/lwtr8dq7) | `baseline` | finished | 2026-06-16 | 5 | 28.999 | 64.605 | 8.932 | 202.57 | `best_validation` |
| Baseline | `static_max_pressure` | `static_max_pressure` | [ydj3q20u](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/ydj3q20u) | `baseline` | finished | 2026-06-04 | 5 | 68.349 | 214.415 | 1.231 | 235.514 | `validation` |
| FGS ablation | `fgs` | `fgs_mlp_gatv2_sac` | [p9c88rhu](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/p9c88rhu) | `fgs_ablation` | finished | 2026-06-21 | 21 | 9.351 | 39.117 | 12.869 | 175.19 | `best_validation` |
| FGS ablation | `fgs_ppo` | `fgs_frap_gatv2_ppo` | [vik441la](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/vik441la) | `fgs_ablation` | finished | 2026-06-13 | 200 | 460.664 | 617.002 | 7.767 | 614.756 | `best_validation` |
| FGS ablation | `fgs_ppo` | `fgs_mlp_gat_ppo` | [f3djwjx7](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/f3djwjx7) | `fgs_ablation` | finished | 2026-06-13 | 180 | 261.213 | 491.963 | 4.933 | 406.636 | `best_validation` |
| FGS ablation | `fgs_ppo` | `fgs_mlp_gatv2_ppo` | [b04863fh](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/b04863fh) | `fgs_ablation` | finished | 2026-06-13 | 195 | 88.601 | 234.931 | 2.578 | 253.487 | `best_validation` |
| FGSv2 | `fgsv2` | `fgsv2_sac` | [4pn2fg93](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/4pn2fg93) | `fgsv2` | finished | 2026-06-17 | 5 | 13.845 | 53.665 | 12.896 | 191.372 | `best_validation` |
| FGSv3 | `fgsv3` | `fgsv3_frap_gatv2_sac` | [76dz4us4](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/76dz4us4) | `fgsv3` | finished | 2026-06-17 | 20 | 11.086 | 45.274 | 12.412 | 179.146 | `best_validation` |
| FGSv3 | `fgsv3` | `fgsv3_frap_gatv2_sac_presslight_rescofix` | [2ay8xrsj](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/2ay8xrsj) | `fgsv3` | finished | 2026-06-22 | 168 | 87.087 | 130.44 | 2.035 | 261.427 | `best_validation` |
| FGSv3 | `fgsv3_ppo` | `fgsv3_frap_gatv2_ppo` | [iwd3hutz](https://wandb.ai/jv-fuisl-vietnamese-german-university/marl-traffic-gat/runs/iwd3hutz) | `fgsv3` | finished | 2026-06-17 | 90 | 22.897 | 68.391 | 0.712 | 203.9 | `best_validation` |
