from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load model và tokenizer từ thư mục đã huấn luyện
model = AutoModelForSequenceClassification.from_pretrained("./results")
tokenizer = AutoTokenizer.from_pretrained("./results")
model.eval()


def predict_sentiment(text):
    # Token hóa input
    global predicted_class
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # Move input tensors and model to the same device
    # (Use 'cuda' if available, otherwise 'cpu')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)  # Ensure model is on the correct device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Đưa vào mô hình
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits  # Now outputs should have logits attribute
        probs = F.softmax(logits, dim=-1)
        predicted_lable = torch.argmax(probs, dim=-1).item()

    match predicted_lable:
        case 0:
            predicted_class = "Tiêu cực"
        case 1:
            predicted_class = "Trung lập"
        case 2:
            predicted_class = "Tích cực"

    return predicted_class, probs.squeeze()[predicted_lable]
