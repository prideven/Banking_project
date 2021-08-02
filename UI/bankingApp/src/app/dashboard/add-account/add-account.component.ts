import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Account, AccountDetails } from 'src/app/core';
import { DashboardService } from 'src/app/core/services/dashboard';

@Component({
  selector: 'app-add-account',
  templateUrl: './add-account.component.html',
  styleUrls: ['./add-account.component.scss']
})
export class AddAccountComponent implements OnInit {
  public accountType = new FormControl();
  constructor(private dashboardService: DashboardService, private snackBar: MatSnackBar) { }

  ngOnInit(): void {

}




  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }
  
  addAccount() {
    this.dashboardService.addAccount(this.accountType.value, sessionStorage.getItem('username')).subscribe(response => {
      if(response.success === 'true') {
        this.openSnackBar(response.Message, 'mat-primary');
      } else {
        this.openSnackBar(response.Message, 'mat-warn');

      }
    }, error=> {
      this.openSnackBar(error.Message, 'mat-warn');

    });
  }

}
