import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm

class MathDataset(Dataset):
    def __init__(self, textos, etiquetas, tokenizer, max_len=512):
        self.textos = textos
        self.etiquetas = etiquetas
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.textos)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.textos[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'label': torch.tensor(self.etiquetas[idx], dtype=torch.long)
        }

# === CONFIGURACIÓN ===
model_name = "tbs17/mathbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# === CARGAR DATOS ===
df = pd.read_csv("dataset_math.csv")  # CSV con columnas: texto, etiqueta
train_texts, val_texts, train_labels, val_labels = train_test_split(df["texto"], df["etiqueta"], test_size=0.2)

train_dataset = MathDataset(train_texts.tolist(), train_labels.tolist(), tokenizer)
val_dataset = MathDataset(val_texts.tolist(), val_labels.tolist(), tokenizer)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8)

# === OPTIMIZADOR ===
optimizer = AdamW(model.parameters(), lr=2e-5)

# === ENTRENAMIENTO ===
epochs = 3
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}"):
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")

# === GUARDAR MODELO ===
model.save_pretrained("mathbert-finetuned")
tokenizer.save_pretrained("mathbert-finetuned")