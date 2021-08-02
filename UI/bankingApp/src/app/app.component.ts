import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from "@angular/common";
import { SharedService } from './core';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'bankingApp';
  showSpinner = false;
  constructor(private sharedService: SharedService) {}

  ngOnInit() {
    this.sharedService.showSpinner.subscribe(data => {
      this.showSpinner = data;
    })
  }
}
