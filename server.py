from concurrent import futures
from datetime import datetime
import uuid

import grpc
import banking_pb2
import banking_pb2_grpc

# In-memory "database" for demo purposes
accounts = {
    "user1": 1000.0,
    "user2": 500.0,
    "user3": 2000.0,
}

transactions = []  # list of banking_pb2.Transaction objects


class AccountService(banking_pb2_grpc.AccountServiceServicer):
    def getBalance(self, request, context):
        user_id = request.user_id

        if user_id not in accounts:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"User '{user_id}' not found",
            )

        balance = accounts[user_id]
        return banking_pb2.BalanceResponse(
            user_id=user_id,
            balance=balance,
            message="Balance retrieved successfully",
        )

    def updateBalance(self, request, context):
        user_id = request.user_id
        amount = request.amount  # +ve deposit, -ve withdraw

        if user_id not in accounts:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"User '{user_id}' not found",
            )

        if accounts[user_id] + amount < 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Insufficient funds for this update",
            )

        accounts[user_id] += amount

        return banking_pb2.BalanceResponse(
            user_id=user_id,
            balance=accounts[user_id],
            message="Balance updated successfully",
        )


class TransactionService(banking_pb2_grpc.TransactionServiceServicer):
    def initiateTransfer(self, request, context):
        from_id = request.from_user_id
        to_id = request.to_user_id
        amount = request.amount
        description = request.description or "Transfer"

        # ---- Error handling ----
        if from_id not in accounts:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Source user '{from_id}' not found",
            )

        if to_id not in accounts:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Destination user '{to_id}' not found",
            )

        if amount <= 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Amount must be positive",
            )

        if accounts[from_id] < amount:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Insufficient funds for transfer",
            )

        # ---- Perform transfer ----
        accounts[from_id] -= amount
        accounts[to_id] += amount

        # ---- Log transaction ----
        tx_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"

        tx = banking_pb2.Transaction(
            transaction_id=tx_id,
            from_user_id=from_id,
            to_user_id=to_id,
            amount=amount,
            description=description,
            timestamp=timestamp,
        )
        transactions.append(tx)

        return banking_pb2.TransferResponse(
            success=True,
            message="Transfer completed successfully",
            from_new_balance=accounts[from_id],
            to_new_balance=accounts[to_id],
        )

    def getTransactionHistory(self, request, context):
        user_id = request.user_id

        if user_id not in accounts:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"User '{user_id}' not found",
            )

        user_transactions = [
            tx
            for tx in transactions
            if tx.from_user_id == user_id or tx.to_user_id == user_id
        ]

        return banking_pb2.TransactionHistoryResponse(
            transactions=user_transactions
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    banking_pb2_grpc.add_AccountServiceServicer_to_server(
        AccountService(), server
    )
    banking_pb2_grpc.add_TransactionServiceServicer_to_server(
        TransactionService(), server
    )

    server.add_insecure_port("[::]:50051")
    print("gRPC server is running on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()