import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthenticationComponent } from './pages/authentication/authentication.component';
import { AuthenticationModule } from './pages/authentication/authentication.module';
import { HomeComponent } from './pages/home/home.component';
import { HomeModule } from './pages/home/home.module';

const routes: Routes = [
  { path: '', redirectTo: '/authenticate/login', pathMatch: 'full' },
  { path: 'authenticate', component: AuthenticationComponent, pathMatch: 'prefix' },
  { path: 'home', component: HomeComponent, pathMatch: 'prefix' },

];

@NgModule({
  imports: [RouterModule.forRoot(routes), AuthenticationModule, HomeModule],
  exports: [RouterModule]
})
export class AppRoutingModule { }
