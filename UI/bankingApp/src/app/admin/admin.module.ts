import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminHomeComponent } from './admin-home/admin-home.component';
import { RouterModule } from '@angular/router';
import { AdminRoutes } from './admin.routes';
import { MaterialModule } from '../material/material.module';
import { AdminTransactionsComponent } from './admin-transactions/admin-transactions.component';
import { AdminRefundComponent } from './admin-refund/admin-refund.component';
import { AdminFeesComponent } from './admin-fees/admin-fees.component';
import { AddAdminAccountComponent } from './add-admin-account/add-admin-account.component';



@NgModule({
  declarations: [AdminHomeComponent, AdminTransactionsComponent, AdminRefundComponent, AdminFeesComponent, AddAdminAccountComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(AdminRoutes),
    MaterialModule
  ]
})
export class AdminModule { }
