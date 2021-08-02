import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { Account, AccountDetails, SharedService } from 'src/app/core';
import { DashboardService } from 'src/app/core/services/dashboard';
import { ConfirmBoxComponent } from '../confirm-box/confirm-box.component';

@Component({
  selector: 'app-my-accounts',
  templateUrl: './my-accounts.component.html',
  styleUrls: ['./my-accounts.component.scss']
})
export class MyAccountsComponent implements OnInit {
accountList: Account[];
  constructor(private router: Router, private dashboardService: DashboardService, public dialog: MatDialog, private snackBar: MatSnackBar, private sharedService: SharedService) { }

  ngOnInit(): void {
    this.accountList = JSON.parse(sessionStorage.getItem('accountList'));
  }

  goToTransactions(accNumber) {
    this.router.navigate(['dashboard/transactions', accNumber]);
  }

  deleteAccount(accNumber) {
    this.dashboardService.deleteAccount(sessionStorage.getItem('username'),accNumber).subscribe(response => {
      if(response.success) {
        this.openSnackBar(response.Message, 'mat-warn');
        this.sharedService.accountDetails.next(true);
      } else {
        this.openSnackBar(response.Message, 'mat-warn');
      }
    }, error=> {
      this.openSnackBar(error.Message, 'mat-warn');
    })
  }

  openDialog(accNumber) {
    const dialogRef = this.dialog.open(ConfirmBoxComponent);

    dialogRef.afterClosed().subscribe(result => {
      if(result === true) {
        this.deleteAccount(accNumber);

      }
    });
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }


}
