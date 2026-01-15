import re
import pandas as pd
from pathlib import Path


class K2PReviewer:
    """
    Class to evaluate K2P (Knowledge to Prediction) pipeline performance
    by comparing clingo output with ground truth rule firings.
    """
    
    def __init__(self, ground_truth_path, clingo_output_path):
        """
        Initialize the K2P reviewer.
        
        Args:
            ground_truth_path: Path to the K2P ground truth CSV file
            clingo_output_path: Path to the clingo output file
        """
        self.ground_truth_path = Path(ground_truth_path)
        self.clingo_output_path = Path(clingo_output_path)
        self.gt_rules_by_patient = {}
        self.clingo_rules_by_patient = {}
        
    def parse_rule_list(self, s):
        """
        Parse a rule list string from ground truth CSV.
        
        Example input: "[1.1.4; 1.1.18]"
        Output: set of strings: {"1.1.4", "1.1.18"}
        """
        if pd.isna(s):
            return set()
        s = s.strip()
        if s.startswith("[") and s.endswith("]"):
            s = s[1:-1]
        # split on ';' and strip whitespace
        rules = [r.strip() for r in s.split(";") if r.strip()]
        return set(rules)
    
    def load_ground_truth(self):
        """Load and parse ground truth from CSV file."""
        gt_df = pd.read_csv(self.ground_truth_path)
        self.gt_rules_by_patient = {
            int(row["Patient"]): self.parse_rule_list(row["Rules to fire"])
            for _, row in gt_df.iterrows()
        }
    
    def load_clingo_output(self):
        """Load and parse clingo output file."""
        self.clingo_rules_by_patient = {}
        current_patient = None
        
        with open(self.clingo_output_path, "r") as f:
            for line in f:
                line = line.strip()
                
                # Detect patient header: "=== Patient X ==="
                m = re.match(r"=== Patient\s+(\d+)\s+===", line)
                if m:
                    current_patient = int(m.group(1))
                    self.clingo_rules_by_patient.setdefault(current_patient, set())
                    continue
                
                if current_patient is None:
                    continue
                
                # Extract all fired("...") occurrences on this line
                fired_rules = re.findall(r'fired\("([^"]+)"\)', line)
                if fired_rules:
                    self.clingo_rules_by_patient[current_patient].update(fired_rules)
    
    def compute_metrics(self):
        """
        Compute TP, FP, FN, precision, recall, and F1 for all patients.
        
        Returns:
            tuple: (per_patient_df, global_metrics_dict)
        """
        all_patients = sorted(
            set(self.gt_rules_by_patient.keys()) | 
            set(self.clingo_rules_by_patient.keys())
        )
        
        total_tp = total_fp = total_fn = 0
        per_patient_metrics = []
        
        for pid in all_patients:
            gt = self.gt_rules_by_patient.get(pid, set())
            pred = self.clingo_rules_by_patient.get(pid, set())
            
            tp = len(gt & pred)
            fp = len(pred - gt)
            fn = len(gt - pred)
            
            total_tp += tp
            total_fp += fp
            total_fn += fn
            
            # per-patient precision/recall/F1
            prec_p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec_p = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1_p = 2 * prec_p * rec_p / (prec_p + rec_p) if (prec_p + rec_p) > 0 else 0.0
            
            per_patient_metrics.append({
                "Patient": pid,
                "TP": tp,
                "FP": fp,
                "FN": fn,
                "Precision": prec_p,
                "Recall": rec_p,
                "F1": f1_p,
                "GT_rules": sorted(gt),
                "Pred_rules": sorted(pred),
            })
        
        per_patient_df = pd.DataFrame(per_patient_metrics)
        
        # Global (micro-averaged) precision, recall, F1
        precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
        recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        global_metrics = {
            "TP": total_tp,
            "FP": total_fp,
            "FN": total_fn,
            "Precision": precision,
            "Recall": recall,
            "F1": f1
        }
        
        return per_patient_df, global_metrics
    
    def evaluate_and_save(self, output_csv_path=None):
        """
        Run complete evaluation pipeline and optionally save results.
        
        Args:
            output_csv_path: Optional path to save per-patient metrics CSV
            
        Returns:
            tuple: (per_patient_df, global_metrics_dict)
        """
        self.load_ground_truth()
        self.load_clingo_output()
        per_patient_df, global_metrics = self.compute_metrics()
        
        # Print global metrics
        print("\n=== K2P Evaluation: Global metrics (micro-averaged) ===")
        print(f"TP: {global_metrics['TP']}, FP: {global_metrics['FP']}, FN: {global_metrics['FN']}")
        print(f"Precision: {global_metrics['Precision']:.3f}")
        print(f"Recall:    {global_metrics['Recall']:.3f}")
        print(f"F1 score:  {global_metrics['F1']:.3f}")
        
        # Save per-patient metrics if output path provided
        if output_csv_path:
            per_patient_df.to_csv(output_csv_path, index=False)
            print(f"\nPer-patient metrics saved to: {output_csv_path}")
        
        return per_patient_df, global_metrics


# For backward compatibility / standalone script usage
if __name__ == "__main__":
    # Example standalone usage
    BASE_DIR = Path(__file__).parent.parent.parent
    GT_PATH = BASE_DIR / "src" / "input_files" / "ground_truths" / "K2P_ground_truth.csv"
    CLINGO_PATH = BASE_DIR / "src" / "output_files" / "CLAUDE" / "pancreatic cancer" / "K2P" / "clingo_output.txt"
    
    reviewer = K2PReviewer(GT_PATH, CLINGO_PATH)
    per_patient_df, global_metrics = reviewer.evaluate_and_save()
    
    print("\n=== Per-patient metrics ===")
    print(per_patient_df[["Patient", "TP", "FP", "FN", "Precision", "Recall", "F1"]])