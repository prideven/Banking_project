import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { Account } from 'src/app/core';
import { DashboardService } from 'src/app/core/services/dashboard';

@Component({
  selector: 'app-recurring',
  templateUrl: './recurring.component.html',
  styleUrls: ['./recurring.component.scss']
})
export class RecurringComponent implements OnInit {
  public recurring: FormGroup;
  public accountDetails: Account[];
  public isSavings: boolean = false;
  public isChecking: boolean =false;
  public savingAccountNum: string;
  public checkingAccountNum: string;
  public transferType;
  public isInternal;
  public interIntraType;
  public date;
  constructor(private snackBar: MatSnackBar, private formBuilder: FormBuilder, private activeRoute: ActivatedRoute, private dashboardService: DashboardService) { 
    this.recurring = this.formBuilder.group({
      amount: [0, Validators.required],
      fromAcc: ['', Validators.required],
      toAcc: [''],
      externalAcc: [''],
      description: ['', Validators.required],
      numberOfMonths: [0, Validators.required]
    });

    
  }

  ngOnInit(): void {
    this.date= new Date().getDate();
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
    let obj = this.recurring.value;
    if(!this.isInternal) {
    obj.toAcc = obj.externalAcc;
    }
    delete(obj.externalAcc);
    this.dashboardService.recurringTransfer(obj).subscribe(response => {
      if(response.success === 'true') {
        this.openSnackBar(response.Message, 'mat-primary');
        formDirective.resetForm();
        this.recurring.reset();
        
      } else {
        this.openSnackBar(response.Message, 'mat-warn');
      }
    }, error => {
      this.openSnackBar(error.Message, 'mat-warn');
    });
  }

  nth() {
    switch (this.date % 10) {
      case 1:  return "st";
      case 2:  return "nd";
      case 3:  return "rd";
      default: return "th";
    }
  }

}
