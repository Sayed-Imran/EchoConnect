import { Component, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {
  public enableSidebar: any= false;
  addclass:any = false;
  public openDropdown: any= false;
  ngOnInit(){
    
  }
  

  openSidebar() {
    this.enableSidebar = !this.enableSidebar
  }
}
