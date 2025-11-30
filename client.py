import grpc
import banking_pb2
import banking_pb2_grpc


def get_balance(account_stub):
    user_id = input("Enter user ID: ")
    try:
        response = account_stub.getBalance(
            banking_pb2.AccountRequest(user_id=user_id)
        )
        print(f"\n✅ Balance for {response.user_id}: {response.balance}")
        print(f"Message: {response.message}\n")
    except grpc.RpcError as e:
        print(f"\n❌ Error: {e.code().name} - {e.details()}\n")


def update_balance(account_stub):
    user_id = input("Enter user ID: ")
    amount_str = input("Enter amount (+ for deposit, - for withdrawal): ")

    try:
        amount = float(amount_str)
    except ValueError:
        print("\n❌ Invalid amount\n")
        return

    try:
        response = account_stub.updateBalance(
            banking_pb2.UpdateBalanceRequest(
                user_id=user_id, amount=amount
            )
        )
        print(
            f"\n✅ New balance for {response.user_id}: {response.balance}"
        )
        print(f"Message: {response.message}\n")
    except grpc.RpcError as e:
        print(f"\n❌ Error: {e.code().name} - {e.details()}\n")


def initiate_transfer(transaction_stub):
    from_user = input("From user ID: ")
    to_user = input("To user ID: ")
    amount_str = input("Amount to transfer: ")
    description = input("Description (optional): ")

    try:
        amount = float(amount_str)
    except ValueError:
        print("\n❌ Invalid amount\n")
        return

    try:
        response = transaction_stub.initiateTransfer(
            banking_pb2.TransferRequest(
                from_user_id=from_user,
                to_user_id=to_user,
                amount=amount,
                description=description,
            )
        )
        print("\n✅ Transfer result:")
        print(f"Success: {response.success}")
        print(f"Message: {response.message}")
        print(
            f"From ({from_user}) new balance: {response.from_new_balance}"
        )
        print(f"To ({to_user}) new balance: {response.to_new_balance}\n")
    except grpc.RpcError as e:
        print(f"\n❌ Error: {e.code().name} - {e.details()}\n")


def get_transaction_history(transaction_stub):
    user_id = input("Enter user ID: ")
    try:
        response = transaction_stub.getTransactionHistory(
            banking_pb2.TransactionHistoryRequest(user_id=user_id)
        )
        print(f"\n📜 Transaction history for {user_id}:")
        if not response.transactions:
            print("No transactions found.\n")
            return

        for tx in response.transactions:
            print("------------------------------")
            print(f"Transaction ID: {tx.transaction_id}")
            print(f"From: {tx.from_user_id}")
            print(f"To: {tx.to_user_id}")
            print(f"Amount: {tx.amount}")
            print(f"Description: {tx.description}")
            print(f"Timestamp: {tx.timestamp}")
        print("------------------------------\n")
    except grpc.RpcError as e:
        print(f"\n❌ Error: {e.code().name} - {e.details()}\n")


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        account_stub = banking_pb2_grpc.AccountServiceStub(channel)
        transaction_stub = banking_pb2_grpc.TransactionServiceStub(channel)

        while True:
            print("====== Banking gRPC Client ======")
            print("1. Get balance")
            print("2. Update balance (deposit/withdraw)")
            print("3. Initiate transfer")
            print("4. Get transaction history")
            print("5. Exit")
            choice = input("Enter choice: ")

            if choice == "1":
                get_balance(account_stub)
            elif choice == "2":
                update_balance(account_stub)
            elif choice == "3":
                initiate_transfer(transaction_stub)
            elif choice == "4":
                get_transaction_history(transaction_stub)
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("\n❌ Invalid choice\n")


if __name__ == "__main__":
    main()