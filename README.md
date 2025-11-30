
# Banking gRPC System

The **Banking gRPC System** is a backend project built using **Python**, **gRPC**, and **Protocol Buffers** to simulate essential banking operations such as checking balances, performing deposits/withdrawals, transferring funds between users, and viewing transaction history. The project demonstrates efficient client-server communication using RPC calls, real-time responses, and structured data handling through Protobuf.

---

## 🚀 Project Overview

This system consists of:
- A **gRPC server** that manages accounts, balances, and transactions
- A **gRPC client** that allows users to interact with the server through a menu-driven interface
- A **Protobuf service definition (`banking.proto`)** that defines all banking RPC methods and message types

The aim is to model real-world banking actions in a clean, extensible, and high-performance architecture using gRPC.

---

## 📌 Features

### 🔹 1. Get Account Balance
Retrieve the real-time balance of any user.
- Returns balance
- Includes success/error message

### 🔹 2. Deposit / Withdraw (Update Balance)
Allows updating account balance with positive (deposit) or negative (withdraw) values.
- Validates transaction amounts
- Returns updated balance

### 🔹 3. Fund Transfer Between Users
Secure transfer of funds from one user to another.
- Generates unique transaction ID
- Updates balances of sender and receiver
- Returns success/failure response
- Handles errors such as **insufficient funds**

### 🔹 4. View Transaction History
Displays all past transactions for a user, including:
- Transaction ID  
- Sender and receiver  
- Amount  
- Description  
- Timestamp  

---

## 🧩 Technologies Used

- Python 3  
- gRPC  
- grpcio & grpcio-tools  
- Protocol Buffers  
- VS Code  
- Virtual environment (venv)

---

## 📦 How It Works

### ✔️ 1. Define services in `banking.proto`
- `AccountService`
  - `getBalance`
  - `updateBalance`
- `TransactionService`
  - `initiateTransfer`
  - `getTransactionHistory`

### ✔️ 2. Generate Python files from Protobuf
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. banking.proto

✔️ 3. Run the gRPC server

python server.py

Server runs on:

port 50051

✔️ 4. Run the gRPC client

python client.py

Users can:
	•	Check balance
	•	Deposit/withdraw
	•	Transfer money
	•	View history
	•	Test error cases (e.g., insufficient funds)

⸻

📸 Screenshots (From Testing)
	•	Successful pip installation and setup
	•	Proto file compiled successfully
	•	Server running on port 50051
	•	Client performing:
	•	Balance checks
	•	Deposits/withdrawals
	•	Valid fund transfers
	•	Failed transfer due to insufficient balance
	•	Viewing transaction history

⸻

🎯 Learning Outcomes

Through this project, the following concepts were practiced:
	•	RPC-based communication
	•	Defining and generating Protobuf messages
	•	Implementing gRPC server logic
	•	Client-server architecture
	•	Validating banking operations
	•	Handling errors in distributed systems
	•	Designing structured transaction logs
	•	Building interactive Python client applications

⸻

👤 Author

Ashfaaq KT
Banking gRPC System — using Python, gRPC & Protobuf
