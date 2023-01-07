import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthenticationComponent } from './pages/authentication/authentication.component';
import { AuthenticationModule } from './pages/authentication/authentication.module';

const routes: Routes = [
  { path: '', redirectTo: '/authenticate/login', pathMatch: 'full' },
  { path: 'authenticate', component: AuthenticationComponent, pathMatch: 'prefix' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes), AuthenticationModule],
  exports: [RouterModule]
})
export class AppRoutingModule { }
