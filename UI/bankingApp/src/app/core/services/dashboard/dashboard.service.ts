import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { TransactionResponse } from '.';
import { AccountDetails } from '..';
import { URLConstants } from '../../rest-api-configuration';
import {  AdminTransaction, DeleteAccount, TransferInput } from './model';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  baseUrl: string;
  constructor(private http: HttpClient) { 
    this.baseUrl = environment.url;
  }

    getTransactions(accNum: string, username: string): Observable<TransactionResponse> {
    return this.http.get<TransactionResponse>(`${this.baseUrl}${URLConstants.GET_TRANSACTIONS}/${username}/${accNum}`);
  }

    deleteAccount(username:string, accNum: string): Observable<DeleteAccount> {
      return this.http.delete<DeleteAccount>(`${this.baseUrl}${URLConstants.DELETE_ACCOUNT}/${username}/${accNum}`);
    }
    async getAccountDetails(username: string) {
      return await this.http.get<AccountDetails>(`${this.baseUrl}${URLConstants.GET_ACCOUNT_DETAILS}/${username}`).toPromise();;
    }
    
    addAccount(accountType: string, username: string): Observable<DeleteAccount> {
      return this.http.post<DeleteAccount>(`${this.baseUrl}${URLConstants.ADD_ACCOUNT}/${username}`, {account_type: accountType});

    } 

    transferInternal(bodyObj:TransferInput): Observable<DeleteAccount> {
      return this.http.post<DeleteAccount>(`${this.baseUrl}${URLConstants.INTERNAL_TRANSFER}`, bodyObj);

    }

    transferExternal(bodyObj:TransferInput): Observable<DeleteAccount> {
      return this.http.post<DeleteAccount>(`${this.baseUrl}${URLConstants.EXTERNAL_TRANSFER}`, bodyObj);
    }

    recurringTransfer(bodyObj:TransferInput): Observable<DeleteAccount> {
      return this.http.post<DeleteAccount>(`${this.baseUrl}${URLConstants.RECURRING_TRANSFER}`, bodyObj);
    }


    getAdminTransactions(): Observable<AdminTransaction> {
      return this.http.get<AdminTransaction>(`${this.baseUrl}${URLConstants.ADMIN_TRANSACTIONS}`);
    }
}
