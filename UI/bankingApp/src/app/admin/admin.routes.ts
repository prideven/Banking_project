import { Routes } from '@angular/router';
import { AddAccountComponent } from '../dashboard/add-account/add-account.component';
import { AddAdminAccountComponent } from './add-admin-account/add-admin-account.component';
import { AdminFeesComponent } from './admin-fees/admin-fees.component';
import { AdminHomeComponent } from './admin-home/admin-home.component';
import { AdminRefundComponent } from './admin-refund/admin-refund.component';
import { AdminTransactionsComponent } from './admin-transactions/admin-transactions.component';

export const AdminRoutes: Routes = [
  {path: '', component: AdminHomeComponent},
  {path: 'transactions', component: AdminTransactionsComponent},
  {path: 'refund', component: AdminRefundComponent},
  {path: 'fees', component: AdminFeesComponent},
  {path: 'add-account', component: AddAdminAccountComponent}

];
