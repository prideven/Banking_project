import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DashboardService } from 'src/app/core/services/dashboard';

@Component({
  selector: 'app-add-admin-account',
  templateUrl: './add-admin-account.component.html',
  styleUrls: ['./add-admin-account.component.scss']
})
export class AddAdminAccountComponent implements OnInit {
  public addAccountForm: FormGroup;
  constructor(private formBuilder: FormBuilder,private dashboardService: DashboardService, private snackBar: MatSnackBar) {
    this.addAccountForm = this.formBuilder.group({
      username: ['', Validators.required],
      accountType: ['', Validators.required]
    });
   }

  ngOnInit(): void {
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }
  
  addAccount() {
    this.dashboardService.addAccount(this.addAccountForm.value.accountType, this.addAccountForm.value.username).subscribe(response => {
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
