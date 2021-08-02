
export interface ErrorResponse{
    errorCode: string
	errorStatusCode: number
	message: string
	details: string
	recommendationAction: string[]
}
export  interface LoginResponse {
    status: number; 
    success: boolean;
    data:{
        profile: {
            email: string;
            firstName: string;
            lastName: string;
            phoneNumber: string;
            isAdmin: boolean;
        };
    accessToken: string;

    }
    error?: ErrorResponse
}

export interface RegisterResponse {
success: boolean;
data?: string;
error?: ErrorResponse;
}

export interface UserParams {
    firstName: string;
    lastName: string;
    phoneNumber: string;
    email: string;
    userName: string;
}

export interface Account {
    accountType: string;
    accountNumber: string;
    accountBalance: number;
}

export interface AccountDetails {
    data: Account[];
    success: string;
    error?: ErrorResponse;
    Message: string;
}

