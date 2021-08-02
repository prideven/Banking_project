import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { Account, AccountDetails, SharedService } from 'src/app/core';
import { DashboardService, TransferInput } from 'src/app/core/services/dashboard';

@Component({
  selector: 'app-deposit-withdraw',
  templateUrl: './deposit-withdraw.component.html',
  styleUrls: ['./deposit-withdraw.component.scss']
})
export class DepositWithdrawComponent implements OnInit {

  public depWithForm: FormGroup;
  public serviceType: string;
  public accountDetails: Account[];
  public isSavings: boolean = false;
  public isChecking: boolean =false;
  public savingAccountNum: string;
  public checkingAccountNum: string;
  constructor(private formBuilder: FormBuilder, private route: ActivatedRoute, private dashboardService: DashboardService, private snackBar: MatSnackBar, private sharedService: SharedService) { 
    this.depWithForm = this.formBuilder.group({
      amount: [0, Validators.required],
      accountNum: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(data => {
      this.serviceType = data.serviceType;
    });
    this.accountDetails = JSON.parse(sessionStorage.getItem('accountList'));
    this.setAlreadyExistingAcc()
  }

  setAlreadyExistingAcc() {
    this.savingAccountNum = this.accountDetails.filter(account => account.accountType === 'Savings')[0]?.accountNumber;
    this.checkingAccountNum = this.accountDetails.filter(account => account.accountType === 'Checking')[0]?.accountNumber;
    if(this.savingAccountNum) {
      this.isSavings = true;
    }
    if(this.checkingAccountNum) {
      this.isChecking = true;
    }
  }

  openSnackBar(message: string, className: string) {
    this.snackBar.open(message, '', {
      duration: 5000,
      panelClass: ['mat-toolbar', className]
    });
  }

  onSubmit(formDirective) {
    let type;
    let bodyObj: TransferInput={amount: this.depWithForm.value.amount};
    if(this.serviceType === 'deposit') {
      bodyObj['transactionType']="credit";
      bodyObj['toAcc'] = this.depWithForm.value.accountNum;
    } else {
      bodyObj['transactionType'] = "debit";
      bodyObj['fromAcc'] = this.depWithForm.value.accountNum;
    }
    this.dashboardService.transferInternal(bodyObj).subscribe(response => {
        if(response.success === 'true') {
          this.openSnackBar(response.Message, 'mat-primary');
          formDirective.resetForm();
         this.depWithForm.reset();
          this.sharedService.accountDetails.next(true);
        } else {
          this.openSnackBar(response.error.message, 'mat-warn');

        }
    }, error=> {
      this.openSnackBar(error.error.message, 'mat-warn');

    });


  }
}
