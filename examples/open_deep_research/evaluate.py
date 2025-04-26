import json 
import numpy as np 
import argparse  
from scripts.gaia_scorer import question_scorer 


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file", type=str, required=True) 
    return parser.parse_args()

def load_results(output_file):
    results = [] 
    with open(output_file, "r") as f:
        for line in f:
            results.append(json.loads(line))
    return results 

def main(output_file):
    results = load_results(output_file) 
    scores = [] 
    level1_scores, level2_scores, level3_scores = [], [], [] 
    for i, item in enumerate(results):
        prediction = item["prediction"]
        ground_truth = item["true_answer"]
        try:
            score = question_scorer(prediction, ground_truth) 
            score = float(score)
        except Exception as e:
            score = 0.0 
        scores.append(score)
        if item["task"] == "1":
            level1_scores.append(score)
        elif item["task"] == "2":
            level2_scores.append(score)
        elif item["task"] == "3":
            level3_scores.append(score)     

    print(f"Length: {len(scores)}")
    print("Average Accuracy: {:.2f}%".format(100*np.mean(scores)))
    print("Level 1 Accuracy: {:.2f}%".format(100*np.mean(level1_scores)))
    print("Level 2 Accuracy: {:.2f}%".format(100*np.mean(level2_scores)))
    print("Level 3 Accuracy: {:.2f}%".format(100*np.mean(level3_scores)))

if __name__ == "__main__":

    args = parse_args()
    main(args.output_file)
