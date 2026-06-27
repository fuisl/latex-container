# Figure List

This file lists generated figure stems along with their figure group and purpose. Stems are listed without file extensions; each stem exist as `.pdf`, `.png`.

| Figure stem | Group | Description |
|---|---|---|
| `Figures/main_results_bar` | Main results | Grouped log-scale bar chart of mean delay across the six scenarios and main methods. |
| `Figures/scale_benefit` | Scale analysis | Percent improvement of best FGS variant over CoLight and PPO by network scale tier. |
| `Figures/radar_comparison` | Regional multi-metric comparison | Radar chart for regional scenarios comparing Wait, Delay, Trip, and Queue after normalization. |
| `Figures/train_curves_all_scenarios_4metrics_200ep` | Consolidated training curves | One document-style figure with six scenario rows and four metric columns; raw training curves are dimmed and 10-point running averages are foregrounded. |
| `Figures/validation_curves_all_scenarios_4metrics_200ep` | Consolidated validation curves | One document-style figure with six scenario rows and four metric columns using validation curves only, without smoothing. |
| `Figures/cologne1/delay_curves_cologne1` | Scenario delay curves | Cologne 1 training and validation mean-delay curves for selected baselines and final FGS method. |
| `Figures/cologne3/delay_curves_cologne3_training` | Scenario delay curves | Cologne 3 training mean-delay curves for all available algorithms. |
| `Figures/cologne8/delay_curves_cologne8` | Scenario delay curves | Cologne 8 training and validation mean-delay curves including PPO/SAC variants where available. |
| `Figures/ingolstadt1/delay_curves_ingolstadt1` | Scenario delay curves | Ingolstadt 1 training and validation mean-delay curves for selected baselines and final FGS method. |
| `Figures/ingolstadt7/delay_curves_ingolstadt7_training` | Scenario delay curves | Ingolstadt 7 training mean-delay curves for all available algorithms. |
| `Figures/ingolstadt21/delay_curves_ingolstadt21` | Scenario delay curves | Ingolstadt 21 training and validation mean-delay curves including PPO/SAC variants where available. |
| `Figures/ablation_encoder` | Ablation study | Combined encoder ablation figure comparing MLP and FRAP with fixed GATv2+PPO. |
| `Figures/ablation_graph` | Ablation study | Combined graph-module ablation figure comparing GATv2 and GAT with fixed MLP+PPO. |
| `Figures/ablation_rl` | Ablation study | Combined RL-backend ablation figure comparing SAC and PPO with fixed MLP+GATv2. |
| `Figures/cologne8/ablation_curves_cologne8` | Ablation study | Cologne 8 training delay curves for all available FGS ablation variants in one scenario-level figure. |
| `Figures/cologne8/ablation_encoder` | Ablation study | Cologne 8 encoder ablation, MLP versus FRAP with fixed GATv2+PPO. |
| `Figures/cologne8/ablation_graph` | Ablation study | Cologne 8 graph-module ablation, GATv2 versus GAT with fixed MLP+PPO. |
| `Figures/cologne8/ablation_rl` | Ablation study | Cologne 8 RL-backend ablation, SAC versus PPO with fixed MLP+GATv2. |
| `Figures/ingolstadt21/ablation_curves_ingolstadt21` | Ablation study | Ingolstadt 21 training delay curves for all available FGS ablation variants in one scenario-level figure. |
| `Figures/ingolstadt21/ablation_encoder` | Ablation study | Ingolstadt 21 encoder ablation, MLP versus FRAP with fixed GATv2+PPO. |
| `Figures/ingolstadt21/ablation_graph` | Ablation study | Ingolstadt 21 graph-module ablation, GATv2 versus GAT with fixed MLP+PPO. |
| `Figures/ingolstadt21/ablation_rl` | Ablation study | Ingolstadt 21 RL-backend ablation, SAC versus PPO with fixed MLP+GATv2. |
| `Figures/ablation_delay_tripcount_cologne8_200ep` | Ablation diagnostics | Cologne 8 four-panel FGS ablation diagnostic with delay and tripinfo count on dual y-axes. |
| `Figures/ablation_delay_tripcount_ingolstadt21_200ep` | Ablation diagnostics | Ingolstadt 21 four-panel FGS ablation diagnostic with delay and tripinfo count on dual y-axes. |
| `Figures/delay_queue_diagnostic` | Delay-queue diagnostics | Earlier two-panel delay and queue diagnostic figure for FGS-P runs. |
| `Figures/delay_queue_diagnostic_ppo` | Delay-queue diagnostics | PPO-only delay and mean queue dual-axis diagnostic for Cologne 8 and Ingolstadt 21. |
| `Figures/delay_queue_diagnostic_sac` | Delay-queue diagnostics | SAC-only delay and mean queue dual-axis diagnostic for Cologne 8 and Ingolstadt 21. |
| `Figures/delay_queue_diagnostic_combined` | Delay-queue diagnostics | Earlier combined PPO/SAC delay and mean queue dual-axis diagnostic figure. |
| `Figures/delay_queue_diagnostic_combined_40ep` | Delay-queue diagnostics | Four-panel PPO/SAC delay and queue diagnostic focused on the first 40 episodes. |
| `Figures/delay_queue_diagnostic_combined_200ep` | Delay-queue diagnostics | Four-panel PPO/SAC delay and queue diagnostic extended to 200 episodes. |
| `Figures/delay_tripcount_diagnostic_combined_200ep` | Delay-tripcount diagnostics | Four-panel PPO/SAC diagnostic using delay and tripinfo count on dual y-axes. |
| `Figures/frap_vs_original_delay_queue_cologne8_ingolstadt21_ppo_sac_200ep` | FRAP versus original diagnostics | Four-panel delay and queue comparison of original PPO/SAC against FRAP+GATv2 PPO/SAC for Cologne 8 and Ingolstadt 21. |
| `Figures/frap_vs_original_delay_queue_ingolstadt21_ppo_sac_200ep` | FRAP versus original diagnostics | Ingolstadt 21 focused delay and queue comparison of original PPO/SAC against FRAP+GATv2 PPO/SAC. |
| `Figures/fgsv3_sac_cologne8_variant_metrics_200ep` | FGSv3 variant comparison | Cologne 8 horizontal four-metric comparison of original FGSv3 SAC, TI4 Big, and PressLight RESCO-Fix variants. |
| `Figures/fgs_versions_cologne8_frap_gatv2_sac_metrics_200ep` | FGS version comparison | Cologne 8 four-metric comparison of FGSv1, FGSv2, and FGSv3 FRAP/GATv2/SAC lineage. |
| `Figures/fgs_versions_cologne8_train_4metrics_200ep` | FGS version comparison | Cologne 8 training curves for FGS versions across Wait, Delay, Queue, and Trip Time. |
| `Figures/fgs_versions_cologne8_validation_4metrics_200ep` | FGS version comparison | Cologne 8 validation curves for FGS versions across Wait, Delay, Queue, and Trip Time. |
| `Figures/fgs_versions_ingolstadt21_train_4metrics_200ep` | FGS version comparison | Ingolstadt 21 training curves for available FGS versions across Wait, Delay, Queue, and Trip Time. |
| `Figures/fgs_versions_ingolstadt21_validation_4metrics_200ep` | FGS version comparison | Ingolstadt 21 validation curves for available FGS versions across Wait, Delay, Queue, and Trip Time. |
| `Figures/fgs_versions_cologne8_ingolstadt21_train_validation_delay_200ep` | FGS version comparison | Single four-panel mean-delay comparison: Cologne 8 training, Cologne 8 validation, Ingolstadt 21 training, and Ingolstadt 21 validation. |
