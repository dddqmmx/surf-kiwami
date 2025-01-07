import {Component, OnInit} from '@angular/core';
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-account-manage',
  standalone: true,
  imports: [
    FormsModule
  ],
  templateUrl: './account-manage.component.html',
  styleUrl: './account-manage.component.css'
})
export class AccountManageComponent implements OnInit {
  rememberMe = false;

  ngOnInit(): void {
    const storedRememberMe = localStorage.getItem('rememberMe') || '';

    if (storedRememberMe === 'true') {
      this.rememberMe = true;
    }
  }

  onRememberMeChange(newValue: boolean): void {
    localStorage.setItem('rememberMe', newValue.toString());
  }


}
