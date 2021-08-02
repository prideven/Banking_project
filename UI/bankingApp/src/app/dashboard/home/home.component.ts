import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { Account, AccountDetails, LoginService, SharedService } from 'src/app/core';
import { DashboardService } from 'src/app/core/services/dashboard';
import { AddAccountComponent } from '../add-account/add-account.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
accountDetails: Account[]
  constructor(public dialog: MatDialog, private dashboardService: DashboardService, private snackBar: MatSnackBar, private router: Router, private sharedService: SharedService) { }

  ngOnInit(): void {
    this.getAccountDetails(sessionStorage.getItem('username'));
    this.sharedService.accountDetails.subscribe(res => {
      if(res) {
        this.getAccountDetails(sessionStorage.getItem('username'));
      }
    })
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }
  async getAccountDetails(username: string) {
  let response = await this.dashboardService.getAccountDetails(username);
      if(response.success) {
        sessionStorage.removeItem('accountList');
        sessionStorage.setItem('accountList', JSON.stringify(response.data));
        this.accountDetails = response.data;
        
      } else {
        this.openSnackBar(response.error.message, 'mat-warn')
      }
  
  }


  openAddAccount() {
        const dialogRef = this.dialog.open(AddAccountComponent, {
          height: '400px',
          width: '600px',
        });

    dialogRef.afterClosed().subscribe(result => {
      if(result === true) {
        this.getAccountDetails(sessionStorage.getItem('username'));

      }
    });
  }


  openDepositWithdraw(servicetype) {
    this.router.navigate(['dashboard/services', servicetype])
  }


}
