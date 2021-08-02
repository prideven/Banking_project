import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-transfer',
  templateUrl: './transfer.component.html',
  styleUrls: ['./transfer.component.scss']
})
export class TransferComponent implements OnInit {
public showInternalEx = true;
public intraInter:string;
  constructor(private router: Router) { }

  ngOnInit(): void {
  }


  setIntraInter(type) {
    this.intraInter = type;
    this.showInternalEx = false;
  }

  goBack() {
    this.showInternalEx = true;
  }



  goToPayment(type: string) {
    this.router.navigate(['dashboard/'+type+'/'+this.intraInter])
  }
}
