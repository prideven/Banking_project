import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { SharedService } from 'src/app/core';
import { DashboardService, TransferInput } from 'src/app/core/services/dashboard';

@Component({
  selector: 'app-admin-fees',
  templateUrl: './admin-fees.component.html',
  styleUrls: ['./admin-fees.component.scss']
})
export class AdminFeesComponent implements OnInit {
  public adminFeesForm: FormGroup;
  constructor(private formBuilder: FormBuilder, private route: ActivatedRoute, private dashboardService: DashboardService, private snackBar: MatSnackBar, private sharedService: SharedService) { 
    this.adminFeesForm = this.formBuilder.group({
      amount: [0, Validators.required],
      fromAcc: ['', Validators.required],
      description: ['', Validators.required]
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

  onSubmit(formDirective) {
    let type;
    let bodyObj = this.adminFeesForm.value;
      bodyObj['transactionType']="debit";
      bodyObj['modeOfTransaction']="fees";
    this.dashboardService.transferInternal(bodyObj).subscribe(response => {
        if(response.success === 'true') {
          this.openSnackBar(response.Message, 'mat-primary');
          formDirective.resetForm();
          this.adminFeesForm.reset();
        } else {
          this.openSnackBar(response.error.message, 'mat-warn');

        }
    }, error=> {
      this.openSnackBar(error.error.message, 'mat-warn');

    });


  }
}
