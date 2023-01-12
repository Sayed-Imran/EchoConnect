import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { PostboxComponent } from './postbox/postbox.component';
import { ProfileComponent} from './profile/profile.component'
const routes: Routes = [
  {
    path: 'home',
    component: HomeComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full'},
      { path: 'dashboard', component: DashboardComponent, pathMatch: 'full' },
      { path: 'postbox', component: PostboxComponent, pathMatch: 'full' },
      { path: 'profile', component: ProfileComponent, pathMatch: 'full' }
    ],
    pathMatch: 'prefix'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HomeRoutingModule { }
