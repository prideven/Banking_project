import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { SharedService } from 'src/app/core';
import { DashboardService } from 'src/app/core/services/dashboard';

@Component({
  selector: 'app-admin-refund',
  templateUrl: './admin-refund.component.html',
  styleUrls: ['./admin-refund.component.scss']
})
export class AdminRefundComponent implements OnInit {

  public refundForm: FormGroup;
  constructor(private formBuilder: FormBuilder, private route: ActivatedRoute, private dashboardService: DashboardService, private snackBar: MatSnackBar, private sharedService: SharedService) { 
    this.refundForm = this.formBuilder.group({
      amount: [0, Validators.required],
      toAcc: ['', Validators.required],
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
    let bodyObj = this.refundForm.value;
      bodyObj['transactionType']="credit";
      bodyObj['modeOfTransaction']="fees";
    this.dashboardService.transferInternal(bodyObj).subscribe(response => {
        if(response.success === 'true') {
          this.openSnackBar(response.Message, 'mat-primary');
          formDirective.resetForm();
          this.refundForm.reset();
        } else {
          this.openSnackBar(response.error.message, 'mat-warn');

        }
    }, error=> {
      this.openSnackBar(error.error.message, 'mat-warn');

    });


  }

}
