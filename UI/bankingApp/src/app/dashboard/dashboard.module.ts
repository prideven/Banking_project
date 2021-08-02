import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import { RouterModule } from '@angular/router';
import { DashboardRoutes } from './dashboard.routes';
import { MaterialModule } from '../material/material.module';
import { MyAccountsComponent } from './my-accounts/my-accounts.component';
import { TransactionsComponent } from './transactions/transactions.component';
import { ConfirmBoxComponent } from './confirm-box/confirm-box.component';
import { AddAccountComponent } from './add-account/add-account.component';
import { DepositWithdrawComponent } from './deposit-withdraw/deposit-withdraw.component';
import { TransferComponent } from './transfer/transfer.component';
import { OneTimeTransferComponent } from './one-time-transfer/one-time-transfer.component';
import { RecurringComponent } from './recurring/recurring.component';



@NgModule({
  declarations: [HomeComponent, MyAccountsComponent, TransactionsComponent, ConfirmBoxComponent, AddAccountComponent, DepositWithdrawComponent, TransferComponent, OneTimeTransferComponent, RecurringComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(DashboardRoutes),
    MaterialModule
  ]
})
export class DashboardModule { }
