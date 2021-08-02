import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { ActivatedRoute } from '@angular/router';
import { Account, AccountDetails } from 'src/app/core';
import { DashboardService, Transaction } from 'src/app/core/services/dashboard';

@Component({
  selector: 'app-transactions',
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.scss']
})
export class TransactionsComponent implements OnInit {
public accountDetails;
public accountList: Account[];
public accountNum: string;
public selectedAccount: Account;
public searchKey: string;
public originalList: Transaction[];
public transactionType = new FormControl();
public transactionMode = new FormControl();
public dataSource = new MatTableDataSource();
range = new FormGroup({
  start: new FormControl(),
  end: new FormControl()
});
public minDate: Date;
public maxDate: Date;
public displayedColumns: string[] = ['transactionID', 'dateTime','description', 'fromAcc', 'toAcc', 'amount', 'modeOfTransaction', 'transactionType', 'accountBalance']
  constructor(private activeRoute: ActivatedRoute, private dashboardService: DashboardService, private snackBar: MatSnackBar) {
    
   }
  
  ngOnInit(): void {
    if(sessionStorage.getItem('accountDetails')) {
    this.accountDetails = JSON.parse(sessionStorage.getItem('accountDetails'));
    }

     this.activeRoute.params.subscribe(data => {
       this.accountNum = data.accNumber;
       this.getTransactions();
       if(sessionStorage.getItem('accountList')) {
        this.accountList = JSON.parse(sessionStorage.getItem('accountList'));
        this.getSelectedAccountDetails();
      }
     });


     const today = new Date();
     const month = today.getMonth()-6;
     const year = today.getFullYear()-1;
     this.minDate = new Date(year, month,today.getDate() );
     this.maxDate = new Date();
  }
  getTransactions() {
    this.dashboardService.getTransactions(this.accountNum, sessionStorage.getItem('username')).subscribe(response => {
      if(response.success) {
        this.dataSource.data = response.data[0].transactions;
        this.originalList = response.data[0].transactions.slice();
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

  getSelectedAccountDetails() {
    this.selectedAccount = this.accountList.filter(account => account.accountNumber === this.accountNum)[0];
  }
  


  searchTransactions() {
    if (this.searchKey && this.searchKey !== '') {
      const listOfData = this.originalList.slice();
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

    if (this.transactionMode.value) {
      filteredTransactions = filteredTransactions.filter(
        transaction => transaction.modeOfTransaction.toLowerCase() === this.transactionMode.value.toLowerCase()
      );
    }
    if (this.transactionType.value) {
      filteredTransactions = filteredTransactions.filter(
        transaction => transaction.transactionType.toLowerCase() === this.transactionType.value.toLowerCase()
      );
    }

    if(this.range.value.start && this.range.value.end) {
      filteredTransactions = filteredTransactions.filter(
        transaction => new Date(transaction.dateTime)>=this.range.value.start && new Date(transaction.dateTime)<=this.range.value.end
      );
    }

    this.dataSource.data = filteredTransactions.slice();
  }

  clearFilters() {
    this.dataSource.data = this.originalList.slice();
    this.transactionMode.setValue('');
    this.transactionType.setValue('');
    this.range.reset();
    

  }

}
