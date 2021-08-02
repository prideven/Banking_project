import { Routes } from '@angular/router';
import { DepositWithdrawComponent } from './deposit-withdraw/deposit-withdraw.component';
import { HomeComponent } from './home/home.component';
import { MyAccountsComponent } from './my-accounts/my-accounts.component';
import { OneTimeTransferComponent } from './one-time-transfer/one-time-transfer.component';
import { RecurringComponent } from './recurring/recurring.component';
import { TransactionsComponent } from './transactions/transactions.component';
import { TransferComponent } from './transfer/transfer.component';

export const DashboardRoutes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'accounts', component: MyAccountsComponent},
  { path: 'transactions/:accNumber',component: TransactionsComponent},
  {path: 'services/:serviceType', component: DepositWithdrawComponent},
  {path: 'transfer', component: TransferComponent},
  {path: 'oneTime/:interIntraType', component: OneTimeTransferComponent},
  {path: 'recurring/:interIntraType', component: RecurringComponent}
];
