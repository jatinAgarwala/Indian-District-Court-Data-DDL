import torch
from data import train, test, valid, DataDispFem, DataDispNoFem
from torch.utils.data import DataLoader
from tqdm import tqdm

INPUT_SIZE = 13
OUTPUT_SIZE = 52
HIDDEN_LAYER_SIZE = 100

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.f1 = torch.nn.Linear(INPUT_SIZE, HIDDEN_LAYER_SIZE)
        self.f2 = torch.nn.Linear(HIDDEN_LAYER_SIZE, OUTPUT_SIZE)
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001)

    def forward(self, x):
        x = torch.nn.functional.relu(self.f1(x))
        x = self.f2(x)
        return x

    def train(self, train, val, n_epochs):
        for epoch in tqdm(range(n_epochs), desc="Train Epochs"):
            avg_loss = 0
            iter = 0
            correct = 0
            total = 0
            train_dl = DataLoader(train, batch_size=8, shuffle=True)
            for batch in tqdm(train_dl, desc="Training"):
                self.optimizer.zero_grad()
                output = self.forward(batch[0])
                loss = torch.nn.CrossEntropyLoss(output, batch[1])

                avg_loss += loss
                correct += (output == batch[1]).sum().item()
                total += len(batch[1])
                iter += 1

                print(f"Training Loss: {loss}")
                loss.backward()
                self.optimizer.step()

            print(f"Average Training Loss for Epoch {epoch}: {avg_loss/iter}")
            print(f"Training Accuracy: {100*correct/total}")
            val_dl = DataLoader(val, batch_size=8, shuffle=True)
            for batch in tqdm(val_dl, desc="Validating"):
                output = self.forward
                loss = torch.nn.CrossEntropyLoss(output, batch[1])
                print(f"Validation Loss: {loss}")

    def test(self, test):
        test_dl = DataLoader(test, batch_size=8, shuffle=True)
        correct = 0
        total = 0
        for batch in tqdm(test_dl, desc="Testing"):
            output = self.forward
            loss = torch.nn.CrossEntropyLoss(output, batch[1])
            correct += (output == batch[1]).sum().item()
            total += len(batch[1])
            print(f"Test Loss: {loss}")        
            print(f"Test Accuracy: {100*correct/total}")

model = Model()
print("Model initialised")
train_ds = DataDispFem(train)
valid_ds = DataDispFem(valid)
model.train(train_ds, valid_ds, 5)
test_ds = DataDispFem(test)
model.test(test_ds)
