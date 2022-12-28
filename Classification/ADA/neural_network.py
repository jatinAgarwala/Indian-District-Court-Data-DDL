import torch
import torch.nn as nn

from tqdm import tqdm

from torch.utils.data import DataLoader
from data import PreProcessing, DataDispFem, DataDispNoFem

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

dataset_classes = [DataDispFem, DataDispNoFem]

for guilty in [False, True]:
    train, valid, test = PreProcessing('cases_2010.csv', guilty)
    dc_i = 0
    for dc in dataset_classes:
        train_dataloader = DataLoader(dc(train), batch_size=128)
        valid_dataloader = DataLoader(dc(valid), batch_size=128)

        class NeuralNet(nn.Module):
            def __init__(self, input_size, hidden_size, num_classes):
                super(NeuralNet, self).__init__()
                self.fc1 = nn.Linear(input_size, hidden_size)
                self.relu = nn.ReLU()
                self.fc2 = nn.Linear(hidden_size, num_classes)
            
            def forward(self, x):
                out = self.fc1(x)
                out = self.relu(out)
                out = self.fc2(out)
                return out

        if dc == DataDispFem:
            if guilty:
                model = NeuralNet(13, 128, 2).to(DEVICE)    
            else:
                model = NeuralNet(13, 128, 52).to(DEVICE)
        else:
            if guilty:
                model = NeuralNet(9, 128, 2).to(DEVICE)
            else:
                model = NeuralNet(9, 128, 52).to(DEVICE)
            
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        num_epochs = 10
        prev_acc = 0
        for epoch in range(num_epochs):
            for batch in tqdm(train_dataloader, desc="Training"):
                outputs = model(batch[0])
                loss = criterion(outputs, batch[1])
                # print(f"Training Loss: {loss}")
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            
            correct = 0
            total = 0
            with torch.no_grad():
                for batch in tqdm(valid_dataloader, desc="Validating"):
                    outputs = model(batch[0])
                    _, predicted = torch.max(outputs.data, 1)
                    total += batch[1].size(0)
                    correct += (predicted == batch[1]).sum().item()
            
            curr_acc = 100*correct/total
            print('Epoch [{}/{}], Loss: {:.4f}, Accuracy: {:.2f}%'
                .format(epoch+1, num_epochs, loss.item(), curr_acc))

            if curr_acc < prev_acc:
                break
            prev_acc = curr_acc

            if dc_i == 0:
                if guilty:
                    torch.save(model.state_dict(), "guilty_model_fem.pth")
                else:
                    torch.save(model.state_dict(), "model_fem.pth")
            else:
                if guilty:
                    torch.save(model.state_dict(), "guilty_model_no_fem.pth")
                else:
                    torch.save(model.state_dict(), "model_no_fem.pth")

        test_dataloader = DataLoader(dc(test), batch_size=128)

        correct = 0
        total = 0
        with torch.no_grad():
            for batch in tqdm(test_dataloader, desc="Testing"):
                outputs = model(batch[0])
                _, predicted = torch.max(outputs.data, 1)
                total += batch[1].size(0)
                correct += (predicted == batch[1]).sum().item()

        print('Test Accuracy: {:.2f}%'.format(100*correct/total))
