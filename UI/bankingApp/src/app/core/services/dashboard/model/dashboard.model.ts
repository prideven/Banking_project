import { ErrorResponse } from "../../login";

export interface Transaction {
amount: number;
accountBalance: number;
dateTime: Date;
description: string;
fromAcc: string;
modeOfTransaction: string;
toAcc: string;
transactionType: string
}

export  interface AdminTransaction {
    data: Transaction[];
    success: string;
    error?: ErrorResponse;
}

export interface TransactionResponse {
    success: boolean;
    data: {
        transactions: Transaction[];
    }[];
    error?: ErrorResponse
}

export interface DeleteAccount {
    success: string;

        Message: string;
    error?: ErrorResponse
}


export interface TransferInput {
    fromAcc?: string;
    toAcc?: string;
    amount: number;
    modeOfTransaction?: string;
    description?: string;
    transactionType?: string;
    numberOfMonths?: number;
}