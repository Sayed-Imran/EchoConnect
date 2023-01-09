import { FormControl, FormGroup } from '@angular/forms';
import { Component } from '@angular/core';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { EchoToasterService } from 'src/app/services/echo-toaster.service';
import { Router } from '@angular/router';
import { DefaultResponse } from 'src/app/models/default-response';
import { SocialAuthService } from '@abacritt/angularx-social-login';
import { CommonUtils } from 'src/app/utils/common-utils';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {

  registrationForm =  new FormGroup({
    first_name: new FormControl(''),
    last_name: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
  });

  constructor(private echoToasterService: EchoToasterService, private authenticationService: AuthenticationService, private router: Router, private socialAuthService: SocialAuthService) { }

  ngOnInit(): void {
    this.googleLogin();
  }

  register() {
    console.log(this.registrationForm.value);
    this.authenticationService.register(this.registrationForm.value).subscribe((response: DefaultResponse) => {
      this.echoToasterService.show(response);
      if(response.status=="success")
        this.router.navigate(['/authenticate/login']);
    });
  }

  googleLogin(): void {
    this.socialAuthService.authState.subscribe((user) => {
      this.authenticationService.googleLogin({ id_token: user.idToken }).subscribe((response: DefaultResponse) => {
        this.echoToasterService.show(response);
        if (response.data?.token)
          CommonUtils.setAuthToken(response.data.token);
      });
    });
  }

}
