import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { Account, AccountDetails } from 'src/app/core';
import { DashboardService } from 'src/app/core/services/dashboard';

@Component({
  selector: 'app-one-time-transfer',
  templateUrl: './one-time-transfer.component.html',
  styleUrls: ['./one-time-transfer.component.scss']
})
export class OneTimeTransferComponent implements OnInit {
  public oneTimeTransfer: FormGroup;
  public accountDetails: Account[];
  public isSavings: boolean = false;
  public isChecking: boolean =false;
  public savingAccountNum: string;
  public checkingAccountNum: string;
  public transferType;
  public isInternal;
  public interIntraType;
  constructor(private snackBar: MatSnackBar, private formBuilder: FormBuilder, private activeRoute: ActivatedRoute, private dashboardService: DashboardService) { 
    this.oneTimeTransfer = this.formBuilder.group({
      amount: [0, Validators.required],
      fromAcc: ['', Validators.required],
      toAcc: [''],
      externalAcc: [''],
      modeOfTransaction: ['', Validators.required],
      description: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.accountDetails = JSON.parse(sessionStorage.getItem('accountList'));
    this.activeRoute.params.subscribe(data => {
      this.interIntraType = data.interIntraType;
      if(data.interIntraType === 'internal') {
        this.isInternal = true;
      } else {
        this.isInternal = false;
      }
    })
    this.setAlreadyExistingAcc();
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
    let obj = this.oneTimeTransfer.value;
    if(!this.isInternal) {
    obj.toAcc = obj.externalAcc;
    }
    delete(obj.externalAcc);
    this.dashboardService.transferExternal(obj).subscribe(response => {
      if(response.success === 'true') {
        this.openSnackBar(response.Message, 'mat-primary');
        this.oneTimeTransfer.reset();
        formDirective.resetForm();
      } else {
        this.openSnackBar(response.Message, 'mat-warn');
      }
    }, error => {
      this.openSnackBar(error.Message, 'mat-warn');
    });
  }
}
