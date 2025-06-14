from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load model và tokenizer từ thư mục đã huấn luyện
model = AutoModelForSequenceClassification.from_pretrained("./results/sarcasm_model")
tokenizer = AutoTokenizer.from_pretrained("./results/sarcasm_model")
model.eval()


def predict_sarcasm(text):
    # Token hóa input
    predicted_class = "default"
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # Move input tensors and model to the same device
    # (Use 'cuda' if available, otherwise 'cpu')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)  # Ensure model is on the correct device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Đưa vào mô hình
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits # Now outputs should have logits attribute
        probs = F.softmax(logits, dim=-1)
        predicted_label = torch.argmax(probs, dim=-1).item()

    match predicted_label:
        case 0:
            predicted_class = "Bình thường"
        case 1:
            predicted_class = "Mỉa mai"

    return predicted_class, probs.squeeze()[predicted_label]
