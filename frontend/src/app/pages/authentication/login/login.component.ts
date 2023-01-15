import { GoogleSigninButtonDirective } from '@abacritt/angularx-social-login/public-api';
import { DefaultResponse } from './../../../models/default-response';
import { EchoToasterService } from '../../../services/echo-toaster.service';
import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { CommonUtils } from 'src/app/utils/common-utils';
import { SocialAuthService, GoogleLoginProvider } from '@abacritt/angularx-social-login';
import { SocialUser } from '@abacritt/angularx-social-login/entities/social-user';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  loginForm = new FormGroup({
    email: new FormControl(''),
    password: new FormControl(''),
  });

  constructor(private routeService: Router, private echoToasterService: EchoToasterService, private authenticationService: AuthenticationService, private socialAuthService: SocialAuthService) {

  }

  ngOnInit(): void {
    this.googleLogin();
  }

  googleLogin(): void {
    this.socialAuthService.authState.subscribe((user) => {
      this.authenticationService.googleLogin({ id_token: user.idToken }).subscribe((response: DefaultResponse) => {
        this.echoToasterService.show(response);
        if(response.data?.token)
          CommonUtils.setAuthToken(response.data.token);
      });
    });
  }

  login() {
    try {
      this.authenticationService.login(this.loginForm.value).subscribe((response: DefaultResponse) => {
        this.echoToasterService.show(response);
        if(response.data?.token){
          CommonUtils.setAuthToken(response.data.token);
          this.routeTo('/home/dashboard');
        } else {
          this.echoToasterService.show(response || new DefaultResponse("failed", "Login Failed!"));
        }
      });
    } catch(loginErr) {
      console.error(loginErr);
    }
  }

  routeTo(route: any) {
    try{
      this.routeService.navigate([route])
    } catch(routrErr){
      console.error(routrErr);
    }
  }
}