import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTableDataSource } from '@angular/material/table';
import { ActivatedRoute } from '@angular/router';
import { Account } from 'src/app/core';
import { Transaction, DashboardService } from 'src/app/core/services/dashboard';
@Component({
  selector: 'app-admin-transactions',
  templateUrl: './admin-transactions.component.html',
  styleUrls: ['./admin-transactions.component.scss']
})
export class AdminTransactionsComponent implements OnInit {

  
  public searchKey: string;
  public originalList: Transaction[];
  public dataSource = new MatTableDataSource();
  range = new FormGroup({
    start: new FormControl(),
    end: new FormControl()
  });
  public minDate: Date;
  public maxDate: Date;
  public displayedColumns: string[] = ['transactionID','dateTime','description', 'fromAcc', 'toAcc', 'amount', 'modeOfTransaction', 'transactionType']
    constructor(private activeRoute: ActivatedRoute, private dashboardService: DashboardService, private snackBar: MatSnackBar) {
      
     }
    
    ngOnInit(): void {
      this.getTransactions();
       const today = new Date();
       const month = today.getMonth()-6;
       const year = today.getFullYear()-1;
       this.minDate = new Date(year, month,today.getDate() );
       this.maxDate = new Date();
    }
    getTransactions() {
      this.dashboardService.getAdminTransactions().subscribe(response => {
        if(response.success === 'true') {
          this.dataSource.data = response.data;
          this.originalList = response.data.slice();
          this
        } else {
          this.openSnackBar(response.error.message, 'mat-warn')
        }
      }, error=> {
        this.openSnackBar(error.error.message, 'mat-warn')
      })
    }
  
    openSnackBar(message: string, className: string) {
      this.snackBar.open(message, '', {
        duration: 5000,
        panelClass: ['mat-toolbar', className]
      });
    }
  

    
  
  
    searchTransactions() {
      if (this.searchKey && this.searchKey !== '') {
        const listOfData: Transaction[] = this.originalList.slice();
        this.dataSource.data = listOfData.filter((product) => {
          return (product.description.toLowerCase().includes(this.searchKey.toLowerCase()) )
        });
      } else {
        this.dataSource.data = this.originalList.slice();                
      }
    }
  
    keyupFilter() {
      if (this.searchKey === '') {
        this.searchTransactions();
      }
    }
    applyFilters() {
      let filteredTransactions = this.originalList.slice();
  
      if(this.range.value.start && this.range.value.end) {
        filteredTransactions = filteredTransactions.filter(
          transaction => new Date(transaction.dateTime)>=this.range.value.start && new Date(transaction.dateTime)<=this.range.value.end
        );
      }
  
      this.dataSource.data = filteredTransactions.slice();
    }
  
    clearFilters() {
      this.dataSource.data = this.originalList.slice();
      this.range.reset();
    }

    refund() {
      
    }


}
