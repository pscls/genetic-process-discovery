import math

def get_g_score(predicted_probs, true_probs):
    pred_dict = {trace: prob for (trace, prob) in predicted_probs}
    true_dict = {trace: prob for (trace, prob) in true_probs}
    
    g_score = 0
    for key in set(list(pred_dict.keys()) + list(true_dict.keys())):
        true_value = true_dict[key] if key in true_dict else 0
        pred_value = pred_dict[key] if key in pred_dict else 0
        g_score += math.sqrt(true_value * pred_value)

    return g_score